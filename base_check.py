with open('app/templates/base.html', 'r') as f:
    content = f.read()

print("=== BASE TEMPLATE ANALYSIS ===\n")
print(f"Total length: {len(content)} chars\n")

# Check for common layout issues
checks = {
    'bootstrap grid row': 'row' in content.lower(),
    'bootstrap grid col': 'col' in content.lower(),
    'footer': 'footer' in content.lower(),
    'charset': '<!doctype' in content.lower() or '<html>' in content.lower(),
    'meta viewport': 'viewport' in content.lower(),
    'bootstrap css link': 'bootstrap' in content.lower(),
    'custom css': 'style.css' in content,
    'body tag': '<body>' in content,
}

for check_name, result in checks.items():
    symbol = 'OK' if result else 'MISSING'
    print(f"  {check_name}: {symbol}")

# Find all style links
import re
style_links = re.findall(r'style=["\'][^"\']*["\']', content)
print(f"\n  style attributes found: {len(style_links)}")

# Find css links
css_links = re.findall(r'href=["\']([^"]*style[^"]*)["\']', content)
print(f"\n  CSS links: {css_links}")

# Find js links
js_links = re.findall(r'src=["\']([^"]*main[^"]*)["\']', content)
print(f"\n  JS links: {js_links}")

# Check for display:none
if 'display: none' in content.lower():
    print("\n  WARNING: 'display: none' found in base.html")
    # Show where
    for i, line in enumerate(content.split('\n'), 1):
        if 'display: none' in line.lower():
            print(f"    Line {i}: {line[:100]}...")
else:
    print("\n  OK: No 'display: none' in base.html")

# Check for height:0
if 'height: 0' in content.lower():
    print("  WARNING: 'height: 0' found in base.html")
else:
    print("  OK: No height:0 in base.html")

# Check for overflow:hidden
if 'overflow:hidden' in content.lower():
    print("  WARNING: 'overflow:hidden' found in base.html")
else:
    print("  OK: No overflow:hidden in base.html")