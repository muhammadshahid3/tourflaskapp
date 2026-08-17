from datetime import datetime, timedelta
from calendar import month_abbr

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func, extract

from app.extensions import db
from app.decorators import admin_required
from app.models import Category, Destination, Tour, Booking, User
from app.forms import CategoryForm, DestinationForm, TourForm, BookingActionForm
from app.admin.helpers import save_upload

admin_bp = Blueprint('admin', __name__)


# ---------- Dashboard ----------

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_tours = Tour.query.count()
    total_bookings = Booking.query.count()
    total_categories = Category.query.count()
    total_destinations = Destination.query.count()
    total_revenue = db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(
        Booking.booking_status.in_(['Confirmed', 'Completed'])
    ).scalar()

    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_tours=total_tours,
        total_bookings=total_bookings,
        total_categories=total_categories,
        total_destinations=total_destinations,
        total_revenue=total_revenue,
        recent_bookings=recent_bookings,
    )


# ---------- Category CRUD ----------

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    items = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=items)


@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        image_path = save_upload(form.image.data)
        category = Category(name=form.name.data, description=form.description.data, image=image_path)
        db.session.add(category)
        db.session.commit()
        flash('Category added.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='Add Category')


@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        image_path = save_upload(form.image.data)
        if image_path:
            category.image = image_path
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('admin.categories'))
    return render_template('admin/category_form.html', form=form, title='Edit Category')


@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.tours:
        flash('Cannot delete a category that still has tours assigned to it.', 'danger')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted.', 'success')
    return redirect(url_for('admin.categories'))


# ---------- Destination CRUD ----------

@admin_bp.route('/destinations')
@login_required
@admin_required
def destinations():
    items = Destination.query.order_by(Destination.name).all()
    return render_template('admin/destinations.html', destinations=items)


