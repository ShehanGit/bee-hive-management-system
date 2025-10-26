from app import db
from datetime import datetime

class SynchronizedData(db.Model):
    """
    Model for storing synchronized sensor and weather data
    with perfect timestamp alignment for future prediction models
    """
    __tablename__ = 'synchronized_data'

    id = db.Column(db.Integer, primary_key=True)
    collection_timestamp = db.Column(db.DateTime, nullable=False, index=True, default=datetime.now)
    hive_id = db.Column(db.Integer, db.ForeignKey('hives.id'), nullable=False)
    
    # Weather data fields (only specified fields)
    weather_temperature = db.Column(db.Float, nullable=True)  # Temperature in °C
    weather_humidity = db.Column(db.Float, nullable=True)     # Humidity in %
    weather_wind_speed = db.Column(db.Float, nullable=True)   # Wind Speed in km/h
    weather_light_intensity = db.Column(db.Float, nullable=True)  # Light Intensity in lux
    weather_rainfall = db.Column(db.Float, nullable=True)     # Rainfall in mm/hour
    
    # Sensor data fields (only specified fields)
    sensor_temperature = db.Column(db.Float, nullable=True)   # Temperature in °C
    sensor_humidity = db.Column(db.Float, nullable=True)      # Humidity in %
    sensor_sound = db.Column(db.Float, nullable=True)         # Sound in dB
    sensor_weight = db.Column(db.Float, nullable=True)        # Weight in kg
    
    # Threat detection fields (generated from existing data)
    sensor_sound_peak_freq = db.Column(db.Float, nullable=True)  # Sound peak frequency in Hz
    sensor_vibration_hz = db.Column(db.Float, nullable=True)     # Vibration frequency in Hz
    sensor_vibration_var = db.Column(db.Float, nullable=True)     # Vibration variance
    
    # Metadata
    weather_data_id = db.Column(db.Integer, db.ForeignKey('weather_data.id'), nullable=True)
    sensor_data_count = db.Column(db.Integer, default=0)
    collection_success = db.Column(db.Boolean, default=True)
    api_usage_weather_calls = db.Column(db.Integer, default=0)
    api_usage_adafruit_calls = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f'<SynchronizedData {self.id}: {self.collection_timestamp}>'
    
    def to_dict(self):
        """Convert SynchronizedData instance to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'collection_timestamp': self.collection_timestamp.isoformat() if self.collection_timestamp else None,
            'hive_id': self.hive_id,
            
            # Weather data (only fields that exist)
            'weather': {
                'temperature': self.weather_temperature,
                'humidity': self.weather_humidity,
                'wind_speed': self.weather_wind_speed,
                'light_intensity': self.weather_light_intensity,
                'rainfall': self.weather_rainfall
            },
            
            # Sensor data (only fields that exist)
            'sensors': {
                'temperature': self.sensor_temperature,
                'humidity': self.sensor_humidity,
                'sound': self.sensor_sound,
                'weight': self.sensor_weight
            },
            
            # Threat detection data (generated fields)
            'threat_detection': {
                'sound_peak_freq': self.sensor_sound_peak_freq,
                'vibration_hz': self.sensor_vibration_hz,
                'vibration_var': self.sensor_vibration_var
            },
            
            # Metadata
            'metadata': {
                'weather_data_id': self.weather_data_id,
                'sensor_data_count': self.sensor_data_count,
                'collection_success': self.collection_success,
                'api_usage': {
                    'weather_calls': self.api_usage_weather_calls,
                    'adafruit_calls': self.api_usage_adafruit_calls
                },
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
        }
    
    @classmethod
    def get_latest(cls, hive_id: int = 1):
        """Get the most recent synchronized data entry for a hive"""
        return cls.query.filter_by(hive_id=hive_id).order_by(cls.collection_timestamp.desc()).first()
    
    @classmethod
    def get_historical_data(cls, hive_id: int = 1, hours: int = 24):
        """Get historical synchronized data for the specified number of hours"""
        from datetime import datetime, timedelta
        since_time = datetime.now() - timedelta(hours=hours)
        return cls.query.filter(
            cls.hive_id == hive_id,
            cls.collection_timestamp >= since_time
        ).order_by(cls.collection_timestamp.asc()).all()
    
    @classmethod
    def get_perfect_alignment_data(cls, hive_id: int = 1, hours: int = 24):
        """Get only perfectly aligned data (both weather and sensor data present)"""
        from datetime import datetime, timedelta
        since_time = datetime.now() - timedelta(hours=hours)
        return cls.query.filter(
            cls.hive_id == hive_id,
            cls.collection_timestamp >= since_time,
            cls.weather_temperature.isnot(None),
            cls.sensor_temperature.isnot(None)
        ).order_by(cls.collection_timestamp.asc()).all()
    
    @classmethod
    def get_alignment_statistics(cls, hive_id: int = 1, hours: int = 24):
        """Get statistics about data alignment quality"""
        from datetime import datetime, timedelta
        since_time = datetime.now() - timedelta(hours=hours)
        
        total_records = cls.query.filter(
            cls.hive_id == hive_id,
            cls.collection_timestamp >= since_time
        ).count()
        
        perfect_alignment = cls.query.filter(
            cls.hive_id == hive_id,
            cls.collection_timestamp >= since_time,
            cls.weather_temperature.isnot(None),
            cls.sensor_temperature.isnot(None)
        ).count()
        
        weather_only = cls.query.filter(
            cls.hive_id == hive_id,
            cls.collection_timestamp >= since_time,
            cls.weather_temperature.isnot(None),
            cls.sensor_temperature.is_(None)
        ).count()
        
        sensor_only = cls.query.filter(
            cls.hive_id == hive_id,
            cls.collection_timestamp >= since_time,
            cls.weather_temperature.is_(None),
            cls.sensor_temperature.isnot(None)
        ).count()
        
        return {
            'total_records': total_records,
            'perfect_alignment': perfect_alignment,
            'weather_only': weather_only,
            'sensor_only': sensor_only,
            'alignment_percentage': (perfect_alignment / total_records * 100) if total_records > 0 else 0,
            'hours_analyzed': hours
        }
    
    def calculate_temperature_difference(self):
        """Calculate temperature difference between sensor and weather"""
        if self.sensor_temperature is not None and self.weather_temperature is not None:
            return self.sensor_temperature - self.weather_temperature
        return None
    
    def calculate_humidity_difference(self):
        """Calculate humidity difference between sensor and weather"""
        if self.sensor_humidity is not None and self.weather_humidity is not None:
            return self.sensor_humidity - self.weather_humidity
        return None
    
    def is_perfectly_aligned(self):
        """Check if this record has both weather and sensor data"""
        return (self.weather_temperature is not None and 
                self.sensor_temperature is not None)
    
    def get_data_quality_score(self):
        """Calculate data quality score based on available data"""
        score = 0
        max_score = 0
        
        # Weather data quality (50% of score)
        weather_fields = [
            self.weather_temperature, self.weather_humidity, 
            self.weather_wind_speed, self.weather_light_intensity, self.weather_rainfall
        ]
        for field in weather_fields:
            max_score += 1
            if field is not None:
                score += 1
        
        # Sensor data quality (50% of score)
        sensor_fields = [
            self.sensor_temperature, self.sensor_humidity,
            self.sensor_sound, self.sensor_weight
        ]
        for field in sensor_fields:
            max_score += 1
            if field is not None:
                score += 1
        
        return (score / max_score * 100) if max_score > 0 else 0
    
    def calculate_threat_detection_fields(self):
        """
        Calculate missing threat detection fields from existing data
        Uses intelligent estimation based on bee behavior patterns
        """
        # Sound peak frequency estimation based on activity level
        self.sensor_sound_peak_freq = self._estimate_sound_peak_frequency()
        
        # Vibration frequency estimation based on sound and environment
        self.sensor_vibration_hz = self._estimate_vibration_frequency()
        
        # Vibration variance estimation based on environmental disturbances
        self.sensor_vibration_var = self._estimate_vibration_variance()
    
    def _estimate_sound_peak_frequency(self):
        """Estimate peak frequency based on sound intensity and bee behavior patterns"""
        if self.sensor_sound is None:
            return 200.0  # Default frequency
        
        sound_db = self.sensor_sound
        
        # Bee sound frequency ranges based on activity level
        if sound_db < 50:      # Low activity
            return 150.0 + (sound_db * 0.5)  # 150-175 Hz
        elif sound_db < 70:    # Normal activity  
            return 175.0 + ((sound_db - 50) * 1.0)  # 175-195 Hz
        elif sound_db < 85:    # High activity
            return 195.0 + ((sound_db - 70) * 0.8)  # 195-207 Hz
        else:                  # Very high activity (potential threat)
            return 207.0 + ((sound_db - 85) * 0.5)  # 207-215 Hz
    
    def _estimate_vibration_frequency(self):
        """Estimate vibration frequency based on sound and environmental conditions"""
        if self.sensor_sound is None:
            return 200.0  # Default vibration
        
        # Base vibration from sound intensity
        base_vibration = 150.0 + (self.sensor_sound * 0.8)  # 150-218 Hz range
        
        # Environmental adjustments
        temp_factor = 1.0
        if self.weather_temperature and self.weather_temperature > 35:  # Hot weather increases activity
            temp_factor = 1.1
        elif self.weather_temperature and self.weather_temperature < 15:  # Cold weather decreases activity
            temp_factor = 0.9
        
        humidity_factor = 1.0
        if self.weather_humidity and self.weather_humidity > 80:  # High humidity affects behavior
            humidity_factor = 0.95
        
        estimated_vibration = base_vibration * temp_factor * humidity_factor
        
        # Clamp to realistic range
        return max(100.0, min(300.0, estimated_vibration))
    
    def _estimate_vibration_variance(self):
        """Estimate vibration variance based on sound and environmental disturbances"""
        if self.sensor_sound is None:
            return 10.0  # Default variance
        
        # Base variance from sound intensity
        base_variance = 5.0 + (self.sensor_sound * 0.1)  # 5-13.5 range
        
        # Environmental disturbance factors
        wind_factor = 1.0
        if self.weather_wind_speed and self.weather_wind_speed > 20:  # Strong wind
            wind_factor = 1.5
        elif self.weather_wind_speed and self.weather_wind_speed > 10:  # Moderate wind
            wind_factor = 1.2
        
        rain_factor = 1.0
        if self.weather_rainfall and self.weather_rainfall > 5:  # Heavy rain
            rain_factor = 1.3
        elif self.weather_rainfall and self.weather_rainfall > 0:  # Light rain
            rain_factor = 1.1
        
        estimated_variance = base_variance * wind_factor * rain_factor
        
        # Clamp to realistic range
        return max(2.0, min(25.0, estimated_variance))
    
    def get_threat_detection_payload(self):
        """
        Get threat detection payload format for ML model
        Returns data in the format expected by threat detection model
        """
        return {
            "weather_temp_c": self.weather_temperature or 30.0,
            "weather_humidity_pct": self.weather_humidity or 60.0,
            "hive_sound_db": self.sensor_sound or 70.0,
            "hive_sound_peak_freq": self.sensor_sound_peak_freq or 200.0,
            "vibration_hz": self.sensor_vibration_hz or 200.0,
            "vibration_var": self.sensor_vibration_var or 10.0,
            "timestamp": self.collection_timestamp.isoformat() if self.collection_timestamp else None
        }
