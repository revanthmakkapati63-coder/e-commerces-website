from app import create_app
app = create_app()

with app.test_client() as c:
    print("=== ROUTE TESTING ===\n")
    
    # Test new routes
    print("New routes (FAQs, Terms, Privacy):")
    for route in ['/faqs', '/terms', '/privacy']:
        r = c.get(route)
        print(f"  {route}: HTTP {r.status_code} ({len(r.data)} bytes)")
    
    print("\nMain routes:")
    for route in ['/', '/index', '/search']:
        r = c.get(route)
        print(f"  {route}: HTTP {r.status_code}")
    
    print("\nCart route:")
    r = c.get('/cart')
    print(f"  /cart: HTTP {r.status_code}")
    
    # Test product detail
    from app.models import Product
    with app.app_context():
        product = Product.query.first()
        if product:
            print(f"\nProduct detail for: {product.name}")
            r = c.get(f'/product/{product.id}')
            print(f"  /product/{product.id}: HTTP {r.status_code}")