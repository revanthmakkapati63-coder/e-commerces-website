from app import create_app, db
from app.models import User, Product, Cart, Order, Review, ValidationRule
from werkzeug.security import generate_password_hash

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'Cart': Cart, 'Order': Order, 'Review': Review,
            'ValidationRule': ValidationRule}

def _init_default_data():
    # create default admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
    # default validation rules
    defaults = [
        # whitelist rule disabled by default to avoid blocking all inputs
        ('Whitelist: safe fields', '*', 'whitelist', '', False),
        ('Blacklist: script tags', '*', 'blacklist', r'(?i)<script[^>]*>.*?</script>'),
        ('Datatype: email', 'email', 'datatype', 'email'),
        ('Length: username 2-64', 'username', 'length', '2,64'),
    ]
    for item in defaults:
        if len(item) == 5:
            name, field, rtype, pattern, active = item
        else:
            name, field, rtype, pattern = item
            active = True
        if not ValidationRule.query.filter_by(name=name).first():
            db.session.add(ValidationRule(name=name, field=field, rule_type=rtype, pattern=pattern, active=active))
    # seed sample products if none exist
    if Product.query.count() == 0:
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        _init_default_data()
    app.run(debug=True)