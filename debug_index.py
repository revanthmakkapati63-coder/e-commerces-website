from app import create_app
from app.models import Product
app = create_app()

# Read index.html to see how products are rendered
with open('app/templates/index.html', 'r') as f:
    index_html = f.read()

print("=== index.html product image sections ===")
# Find product card related sections
import re
# Find img tags
img_matches = re.findall(r'<img[^>]+>', index_html)
for i, m in enumerate(img_matches):
    print(f"Image tag {i+1}: {m[:150]}...")

print(f"\nTotal img tags in index.html: {len(img_matches)}")

# Check for product-card-img class
if 'product-card-img' in index_html:
    print("product-card-img class found in index.html")
else:
    print("product-card-img class NOT found in index.html")

# Check for card-img-top class
if 'card-img-top' in index_html:
    print("card-img-top class found in index.html")
else:
    print("card-img-top class NOT found in index.html")

# Check for product-img-fallback
if 'product-img-fallback' in index_html:
    print("product-img-fallback class found in index.html")
else:
    print("product-img-fallback class NOT found in index.html")

# Check for any display:none or opacity on images
if 'display: none' in index_html.lower():
    print("WARNING: Found 'display: none' in index.html")
else:
    print("No 'display: none' in index.html")

if 'opacity:' in index_html.lower():
    for line_num, line in enumerate(index_html.split('\n'), 1):
        if 'opacity:' in line.lower():
            print(f"Line {line_num}: {line.strip()}")
else:
    print("No opacity rules in index.html")