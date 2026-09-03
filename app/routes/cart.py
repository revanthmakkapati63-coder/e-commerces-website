from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Cart, Product, Order, OrderItem
from app.forms import CheckoutForm

bp = Blueprint('cart', __name__)

@bp.route('/')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', title='Cart', cart_items=cart_items, total=total)

@bp.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    flash('Added to cart.')
    return redirect(url_for('cart.view_cart'))

@bp.route('/update/<int:cart_id>', methods=['POST'])
@login_required
def update_quantity(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('cart.view_cart'))
    action = request.form.get('action')
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
            flash('Item removed.')
            db.session.commit()
            return redirect(url_for('cart.view_cart'))
    db.session.commit()
    return redirect(url_for('cart.view_cart'))

@bp.route('/remove/<int:cart_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('cart.view_cart'))
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed.')
    return redirect(url_for('cart.view_cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.')
        return redirect(url_for('cart.view_cart'))
    total = sum(item.product.price * item.quantity for item in cart_items)
    if form.validate_on_submit():
        order = Order(user_id=current_user.id, total_amount=total, status='paid')
        db.session.add(order)
        db.session.flush()  # get order.id
        for ci in cart_items:
            oi = OrderItem(order_id=order.id, product_id=ci.product_id,
                           quantity=ci.quantity, price_at_purchase=ci.product.price)
            db.session.add(oi)
            db.session.delete(ci)
        db.session.commit()
        flash('Order placed successfully!')
        return redirect(url_for('profile.orders'))
    return render_template('checkout.html', title='Checkout', cart_items=cart_items, total=total, form=form)