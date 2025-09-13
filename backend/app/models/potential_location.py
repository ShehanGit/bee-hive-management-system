# app/models/potential_location.py

from app import db
from datetime import datetime

class PotentialLocation(db.Model):
    __tablename__ = 'potential_locations'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    sunlight_exposure = db.Column(db.Float, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    dist_to_water_source = db.Column(db.Float, nullable=False)
    dist_to_flowering_area = db.Column(db.Float, nullable=False)
    dist_to_feeding_station = db.Column(db.Float, nullable=False)
    honey_production = db.Column(db.Float, nullable=True)  # Predicted value
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PotentialLocation lat={self.lat}, lng={self.lng}>"