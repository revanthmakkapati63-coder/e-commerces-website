import re
import html
from datetime import datetime
from flask import request, g, current_app
from app import db
from app.models import BlockedRequest, ValidationRule, RequestLog

# ---------- Compiled regex patterns ----------
# More precise SQL injection patterns - avoid false positives on common words
SQLI_PATTERNS = [
    re.compile(r"(?i)(\bunion\b\s+\bselect\b)"),
    re.compile(r"(?i)(\bselect\b\s+.*\bfrom\b)"),
    re.compile(r"(?i)(\binsert\b\s+\binto\b)"),
    re.compile(r"(?i)(\bupdate\b\s+\bset\b)"),
    re.compile(r"(?i)(\bdelete\b\s+\bfrom\b)"),
    re.compile(r"(?i)(\bor\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+['\"]?)"),
    re.compile(r"(?i)(--|#|;|/\*|\*/)"),
    re.compile(r"(?i)(\bxp_cmdshell\b)"),
    re.compile(r"(?i)(\bexec\b\s*\()"),
    re.compile(r"(?i)(\bdrop\b\s+\btable\b)"),
    re.compile(r"(?i)(\balter\b\s+\btable\b)"),
]

XSS_PATTERNS = [
    re.compile(r"(?i)<script[^>]*>.*?</script>"),
    re.compile(r"(?i)on\w+\s*="),
    re.compile(r"(?i)javascript:"),
    re.compile(r"(?i)<iframe[^>]*>"),
    re.compile(r"(?i)<img[^>]*onerror\s*="),
    re.compile(r"(?i)expression\s*\("),
]

# Safe GET parameter names that should not be validated for SQLi/XSS
SAFE_GET_PARAMS = {'query', 'q', 'search', 'page', 'sort', 'order', 'category', 'brand', 'min_price', 'max_price'}

# ---------- Helper functions ----------
def _load_rules():
    """Load active validation rules from DB into memory (cached on g)."""
    if not hasattr(g, 'validation_rules'):
        rules = ValidationRule.query.filter_by(active=True).all()
        g.validation_rules = rules
    return g.validation_rules

def _check_patterns(value, patterns):
    for pat in patterns:
        if pat.search(value):
            return pat.pattern
    return None

def _validate_type(value, expected_type):
    try:
        if expected_type == 'int':
            int(value)
        elif expected_type == 'float':
            float(value)
        elif expected_type == 'email':
            # simple email regex
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                return False
        elif expected_type == 'alpha':
            if not value.isalpha():
                return False
        elif expected_type == 'alphanum':
            if not value.isalnum():
                return False
        return True
    except Exception:
        return False

def _check_length(value, min_len, max_len):
    l = len(value)
    return (min_len is None or l >= min_len) and (max_len is None or l <= max_len)

def _sanitize(value):
    """Basic sanitization: HTML escape and strip control chars."""
    # Remove null bytes
    value = value.replace('\x00', '')
    # HTML escape
    return html.escape(value)

def _log_blocked(ip, page, payload, attack_type, reason):
    blocked = BlockedRequest(
        ip_address=ip,
        page=page,
        payload=payload,
        attack_type=attack_type,
        reason=reason,
        timestamp=datetime.utcnow()
    )
    db.session.add(blocked)
    # also log in RequestLog
    reqlog = RequestLog(ip_address=ip, page=page, blocked=True, attack_type=attack_type, timestamp=datetime.utcnow())
    db.session.add(reqlog)
    db.session.commit()
    # Alert if same IP > 5 blocks in last hour
    from datetime import timedelta
    window = current_app.config.get('ALERT_WINDOW', 3600)
    recent = BlockedRequest.query.filter(
        BlockedRequest.ip_address == ip,
        BlockedRequest.timestamp >= datetime.utcnow() - timedelta(seconds=window)
    ).count()
    if recent >= current_app.config.get('ALERT_THRESHOLD', 5):
        # In real app, send email/webhook; here just log
        current_app.logger.warning(f"ALERT: IP {ip} exceeded block threshold ({recent})")

def _log_clean(ip, page, attack_type=None):
    """Log a clean request to RequestLog."""
    reqlog = RequestLog(ip_address=ip, page=page, blocked=False, attack_type=attack_type, timestamp=datetime.utcnow())
    db.session.add(reqlog)
    db.session.commit()