@admin_bp.route('/destinations/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_destination():
    form = DestinationForm()
    if form.validate_on_submit():
        image_path = save_upload(form.image.data)
        destination = Destination(
            name=form.name.data, country=form.country.data, city=form.city.data,
            description=form.description.data, image=image_path,
        )
        db.session.add(destination)
        db.session.commit()
        flash('Destination added.', 'success')
        return redirect(url_for('admin.destinations'))
    return render_template('admin/destination_form.html', form=form, title='Add Destination')


@admin_bp.route('/destinations/<int:destination_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    form = DestinationForm(obj=destination)
    if form.validate_on_submit():
        destination.name = form.name.data
        destination.country = form.country.data
        destination.city = form.city.data
        destination.description = form.description.data
        image_path = save_upload(form.image.data)
        if image_path:
            destination.image = image_path
        db.session.commit()
        flash('Destination updated.', 'success')
        return redirect(url_for('admin.destinations'))
    return render_template('admin/destination_form.html', form=form, title='Edit Destination')


@admin_bp.route('/destinations/<int:destination_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    if destination.tours:
        flash('Cannot delete a destination that still has tours assigned to it.', 'danger')
    else:
        db.session.delete(destination)
        db.session.commit()
        flash('Destination deleted.', 'success')
    return redirect(url_for('admin.destinations'))


# ---------- Tour CRUD ----------

def _populate_tour_choices(form):
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    form.destination_id.choices = [(d.id, d.name) for d in Destination.query.order_by(Destination.name).all()]


@admin_bp.route('/tours')
@login_required
@admin_required
def tours():
    items = Tour.query.order_by(Tour.created_at.desc()).all()
    return render_template('admin/tours.html', tours=items)


@admin_bp.route('/tours/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tour():
    form = TourForm()
    _populate_tour_choices(form)
    if form.validate_on_submit():
        image_path = save_upload(form.image.data)
        tour = Tour(
            title=form.title.data,
            image=image_path,
            destination_id=form.destination_id.data,
            category_id=form.category_id.data,
            description=form.description.data,
            duration=form.duration.data,
            price=form.price.data,
            discount=form.discount.data or 0,
            max_guests=form.max_guests.data,
            available_seats=form.available_seats.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            included_services=form.included_services.data,
            excluded_services=form.excluded_services.data,
            hotel=form.hotel.data,
            transport=form.transport.data,
            rating=form.rating.data or 0,
            status=form.status.data,
        )
        db.session.add(tour)
        db.session.commit()
        flash('Tour added.', 'success')
        return redirect(url_for('admin.tours'))
    return render_template('admin/tour_form.html', form=form, title='Add Tour')


@admin_bp.route('/tours/<int:tour_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = TourForm(obj=tour)
    _populate_tour_choices(form)
    if request.method == 'GET':
        form.category_id.data = tour.category_id
        form.destination_id.data = tour.destination_id
    if form.validate_on_submit():
        tour.title = form.title.data
        tour.destination_id = form.destination_id.data
        tour.category_id = form.category_id.data
        tour.description = form.description.data
        tour.duration = form.duration.data
        tour.price = form.price.data
        tour.discount = form.discount.data or 0
        tour.max_guests = form.max_guests.data
        tour.available_seats = form.available_seats.data
        tour.start_date = form.start_date.data
        tour.end_date = form.end_date.data
        tour.included_services = form.included_services.data
        tour.excluded_services = form.excluded_services.data
        tour.hotel = form.hotel.data
        tour.transport = form.transport.data
        tour.rating = form.rating.data or 0
        tour.status = form.status.data
        image_path = save_upload(form.image.data)
        if image_path:
            tour.image = image_path
        db.session.commit()
        flash('Tour updated.', 'success')
        return redirect(url_for('admin.tours'))
    return render_template('admin/tour_form.html', form=form, title='Edit Tour')


@admin_bp.route('/tours/<int:tour_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    db.session.delete(tour)
    db.session.commit()
    flash('Tour deleted.', 'success')
    return redirect(url_for('admin.tours'))


# ---------- Booking management ----------

@admin_bp.route('/bookings')
@login_required
@admin_required
def bookings():
    status_filter = request.args.get('status', 'All')
    query = Booking.query
    if status_filter != 'All':
        query = query.filter_by(booking_status=status_filter)
    items = query.order_by(Booking.booking_date.desc()).all()
    form = BookingActionForm()
    return render_template('admin/bookings.html', bookings=items, status_filter=status_filter, form=form)


@admin_bp.route('/bookings/<int:booking_id>/confirm', methods=['POST'])
@login_required
@admin_required
def confirm_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.booking_status == 'Pending':
        booking.booking_status = 'Confirmed'
        db.session.commit()
        flash(f'Booking #{booking.id} confirmed.', 'success')
    else:
        flash('Only pending bookings can be confirmed.', 'warning')
    return redirect(url_for('admin.bookings'))


@admin_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
@admin_required
def cancel_booking_admin(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.booking_status in ('Pending', 'Confirmed'):
        if booking.booking_status == 'Confirmed':
            booking.tour.available_seats += booking.persons
        booking.booking_status = 'Cancelled'
        db.session.commit()
        flash(f'Booking #{booking.id} cancelled.', 'info')
    else:
        flash('This booking cannot be cancelled.', 'warning')
    return redirect(url_for('admin.bookings'))


@admin_bp.route('/bookings/<int:booking_id>/complete', methods=['POST'])
@login_required
@admin_required
def complete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.booking_status == 'Confirmed':
        booking.booking_status = 'Completed'
        db.session.commit()
        flash(f'Booking #{booking.id} marked completed.', 'success')
    else:
        flash('Only confirmed bookings can be marked completed.', 'warning')
    return redirect(url_for('admin.bookings'))


# ---------- User management ----------

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    items = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=items)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/block', methods=['POST'])
@login_required
@admin_required
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blocked = True
    db.session.commit()
    flash(f'{user.full_name} has been blocked.', 'info')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@login_required
@admin_required
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blocked = False
    user.is_active_account = True
    db.session.commit()
    flash(f'{user.full_name} has been activated.', 'success')
    return redirect(url_for('admin.users'))


# ---------- Reports ----------

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    # Revenue + bookings per month for the last 6 months
    today = datetime.utcnow()
    pairs = []
    y, m = today.year, today.month
    for _ in range(6):
        pairs.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    pairs.reverse()

    monthly_revenue = []
    monthly_bookings = []
    labels = []
    for (y, m) in pairs:
        revenue = db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(
            extract('year', Booking.booking_date) == y,
            extract('month', Booking.booking_date) == m,
            Booking.booking_status.in_(['Confirmed', 'Completed']),
        ).scalar()
        count = db.session.query(func.count(Booking.id)).filter(
            extract('year', Booking.booking_date) == y,
            extract('month', Booking.booking_date) == m,
        ).scalar()
        labels.append(f"{month_abbr[m]} {y}")
        monthly_revenue.append(float(revenue))
        monthly_bookings.append(int(count))

    most_booked = db.session.query(
        Tour.title, func.count(Booking.id).label('cnt')
    ).join(Booking).group_by(Tour.id).order_by(func.count(Booking.id).desc()).limit(5).all()

    popular_destinations = db.session.query(
        Destination.name, func.count(Booking.id).label('cnt')
    ).join(Tour, Tour.destination_id == Destination.id).join(Booking, Booking.tour_id == Tour.id).group_by(
        Destination.id
    ).order_by(func.count(Booking.id).desc()).limit(5).all()

    total_revenue = db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(
        Booking.booking_status.in_(['Confirmed', 'Completed'])
    ).scalar()

    return render_template(
        'admin/reports.html',
        labels=labels,
        monthly_revenue=monthly_revenue,
        monthly_bookings=monthly_bookings,
        most_booked=most_booked,
        popular_destinations=popular_destinations,
        total_revenue=total_revenue,
    )
