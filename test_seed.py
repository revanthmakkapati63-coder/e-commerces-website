from app import create_app, db
from app.models import Product, User

app = create_app()
with app.app_context():
    # Check current state
    print('Product count:', Product.query.count())
    print('User count:', User.query.count())
    print('Admin user:', User.query.filter_by(is_admin=True).first())
    
    # Seed products manually if none exist
    if Product.query.count() == 0:
        sample_products = [
            Product(name='Gaming Laptop', description='15" high-performance gaming laptop with RTX graphics', price=1299.99, stock=5, image_url='https://via.placeholder.com/400x300/2874f0/ffffff?text=Gaming+Laptop', discount=10),
            Product(name='Wireless Headphones', description='Noise-cancelling Bluetooth headphones with 30hr battery', price=199.99, stock=20, image_url='https://via.placeholder.com/400x300/ff6f61/ffffff?text=Headphones', discount=15),
            Product(name='Smartphone', description='Latest flagship smartphone with 5G and pro camera', price=899.99, stock=10, image_url='https://via.placeholder.com/400x300/00bfa5/ffffff?text=Smartphone', discount=5),
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()
        print('Products seeded successfully')
    else:
        print('Products already exist, count:', Product.query.count())