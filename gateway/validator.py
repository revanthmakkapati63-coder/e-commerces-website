import re

WHITELIST = {
    'username': r'^[A-Za-z0-9_]{3,30}$',
    'email': r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
    'price': r'^\d+(\.\d{0,2})?$',
    'quantity': r'^\d+$',
    'mobile': r'^\+?\d{10,15}$',
}

def validate_field(name, value):
    if len(value) > 200:
        return False, f"{name} too long"
    pattern = WHITELIST.get(name)
    if pattern and not re.fullmatch(pattern, str(value)):
        return False, f"{name} format invalid"
    return True, ""

def validate_request():
    errors = []
    for key, value in request.values.items():
        ok, msg = validate_field(key, value)
        if not ok:
            errors.append((key, msg))
    return len(errors) == 0, errors