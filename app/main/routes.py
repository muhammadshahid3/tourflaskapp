from flask import Blueprint, render_template, request
from sqlalchemy import or_
from app.models import Tour, Category, Destination

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    featured_destinations = Destination.query.limit(6).all()
    popular_tours = Tour.query.filter_by(status='Available').order_by(Tour.rating.desc()).limit(6).all()
    categories = Category.query.limit(8).all()
    return render_template(
        'main/index.html',
        destinations=featured_destinations,
        tours=popular_tours,
        categories=categories,
    )


@main_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    tours = []
    if q:
        like = f"%{q}%"
        tours = Tour.query.join(Destination).filter(
            or_(
                Tour.title.ilike(like),
                Destination.name.ilike(like),
                Destination.city.ilike(like),
                Destination.country.ilike(like),
            )
        ).all()
    return render_template('main/search_results.html', tours=tours, query=q)


@main_bp.route('/tour/<int:tour_id>')
def tour_detail_public(tour_id):
    from flask import redirect, url_for
    # Public visitors are routed through the account area so booking
    # always happens from an authenticated session.
    return redirect(url_for('user.tour_detail', tour_id=tour_id))
