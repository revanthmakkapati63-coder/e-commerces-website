from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    products = Product.query.all()
    print(f"Total products: {len(products)}")
    for p in products:
        url = p.image_url or 'NO IMAGE URL'
        has_http = url and url.startswith('http')
        print(f"ID {p.id}: {p.name}")
        print(f"  image_url: {url}")
        print(f"  Starts with http: {has_http}")