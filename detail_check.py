with open('app/templates/product_detail.html', 'r') as f:
    content = f.read()

print("=== PRODUCT DETAIL TEMPLATE ANALYSIS ===\n")
print(f"Total length: {len(content)} chars\n")

# Check for common issues
checks = {
    'product image': 'img src=' in content,
    'product name': 'name' in content.lower(),
    'product price': 'price' in content.lower(),
    'stock': 'stock' in content.lower(),
    'reviews': 'review' in content.lower(),
    'add to cart': 'cart' in content.lower() or 'add' in content.lower(),
    'form': 'form' in content,
    'row layout': 'row' in content.lower(),
    'column': 'col' in content.lower(),
}

for check_name, result in checks.items():
    symbol = 'OK' if result else 'MISSING'
    print(f"  {check_name}: {symbol}")

# Find all img tags
import re
img_tags = re.findall(r'<img[^>]+>', content)
print(f"\n  Image tags in product_detail: {len(img_tags)}")
for i, img in enumerate(img_tags):
    src_match = re.search(r'src="([^"]+)"', img)
    alt_match = re.search(r'alt="([^"]*)"', img)
    src = src_match.group(1) if src_match else 'No src'
    alt = alt_match.group(1) if alt_match else 'No alt'
    print(f"    {img[:80]}... src={src[:50]} alt={alt[:30]}")

# Check for display:none
if 'display: none' in content.lower():
    print("\n  WARNING: 'display: none' found in product_detail.html")
else:
    print("\n  OK: No 'display: none' in product_detail.html")

# Check for height:0
if 'height: 0' in content.lower():
    print("  WARNING: 'height: 0' found in product_detail.html")
else:
    print("  OK: No height:0 in product_detail.html")

# Check layout columns
print("\n  Layout structure:")
# Find col-md-6 or similar
import re
col_matches = re.findall(r'col-md-\d+', content)
print(f"  Column classes found: {col_matches}")

# Find rows
row_matches = re.findall(r'row', content.lower())
print(f"  'row' occurrences: {len(row_matches)}")