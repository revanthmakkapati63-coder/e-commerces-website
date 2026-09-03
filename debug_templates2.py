from app import create_app
app = create_app()

# Check which templates include _macros.html
import os

templates_dir = 'app/templates'
print("=== Templates in app/templates ===")
for f in os.listdir(templates_dir):
    if f.endswith('.html'):
        print(f"  {f}")

# Check _macros.html usage
with open('app/templates/_macros.html', 'r') as f:
    macros = f.read()

print(f"\n=== _macros.html content ===")
print(f"Has product-image-url check: {'product.image_url' in macros}")
print(f"Has card-img-top: {'card-img-top' in macros}")
print(f"Has product-img-fallback: {'product-img-fallback' in macros}")
print(f"Has img src: {'src=' in macros}")

# Check product_detail.html
with open('app/templates/product_detail.html', 'r') as f:
    detail = f.read()

print(f"\n=== product_detail.html ===")
print(f"Has product-image-url check: {'product.image_url' in detail}")
print(f"Has card-img-top: {'card-img-top' in detail}")
print(f"Has product-img-fallback: {'product-img-fallback' in detail}")
print(f"Has img src: {'src=' in detail}")

# Check search.html
try:
    with open('app/templates/search.html', 'r') as f:
        search = f.read()
    print(f"\n=== search.html ===")
    print(f"Has product-image-url check: {'product.image_url' in search}")
    print(f"Has card-img-top: {'card-img-top' in search}")
    print(f"Has product-img-fallback: {'product-img-fallback' in search}")
except FileNotFoundError:
    print("\nsearch.html not found or error reading")

# Check cart.html
try:
    with open('app/templates/cart.html', 'r') as f:
        cart = f.read()
    print(f"\n=== cart.html ===")
    print(f"Has card-img-top: {'card-img-top' in cart}")
except FileNotFoundError:
    print("\ncart.html not found or error reading")