# ---------- Middleware ----------
def security_gateway():
    """Flask before_request handler."""
    # Skip static files and admin assets
    if request.path.startswith('/static') or request.path.startswith('/admin/static'):
        return None

    ip = request.remote_addr or 'unknown'
    page = request.path
    data_sources = []

    # Collect all input values - only validate POST/PUT/PATCH and form submissions
    # For GET requests, only validate if there are form/json data (not just query params)
    if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
        if request.form:
            data_sources.append(('form', request.form))
        if request.is_json:
            data_sources.append(('json', request.get_json(silent=True) or {}))
        if request.args:
            data_sources.append(('args', request.args))
    elif request.method == 'GET':
        # For GET, only validate form/json data (not query params which are often safe like search)
        # But still collect args for logging purposes
        if request.form:
            data_sources.append(('form', request.form))
        if request.is_json:
            data_sources.append(('json', request.get_json(silent=True) or {}))

    # If no data sources to validate, just log clean request and continue
    if not data_sources:
        _log_clean(ip, page)
        return None

    for source_name, source in data_sources:
        if not source:
            continue
        for key, raw_value in source.items():
            # Ensure we work with string
            if isinstance(raw_value, (list, tuple)):
                values = [str(v) for v in raw_value]
            else:
                values = [str(raw_value)]

            for value in values:
                # ---- SQL Injection detection ----
                # Skip for known safe GET parameters
                if request.method == 'GET' and key in SAFE_GET_PARAMS:
                    continue
                match = _check_patterns(value, SQLI_PATTERNS)
                if match:
                    _log_blocked(ip, page, value, 'SQL Injection', f'Matched pattern {match}')
                    return _block_response('SQL Injection attempt detected.')

                # ---- XSS detection ----
                # Skip for known safe GET parameters
                if request.method == 'GET' and key in SAFE_GET_PARAMS:
                    continue
                match = _check_patterns(value, XSS_PATTERNS)
                if match:
                    _log_blocked(ip, page, value, 'XSS', f'Matched pattern {match}')
                    return _block_response('Cross-site scripting attempt detected.')

                # ---- Validation rules from DB ----
                for rule in _load_rules():
                    # Apply only if rule.field matches key or '*'
                    if rule.field != '*' and rule.field != key:
                        continue
                    # whitelist
                    if rule.rule_type == 'whitelist':
                        allowed = [v.strip() for v in rule.pattern.split(',')]
                        if value not in allowed:
                            _log_blocked(ip, page, value, 'Whitelist Violation', f'Value not in whitelist for {key}')
                            return _block_response('Input not allowed.')
                    # blacklist (regex)
                    elif rule.rule_type == 'blacklist':
                        try:
                            pat = re.compile(rule.pattern)
                            if pat.search(value):
                                _log_blocked(ip, page, value, 'Blacklist Violation', f'Matched blacklist pattern {rule.pattern}')
                                return _block_response('Input contains forbidden pattern.')
                        except re.error:
                            pass
                    # datatype
                    elif rule.rule_type == 'datatype':
                        if not _validate_type(value, rule.pattern):
                            _log_blocked(ip, page, value, 'Data-type Violation', f'Expected {rule.pattern}')
                            return _block_response('Invalid data type.')
                    # length
                    elif rule.rule_type == 'length':
                        try:
                            min_len, max_len = map(lambda x: int(x) if x else None, rule.pattern.split(','))
                        except Exception:
                            min_len, max_len = None, None
                        if not _check_length(value, min_len, max_len):
                            _log_blocked(ip, page, value, 'Length Violation', f'Length out of bounds {rule.pattern}')
                            return _block_response('Input length invalid.')

    # All checks passed – log clean request, sanitize and attach cleaned data to g for downstream use
    _log_clean(ip, page)

    cleaned = {}
    for source_name, source in data_sources:
        if not source:
            continue
        for key, raw_value in source.items():
            if isinstance(raw_value, (list, tuple)):
                cleaned[key] = [_sanitize(str(v)) for v in raw_value]
            else:
                cleaned[key] = _sanitize(str(raw_value))
    g.cleaned_input = cleaned
    return None

def _block_response(message):
    from flask import abort, jsonify
    # For API calls return JSON, else render simple page
    if request.is_json or request.headers.get('Accept','').startswith('application/json'):
        return jsonify(error=message), 400
    return f"<h3>Request blocked</h3><p>{message}</p>", 400