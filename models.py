from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Time

db = SQLAlchemy()


class ParkingRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_day = db.Column(db.Integer, nullable=False)
    start_time = db.Column(Time, nullable=False)
    end_day = db.Column(db.Integer, nullable=False)
    end_time = db.Column(Time, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, start_day, start_time, end_day, end_time, price):
        self.start_day = start_day
        self.start_time = start_time
        self.end_day = end_day
        self.end_time = end_time
        self.price = price
