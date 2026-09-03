from app import create_app
app = create_app()

with open('app/templates/base.html', 'r') as f:
    base = f.read()

print("=== base.html image-related checks ===")
import re

# Check for display:none on images
if 'display: none' in base.lower():
    print("WARNING: 'display: none' found in base.html")
    for i, line in enumerate(base.split('\n'), 1):
        if 'display: none' in line.lower():
            print(f"  Line {i}: {line.strip()}")

# Check for visibility:hidden
if 'visibility: hidden' in base.lower():
    print("WARNING: 'visibility: hidden' found in base.html")

# Check for opacity rules
if 'opacity:' in base.lower():
    for i, line in enumerate(base.split('\n'), 1):
        if 'opacity:' in line.lower():
            print(f"Line {i}: {line.strip()}")

# Check for max-height or height that might clip images
if 'max-height' in base.lower():
    print("Has max-height rules")

# Check for img tags
img_tags = re.findall(r'<img[^>]+>', base)
print(f"\nimg tags in base.html: {len(img_tags)}")
for i, img in enumerate(img_tags):
    print(f"  {img[:100]}")

# Check for any container with overflow:hidden that might clip
if 'overflow:hidden' in base.lower():
    print("WARNING: overflow:hidden found - might clip images")
    for i, line in enumerate(base.split('\n'), 1):
        if 'overflow:hidden' in line.lower():
            print(f"  Line {i}: {line.strip()}")