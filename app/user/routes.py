from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db
from app.decorators import user_required
from app.models import Tour, Category, Destination, Booking
from app.forms import ProfileForm, BookTourForm

user_bp = Blueprint('user', __name__)


@user_bp.route('/dashboard')
@login_required
@user_required
def dashboard():
    recent_bookings = Booking.query.filter_by(user_id=current_user.id).order_by(
        Booking.booking_date.desc()
    ).limit(5).all()
    return render_template('user/dashboard.html', recent_bookings=recent_bookings)


@user_bp.route('/tours')
@login_required
@user_required
def tours():
    query = Tour.query

    destination_id = request.args.get('destination_id', type=int)
    category_id = request.args.get('category_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    q = request.args.get('q', '').strip()

    if destination_id:
        query = query.filter_by(destination_id=destination_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if min_price is not None:
        query = query.filter(Tour.price >= min_price)
    if max_price is not None:
        query = query.filter(Tour.price <= max_price)
    if q:
        query = query.filter(Tour.title.ilike(f"%{q}%"))

    items = query.order_by(Tour.created_at.desc()).all()
    categories = Category.query.order_by(Category.name).all()
    destinations = Destination.query.order_by(Destination.name).all()

    return render_template(
        'user/tours.html',
        tours=items,
        categories=categories,
        destinations=destinations,
        filters=request.args,
    )


@user_bp.route('/tours/<int:tour_id>')
@login_required
@user_required
def tour_detail(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = BookTourForm()
    return render_template('user/tour_detail.html', tour=tour, form=form)


@user_bp.route('/tours/<int:tour_id>/book', methods=['POST'])
@login_required
@user_required
def book_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = BookTourForm()

    if tour.status != 'Available':
        flash('This tour is sold out and cannot be booked.', 'danger')
        return redirect(url_for('user.tour_detail', tour_id=tour.id))

    if form.validate_on_submit():
        persons = form.persons.data
        if persons > tour.available_seats:
            flash(f'Only {tour.available_seats} seat(s) left for this tour.', 'danger')
            return redirect(url_for('user.tour_detail', tour_id=tour.id))
        if persons > tour.max_guests:
            flash(f'This tour allows a maximum of {tour.max_guests} guest(s) per booking.', 'danger')
            return redirect(url_for('user.tour_detail', tour_id=tour.id))

        total_price = round(tour.discounted_price * persons, 2)
        booking = Booking(
            user_id=current_user.id,
            tour_id=tour.id,
            persons=persons,
            total_price=total_price,
            booking_status='Pending',
        )
        tour.available_seats -= persons
        if tour.available_seats <= 0:
            tour.status = 'Sold Out'

        db.session.add(booking)
        db.session.commit()
        flash('Booking submitted! It is now pending admin confirmation.', 'success')
        return redirect(url_for('user.my_bookings'))

    flash('Please enter a valid number of persons.', 'danger')
    return redirect(url_for('user.tour_detail', tour_id=tour.id))


@user_bp.route('/bookings')
@login_required
@user_required
def my_bookings():
    items = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('user/my_bookings.html', bookings=items)


@user_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
@user_required
def cancel_booking(booking_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first_or_404()
    if booking.booking_status != 'Pending':
        flash('Only pending bookings can be cancelled by you. Confirmed bookings require admin action.', 'warning')
        return redirect(url_for('user.my_bookings'))

    booking.tour.available_seats += booking.persons
    if booking.tour.status == 'Sold Out' and booking.tour.available_seats > 0:
        booking.tour.status = 'Available'
    booking.booking_status = 'Cancelled'
    db.session.commit()
    flash('Booking cancelled.', 'info')
    return redirect(url_for('user.my_bookings'))


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@user_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form)
