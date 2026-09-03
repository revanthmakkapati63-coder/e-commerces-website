with open('app/templates/cart.html', 'r') as f:
    content = f.read()

print("=== CART TEMPLATE ANALYSIS ===\n")
print(f"Total length: {len(content)} chars\n")

# Check for common issues
checks = {
    'cart table': 'table' in content.lower(),
    'cart items': 'item' in content.lower() or 'product' in content.lower(),
    'checkout button': 'checkout' in content.lower() or 'btn-primary' in content,
    'form': 'form' in content,
    'class': 'class=' in content,
}

for check_name, result in checks.items():
    symbol = 'OK' if result else 'MISSING'
    print(f"  {check_name}: {symbol}")

# Find all img tags
import re
img_tags = re.findall(r'<img[^>]+>', content)
print(f"\n  Image tags in cart: {len(img_tags)}")
for i, img in enumerate(img_tags):
    print(f"    {img[:80]}...")

# Find all table tags
table_tags = re.findall(r'<table[^>]*>', content)
print(f"\n  Table tags in cart: {len(table_tags)}")
for i, table in enumerate(table_tags):
    print(f"    {table[:80]}...")

# Check for display:none
if 'display: none' in content.lower():
    print("\n  WARNING: 'display: none' found in cart.html")
else:
    print("\n  OK: No 'display: none' in cart.html")

# Check for height:0
if 'height: 0' in content.lower() and 'height:0' not in content.lower():
    print("  WARNING: 'height: 0' found")
elif 'height:0' in content.lower():
    print("  WARNING: 'height:0' found")
else:
    print("  OK: No height:0 issues")