from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product, Cart
from app.forms import ProductSearchForm, AddToCartForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=8)
    form = ProductSearchForm()
    return render_template('index.html', title='Home', products=products, form=form)

@bp.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    form = AddToCartForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please login to add items to cart.')
            return redirect(url_for('auth.login', next=request.url))
        cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product.id).first()
        if cart_item:
            cart_item.quantity += form.quantity.data
        else:
            cart_item = Cart(user_id=current_user.id, product_id=product.id, quantity=form.quantity.data)
            db.session.add(cart_item)
        db.session.commit()
        flash('Item added to cart.')
        return redirect(url_for('cart.view_cart'))
    return render_template('product_detail.html', title=product.name, product=product, form=form)

@bp.route('/search', methods=['GET', 'POST'])
def search():
    form = ProductSearchForm()
    query = ''
    products = None
    if form.validate_on_submit() or request.args.get('query'):
        query = form.query.data or request.args.get('query', '')
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return render_template('search.html', title='Search', form=form, query=query, products=products)

@bp.route('/faqs')
def faqs():
    return render_template('faqs.html', title='FAQs')

@bp.route('/terms')
def terms():
    return render_template('terms.html', title='Terms of Service')

@bp.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')