# E-Commerce Web Application (OWASP Top 10 Security)

A full-stack secure E-Commerce web application built with Python (Flask) and SQLite, designed to demonstrate, test, and defend against the OWASP Top 10 Web Vulnerabilities.

---

## 🛡️ Key Features & Security Architecture

- **Authentication & Authorization:** Secure session management with Werkzeug password hashing (PBKDF2/SHA-256) and role-based access control (Admin vs Customer).
- **SQL Injection Defense:** Parameterized queries via SQLAlchemy ORM and custom WAF validation blocking UNION-based attacks.
- **Dynamic Validation Engine:** Database-driven input validation rules (Regex patterns, length limits, tag filtering).
- **Product Catalog & Cart Management:** Complete shopping cart, checkout workflow, and product inventory tracking.
- **Automated Security Test Suite:** Dedicated test scripts verifying endpoint authorization and input sanitization.

---

## 🚀 Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/e-commerces-website.git
   cd e-commerces-website
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```
   Open `http://127.0.0.1:5000/` in your browser.

---

## 🧪 Running Security Tests

```bash
python test_security.py
python test_routes.py
```
