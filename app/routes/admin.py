from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user, login_user, logout_user
from app import db
from app.models import BlockedRequest, ValidationRule, User, RequestLog
from app.forms import ValidationRuleForm
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            flash('Admin access required')
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return wrapper

# ----- Admin login -----
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'is_admin', False):
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password) and user.is_admin:
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials or not an admin')
    return render_template('admin/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

# ----- Dashboard -----
@bp.route('/')
@bp.route('/dashboard')
@admin_required
def dashboard():
    # Totals from RequestLog
    total_requests = RequestLog.query.count()
    clean_requests = RequestLog.query.filter_by(blocked=False).count()
    blocked_requests = RequestLog.query.filter_by(blocked=True).count()
    sql_inj = BlockedRequest.query.filter_by(attack_type='SQL Injection').count()
    xss = BlockedRequest.query.filter_by(attack_type='XSS').count()
    other = blocked_requests - sql_inj - xss

    recent = BlockedRequest.query.order_by(BlockedRequest.timestamp.desc()).limit(10).all()
    top_ips = db.session.query(
        BlockedRequest.ip_address,
        func.count(BlockedRequest.id).label('cnt')
    ).group_by(BlockedRequest.ip_address).order_by(func.count(BlockedRequest.id).desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                           total=total_requests,
                           clean=clean_requests,
                           blocked=blocked_requests,
                           sql_inj=sql_inj,
                           xss=xss,
                           other=other,
                           recent=recent,
                           top_ips=top_ips)

# ----- Live Attack Monitor -----
@bp.route('/monitor')
@admin_required
def monitor():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    attacks = BlockedRequest.query.order_by(BlockedRequest.timestamp.desc()).paginate(page=page, per_page=per_page)
    return render_template('admin/monitor.html', attacks=attacks)

# ----- Blocked Request Detail -----
@bp.route('/blocked/<int:req_id>')
@admin_required
def blocked_detail(req_id):
    br = BlockedRequest.query.get_or_404(req_id)
    return render_template('admin/blocked_detail.html', br=br)

# ----- Validation Rules Management -----
@bp.route('/rules', methods=['GET', 'POST'])
@admin_required
def rules():
    form = ValidationRuleForm()
    if form.validate_on_submit():
        rule = ValidationRule(
            name=form.name.data,
            field=form.field.data or '*',
            rule_type=form.rule_type.data,
            pattern=form.pattern.data,
            active=form.active.data
        )
        db.session.add(rule)
        db.session.commit()
        flash('Rule added')
        return redirect(url_for('admin.rules'))
    all_rules = ValidationRule.query.order_by(ValidationRule.created_at.desc()).all()
    return render_template('admin/rules.html', form=form, rules=all_rules)

@bp.route('/rules/<int:rule_id>/delete', methods=['POST'])
@admin_required
def delete_rule(rule_id):
    rule = ValidationRule.query.get_or_404(rule_id)
    db.session.delete(rule)
    db.session.commit()
    flash('Rule deleted')
    return redirect(url_for('admin.rules'))

# ----- API for charts (optional) -----
@bp.route('/api/stats')
@admin_required
def api_stats():
    # last 24h per hour
    since = datetime.utcnow() - timedelta(hours=24)
    data = db.session.query(
        func.strftime('%Y-%m-%d %H:00', BlockedRequest.timestamp).label('hour'),
        func.count(BlockedRequest.id)
    ).filter(BlockedRequest.timestamp >= since).group_by('hour').all()
    return jsonify({hour: cnt for hour, cnt in data})