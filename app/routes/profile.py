from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Order
from app.forms import ProfileForm

bp = Blueprint('profile', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Profile updated.')
        return redirect(url_for('profile.profile'))
    return render_template('profile.html', title='Profile', form=form)

@bp.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', title='My Orders', orders=user_orders)

@bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Unauthorized.')
        return redirect(url_for('profile.orders'))
    return render_template('order_detail.html', title=f'Order {order.id}', order=order)