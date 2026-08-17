from datetime import datetime
from app.extensions import db


class Tour(db.Model):
    __tablename__ = 'tours'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    duration = db.Column(db.String(80))  # e.g. "5 Days / 4 Nights"

    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(5, 2), default=0)  # percentage

    max_guests = db.Column(db.Integer, nullable=False, default=1)
    available_seats = db.Column(db.Integer, nullable=False, default=0)

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    included_services = db.Column(db.Text)
    excluded_services = db.Column(db.Text)

    hotel = db.Column(db.String(150))
    transport = db.Column(db.String(150))
    rating = db.Column(db.Numeric(2, 1), default=0)

    status = db.Column(db.String(20), nullable=False, default='Available')  # Available / Sold Out
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='tour', lazy=True, cascade='all, delete-orphan')

    @property
    def discounted_price(self):
        if self.discount and self.discount > 0:
            return round(float(self.price) * (1 - float(self.discount) / 100), 2)
        return float(self.price)

    def __repr__(self):
        return f"<Tour {self.title}>"
