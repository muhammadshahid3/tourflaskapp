from datetime import datetime
from app.extensions import db


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)

    persons = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    # Pending -> Confirmed -> Completed, or Cancelled at any point before Completed
    booking_status = db.Column(db.String(20), nullable=False, default='Pending')
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Booking #{self.id} tour={self.tour_id} user={self.user_id}>"
