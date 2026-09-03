from flask import request, g, abort
from database.db import get_db
import re

def is_malicious(payload):
    s = str(payload)
    sqli_patterns = [
        r"\b(?:or|and)\s+['\"]?1['\"]?=\s*['\"]?",
        r"\b(?:union|select|insert|update|delete|drop|create|alter|exec)\b",
        r'--',
        r"/\*.*?\*/"
    ]
    xss_patterns = [
        r"<script.*?>",
        r"on\w+\s*=\s*["\']",
        r"javascript:",
        r"vbscript:",
        r"expression\s*\("
    ]
    for pat in sqli_patterns + xss_patterns:
        if re.search(pat, s, re.IGNORECASE):
            return True
    return False

def before_request():
    # Validate all incoming values
    ok, errors = validate_request()
    if not ok:
        abort(400)
    # Sanitize and store cleaned values
    cleaned = {}
    for key, value in request.values.items():
        cleaned[key] = clean_input(value)
        g.cleaned_values = cleaned
    # Check raw values for malicious patterns
    for key, value in request.values.items():
        if is_malicious(value):
            ip = request.remote_addr
            page = request.path
            attack_type = "SQLi" if any(re.search(p, str(value), re.IGNORECASE) for p in sqli_patterns) else "XSS"
            db = get_db()
            db.execute(
                "INSERT INTO blocked_requests (ip_address, page_name, user_input, attack_type, timestamp) VALUES (?, ?, ?, ?, datetime('now'))",
                (ip, page, value, attack_type)
            )
            db.commit()
            abort(400)