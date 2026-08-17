from app.extensions import db


class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))

    tours = db.relationship('Tour', backref='destination', lazy=True)

    def __repr__(self):
        return f"<Destination {self.name}, {self.country}>"
