from app import create_app, db
from app.models import Product
from urllib.parse import urlparse

app = create_app()
with app.app_context():
    p = Product.query.first()
    image_url = p.image_url
    
    # Simulate what _macros.html renders
    if p.image_url:
        img_html = f'<img src="{p.image_url}" class="card-img-top product-card-img" alt="{p.name}" loading="lazy">'
    else:
        img_html = f'<div class="card-img-top product-img-fallback" data-product-name="{p.name}" style="height:200px;">'
    
    print("=== Rendered HTML from _macros.html ===")
    print(img_html)
    print()
    
    # Check if the URL would work
    print("=== URL Analysis ===")
    parsed = urlparse(image_url)
    print(f"Protocol: {parsed.scheme}")
    print(f"Host: {parsed.netloc}")
    print(f"Path: {parsed.path}")
    print(f"Query: {parsed.query}")
    print()
    print(f"URL appears valid: {parsed.scheme in ['http', 'https']}")
    
    # Check product_detail template too
    print("=== product_detail.html rendering ===")
    if p.image_url:
        detail_img = f'<img src="{p.image_url}" class="img-fluid rounded product-card-img" alt="{p.name}">'
    else:
        detail_img = f'<div class="bg-light d-flex align-items-center justify-content-center rounded" style="height:400px;"><span class="product-img-fallback" data-product-name="{p.name}" style="width:100%; height:100%; color:#6c757d; pointer-events:none;">{p.name[0] if p.name else ""}</span></div>'
    print(detail_img)