from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValueError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValueError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[Optional(), Length(max=64)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=64)])
    address = StringField('Address', validators=[Optional(), Length(max=256)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Update Profile')

class ProductSearchForm(FlaskForm):
    query = StringField('Search', validators=[Optional(), Length(max=128)])
    submit = SubmitField('Search')

class AddToCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Add to Cart')

class CheckoutForm(FlaskForm):
    # Could add shipping address fields, but reuse profile info
    submit = SubmitField('Place Order')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(i, str(i)) for i in range(1,6)], validators=[DataRequired()], coerce=int)
    comment = TextAreaField('Comment', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Submit Review')

class ValidationRuleForm(FlaskForm):
    name = StringField('Rule Name', validators=[DataRequired(), Length(max=100)])
    field = StringField('Field ( * for all )', validators=[Optional(), Length(max=100)])
    rule_type = SelectField('Type', choices=[
        ('whitelist', 'Whitelist (comma separated)'),
        ('blacklist', 'Blacklist (regex)'),
        ('datatype', 'Data type (int, float, email, alpha, alphanum)'),
        ('length', 'Length (min,max)')
    ], validators=[DataRequired()])
    pattern = TextAreaField('Pattern / Values', validators=[DataRequired()])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Save Rule')