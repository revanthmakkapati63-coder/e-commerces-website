from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Config defaults for alerting
    app.config.setdefault('ALERT_WINDOW', 3600)      # 1 hour
    app.config.setdefault('ALERT_THRESHOLD', 5)      # blocks per window

    db.init_app(app)
    login_manager.init_app(app)

    # ----- Security gateway (runs before every request) -----
    from app.security.gateway import security_gateway
    app.before_request(security_gateway)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.cart import bp as cart_bp
    app.register_blueprint(cart_bp, url_prefix='/cart')

    from app.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp, url_prefix='/profile')

    from app.routes.review import bp as review_bp
    app.register_blueprint(review_bp, url_prefix='/review')

    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app

from app import models  # noqa: F401