from app import db
from datetime import datetime

class WeatherData(db.Model):
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True, default=datetime.now)
    temperature = db.Column(db.Float, nullable=True)  # Temperature in °C
    humidity = db.Column(db.Float, nullable=True)     # Humidity in %
    wind_speed = db.Column(db.Float, nullable=True)   # Wind Speed in km/h
    light_intensity = db.Column(db.Float, nullable=True)  # Light Intensity in lux
    rainfall = db.Column(db.Float, nullable=True)     # Rainfall in mm/hour

    def __repr__(self):
        return f'<WeatherData {self.id}: {self.temperature}°C>'
    
    def to_dict(self):
        """Convert WeatherData instance to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'light_intensity': self.light_intensity,
            'rainfall': self.rainfall
        }
    
    @classmethod
    def get_latest(cls):
        """Get the most recent weather data entry"""
        return cls.query.order_by(cls.timestamp.desc()).first()
    
    @classmethod
    def get_historical_data(cls, hours=24):
        """Get historical weather data for the specified number of hours"""
        from datetime import datetime, timedelta
        since_time = datetime.utcnow() - timedelta(hours=hours)
        return cls.query.filter(cls.timestamp >= since_time).order_by(cls.timestamp.asc()).all()

