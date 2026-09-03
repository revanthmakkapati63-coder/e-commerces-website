from flask import Flask, request, render_template, redirect, url_for, g, abort
from gateway.interceptor import before_request
from gateway.validator import validate_request
from gateway.sanitizer import clean_input
from database.db import init_db, get_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
init_db()

@app.before_request
def wrapper():
    before_request()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ok, errors = validate_request()
        if ok:
            return redirect(url_for('index'))
        else:
            return "Invalid input", 400
    return render_template('login.html')

@app.route('/search')
def search():
    return "Search page"

@app.route('/cart')
def cart():
    return "Cart page"

@app.route('/checkout')
def checkout():
    return "Checkout page"

@app.route('/review')
def review():
    return "Review page"

@app.route('/admin')
def admin():
    db = get_db()
    total = db.execute("SELECT COUNT(*) as cnt FROM blocked_requests").fetchone()['cnt']
    blocked = db.execute("SELECT COUNT(*) as cnt FROM blocked_requests").fetchone()['cnt']
    cur = db.execute("SELECT attack_type, COUNT(*) as cnt FROM blocked_requests GROUP BY attack_type").fetchall()
    attacks = {row['attack_type']: row['cnt'] for row in cur}
    return render_template('admin_dashboard.html', total=total, blocked=blocked, attacks=attacks)

@app.route('/monitor')
def monitor():
    db = get_db()
    rows = db.execute("SELECT ip_address, page_name, user_input, attack_type, timestamp FROM blocked_requests ORDER BY timestamp DESC LIMIT 50").fetchall()
    return render_template('live_monitor.html', rows=rows)

@app.route('/rules')
def rules():
    db = get_db()
    rules = db.execute("SELECT id, rule_name, pattern, status FROM validation_rules").fetchall()
    return render_template('rules_panel.html', rules=rules)

if __name__ == '__main__':
    app.run(debug=True)