import os
from datetime import timedelta

class Config:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+pymysql://root:root@localhost/hive_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Configuration
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")  # Default fallback for development

    # Adafruit IO Configuration
    ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME")
    ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY")
    ADAFRUIT_BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_USERNAME}/feeds" if ADAFRUIT_USERNAME else None

    # Weather API Configuration
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    WEATHER_BASE_URL = os.environ.get("WEATHER_BASE_URL", "http://api.openweathermap.org/data/2.5/weather")

    # Default Location (Colombo, Sri Lanka)
    DEFAULT_LATITUDE = float(os.environ.get("DEFAULT_LATITUDE", 6.900562))
    DEFAULT_LONGITUDE = float(os.environ.get("DEFAULT_LONGITUDE", 80.922718))