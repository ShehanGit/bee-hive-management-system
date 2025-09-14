# app/config.py

import os
from datetime import timedelta

class Config:
    # MySQL connection for AWS RDS
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:beehive123@behive-db.cdyg48iygzhg.ap-southeast-1.rds.amazonaws.com/hive_db'
    
    # Optional: track modifications or not
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other config variables can go here
    SECRET_KEY = 'your-secret-key'

    # JWT settings
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_BLACKLIST_ENABLED = True

    # OpenWeather API key (replace with your actual key after signing up at https://openweathermap.org/)
    OPENWEATHER_API_KEY = '1eceee44619179169ee5a912cc84231f'