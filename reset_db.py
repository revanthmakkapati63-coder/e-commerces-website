from app import create_app, db
from app.models import Product

app = create_app()
with app.app_context():
    # Delete and recreate database
    import os
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)) if False else '.', 'instance', 'ecommerce.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        print('Deleted existing database')
    
    db.create_all()
    # Seed sample products with placeholder images
    sample_products = [
        Product(name='Gaming Laptop', description='15" high-performance gaming laptop with RTX graphics', price=1299.99, stock=5, image_url='https://via.placeholder.com/400x300/2874f0/ffffff?text=Gaming+Laptop', discount=10),
        Product(name='Wireless Headphones', description='Noise-cancelling Bluetooth headphones with 30hr battery', price=199.99, stock=20, image_url='https://via.placeholder.com/400x300/ff6f61/ffffff?text=Headphones', discount=15),
        Product(name='Smartphone', description='Latest flagship smartphone with 5G and pro camera', price=899.99, stock=10, image_url='https://via.placeholder.com/400x300/00bfa5/ffffff?text=Smartphone', discount=5),
        Product(name='Mechanical Keyboard', description='RGB mechanical keyboard with Cherry MX switches', price=129.99, stock=15, image_url='https://via.placeholder.com/400x300/ff9f00/ffffff?text=Keyboard', discount=0),
        Product(name='4K Monitor', description='27" 4K UHD monitor with HDR support', price=349.99, stock=8, image_url='https://via.placeholder.com/400x300/2874f0/ffffff?text=4K+Monitor', discount=12),
        Product(name='External SSD', description='1TB portable SSD with USB-C 10Gbps', price=159.99, stock=12, image_url='https://via.placeholder.com/400x300/ff6f61/ffffff?text=External+SSD', discount=8),
        Product(name='Webcam HD', description='1080p webcam with auto-focus and privacy cover', price=79.99, stock=25, image_url='https://via.placeholder.com/400x300/00bfa5/ffffff?text=Webcam', discount=0),
        Product(name='USB-C Hub', description='7-in-1 USB-C hub with HDMI, USB-A, SD card reader', price=49.99, stock=30, image_url='https://via.placeholder.com/400x300/ff9f00/ffffff?text=USB-C+Hub', discount=20),
    ]
    db.session.bulk_save_objects(sample_products)
    db.session.commit()
    print('Database reset and products seeded successfully')
    print('Product count:', Product.query.count())