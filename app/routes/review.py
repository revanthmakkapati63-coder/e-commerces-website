from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Review
from app.forms import ReviewForm

bp = Blueprint('review', __name__)

@bp.route('/product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    existing = Review.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if existing:
        flash('You have already reviewed this product.')
        return redirect(url_for('main.product_detail', product_id=product.id))
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(user_id=current_user.id, product_id=product.id,
                        rating=form.rating.data, comment=form.comment.data)
        db.session.add(review)
        db.session.commit()
        flash('Thank you for your review!')
        return redirect(url_for('main.product_detail', product_id=product.id))
    return render_template('review.html', title='Write Review', form=form, product=product)

@bp.route('/product/<int:product_id>/reviews')
def product_reviews(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
    return render_template('product_reviews.html', title=f'Reviews for {product.name}', product=product, reviews=reviews)