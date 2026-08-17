from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, PasswordField, TextAreaField, DecimalField, IntegerField,
    SelectField, DateField, SubmitField, BooleanField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


# ---------- Auth ----------

class AdminRegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class UserRegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[Optional(), Length(max=30)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')


class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=150)])
    phone = StringField('Phone', validators=[Optional(), Length(max=30)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Update Profile')


# ---------- Admin: Catalog management ----------

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    submit = SubmitField('Save Category')


class DestinationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=150)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    image = FileField('Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    submit = SubmitField('Save Destination')


class TourForm(FlaskForm):
    title = StringField('Tour Title', validators=[DataRequired(), Length(max=200)])
    image = FileField('Tour Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])
    destination_id = SelectField('Destination', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    duration = StringField('Duration', validators=[Optional(), Length(max=80)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    discount = DecimalField('Discount (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=0)
    max_guests = IntegerField('Max Guests', validators=[DataRequired(), NumberRange(min=1)])
    available_seats = IntegerField('Available Seats', validators=[DataRequired(), NumberRange(min=0)])
    start_date = DateField('Tour Start Date', validators=[Optional()])
    end_date = DateField('Tour End Date', validators=[Optional()])
    included_services = TextAreaField('Included Services', validators=[Optional()])
    excluded_services = TextAreaField('Excluded Services', validators=[Optional()])
    hotel = StringField('Hotel Name', validators=[Optional(), Length(max=150)])
    transport = StringField('Transportation', validators=[Optional(), Length(max=150)])
    rating = DecimalField('Rating', validators=[Optional(), NumberRange(min=0, max=5)], default=0)
    status = SelectField('Status', choices=[('Available', 'Available'), ('Sold Out', 'Sold Out')])
    submit = SubmitField('Save Tour')


class BookingActionForm(FlaskForm):
    """Tiny CSRF-protected form used for the confirm/cancel/complete buttons."""
    submit = SubmitField('Update')


class BookTourForm(FlaskForm):
    persons = IntegerField('Number of Persons', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Confirm Booking')
