import os
from app import create_app

app = create_app()

print("=== WEBSITE STATUS CHECK ===\n")

# 1. Check templates
print("1. TEMPLATES:")
templates_dir = 'app/templates'
if os.path.exists(templates_dir):
    for f in sorted(os.listdir(templates_dir)):
        if f.endswith('.html'):
            path = os.path.join(templates_dir, f)
            size = os.path.getsize(path)
            print(f"   OK {f} ({size} bytes)")
else:
    print("   MISSING templates directory")

# 2. Check CSS
print("\n2. CSS:")
css_dir = 'app/static/css'
if os.path.exists(css_dir):
    css_files = [f for f in os.listdir(css_dir) if f.endswith('.css')]
    print(f"   OK CSS directory exists ({len(css_files)} files)")
    for cf in css_files:
        print(f"      - {cf}")
else:
    print("   MISSING CSS directory")

# 3. Check Flask routes
print("\n3. FLASK ROUTES:")
rules = sorted([str(r) for r in app.url_map.iter_rules()])
print(f"   OK {len(rules)} routes registered")
for r in rules[:10]:
    print(f"      {r}")

# 4. Check product model
print("\n4. PRODUCT MODEL:")
from app.models import Product
with app.app_context():
    products = Product.query.all()
    print(f"   OK Products in DB: {len(products)}")
    for p in products[:3]:
        url = str(p.image_url)[:50] if p.image_url else 'None'
        print(f"      - {p.id}: {p.name} | image_url: {url}")

# 5. Quick template content check
print("\n5. KEY TEMPLATE CHECKS:")
template_files = ['_macros.html', 'product_detail.html', 'index.html', 'base.html']
for tf in template_files:
    path = os.path.join(templates_dir, tf)
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
        has_img = 'img src=' in content
        has_card = 'card-img-top' in content
        print(f"   OK {tf}: has images={has_img}, card-img-top={has_card}")
    else:
        print(f"   MISSING {tf}")