from app import create_app

app = create_app()
with app.test_client() as client:
    # Test SQL injection via POST should still be blocked
    r = client.post('/search', data={'query': 'union select * from users'})
    print('SQLi POST status:', r.status_code)
    print('SQLi POST blocked:', r.status_code == 400 or 'blocked' in r.text.lower())
    
    # Test XSS via POST should still be blocked
    r = client.post('/auth/login', data={'email': 'test@test.com', 'password': '<script>alert(1)</script>'})
    print('XSS POST status:', r.status_code)
    print('XSS POST blocked:', r.status_code == 400 or 'blocked' in r.text.lower())