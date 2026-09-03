with open('app/templates/index.html', 'r') as f:
    content = f.read()

print("=== INDEX TEMPLATE ANALYSIS ===\n")
print(f"Total length: {len(content)} chars\n")

# Check for common issues
checks = {
    'hero carousel': 'carousel' in content.lower(),
    'product grid': 'product' in content.lower() or 'card' in content.lower(),
    'row': 'row' in content.lower(),
    'col': 'col' in content.lower(),
    'card': 'card' in content.lower(),
    'image': 'src=' in content,
    'button': 'button' in content.lower() or 'btn' in content,
}

for check_name, result in checks.items():
    symbol = 'OK' if result else 'MISSING'
    print(f"  {check_name}: {symbol}")

# Find all img tags
import re
img_tags = re.findall(r'<img[^>]+>', content)
print(f"\n  Image tags in index: {len(img_tags)}")
for i, img in enumerate(img_tags):
    # Show src and class
    src_match = re.search(r'src="([^"]+)"', img)
    class_match = re.search(r'class="([^"]*)"', img)
    src = src_match.group(1) if src_match else 'No src'
    cls = class_match.group(1) if class_match else 'No class'
    print(f"    {img[:80]}... src={src[:50]} cls={cls[:30]}")

# Check for display:none
if 'display: none' in content.lower():
    print("\n  WARNING: 'display: none' found in index.html")
else:
    print("\n  OK: No 'display: none' in index.html")

# Check for height:0
if 'height: 0' in content.lower():
    print("  WARNING: 'height: 0' found in index.html")
else:
    print("  OK: No height:0 in index.html")

# Check for overflow:hidden
if 'overflow:hidden' in content.lower():
    print("  WARNING: 'overflow:hidden' found in index.html")
else:
    print("  OK: No overflow:hidden in index.html")