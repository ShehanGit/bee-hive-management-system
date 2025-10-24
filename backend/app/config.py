# # app/config.py

# class Config:
#     # Example MySQL connection: 
#     # 'mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>'
#     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/hive_db'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/hive_db'
    
    
#     # Optional: track modifications or not
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Other config variables can go here
#     SECRET_KEY = 'your-secret-key'



# IT21807862 - Malinda 

import os
from datetime import timedelta

class Config:
    # Database configuration with environment variable support
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+pymysql://admin:beehive123@behive-db.cdyg48iygzhg.ap-southeast-1.rds.amazonaws.com/hive_db'
        # 'mysql+pymysql://root:admin@localhost/hive_db'
    )
    
    
    # Optional: track modifications or not
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask configuration
    SECRET_KEY = os.environ.get("SECRET_KEY")


    # ----------------------------
    # Adafruit IO Configuration
    # ----------------------------
    ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME")
    ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY")
    ADAFRUIT_BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_USERNAME}/feeds" if ADAFRUIT_USERNAME else None

    # ----------------------------
    # Weather API Configuration
    # ----------------------------
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    WEATHER_BASE_URL = os.environ.get("WEATHER_BASE_URL", "http://api.openweathermap.org/data/2.5/weather")

    # ----------------------------
    # Default Location (Colombo, Sri Lanka)
    # ----------------------------
    DEFAULT_LATITUDE = float(os.environ.get("DEFAULT_LATITUDE", 6.900562))
    DEFAULT_LONGITUDE = float(os.environ.get("DEFAULT_LONGITUDE", 80.922718))