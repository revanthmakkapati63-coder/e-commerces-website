import os
from app import create_app

app = create_app()

# Check CSS for hiding rules
css_path = 'app/static/css/style.css'
with open(css_path, 'r') as f:
    css = f.read()

print("=== CSS ANALYSIS ===\n")

# Check for common hiding patterns
hiding_patterns = [
    ('display: none', 'display none'),
    ('visibility: hidden', 'visibility hidden'),
    ('opacity: 0', 'opacity 0'),
    ('height: 0', 'height 0'),
    ('padding: 0', 'padding 0'),
    ('margin: 0', 'margin 0'),
]

print("Checking for content-hiding CSS rules:")
for pattern, name in hiding_patterns:
    if pattern in css:
        count = css.lower().count(pattern.lower())
        print(f"  WARNING '{name}' found {count} time(s) in CSS")
    else:
        print(f"  OK '{name}' not found")

# Specifically check .card, .card-img-top, .product-card
print("\nKey component rules:")
import re

# .card-img-top
if '.card-img-top' in css:
    match = re.search(r'\.card-img-top\s*\{[^}]*\}', css)
    if match:
        print(f"  .card-img-top: {match.group()[:150]}...")

# .product-card
if '.product-card' in css:
    match = re.search(r'\.product-card\s*\{[^}]*\}', css)
    if match:
        print(f"  .product-card: {match.group()[:150]}...")

# .card
if '.card' in css:
    match = re.search(r'\.card\s*\{[^}]*\}', css)
    if match:
        print(f"  .card: {match.group()[:150]}...")

# Check for !important opacity
if 'opacity' in css:
    for line in css.split('\n'):
        if 'opacity' in line.lower():
            print(f"  opacity line: {line.strip()}")