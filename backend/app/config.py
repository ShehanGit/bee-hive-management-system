

# # class Config:
# #     # Example MySQL connection: 
# #     # 'mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>'
# #     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/hive_db'
# #     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/hive_db'
    
    
# #     # Optional: track modifications or not
# #     SQLALCHEMY_TRACK_MODIFICATIONS = False

# #     # Other config variables can go here
# #     SECRET_KEY = 'your-secret-key'



# # app/config.py


# # app/config.py

# import os
# from datetime import timedelta

# class Config:
#     # MySQL Database Configuration
#     # Update these values according to your MySQL setup
#     MYSQL_USERNAME = 'root'  # Change to your MySQL username
#     MYSQL_PASSWORD = 'root'  # Change to your MySQL password
#     MYSQL_HOST = 'localhost'  # Change if MySQL is on different host
#     MYSQL_DATABASE = 'hive_db'  # Database name
    
#     # MySQL Connection String
#     SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'
    
#     # Fallback to SQLite if MySQL connection fails
#     # SQLALCHEMY_DATABASE_URI = 'sqlite:///hive_db.sqlite'
    
    
#     # Optional: track modifications or not
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Other config variables can go here
#     SECRET_KEY = 'your-secret-key'
    
#     # Adafruit IO Configuration
#     ADAFRUIT_USERNAME = '#'
#     ADAFRUIT_KEY = '#'
#     ADAFRUIT_BASE_URL = f'https://io.adafruit.com/api/v2/{ADAFRUIT_USERNAME}/feeds'
    
#     # Weather API Configuration
#     WEATHER_API_KEY = '#'  # Add your OpenWeatherMap API key here
#     WEATHER_BASE_URL = '#'
    
#     # Default Location (Colombo, Sri Lanka)
#     DEFAULT_LATITUDE = 6.9271
#     DEFAULT_LONGITUDE = 79.8612


# app/config.py

import os
from datetime import timedelta

class Config:
    # ----------------------------
    # Database Configuration
    # ----------------------------
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "root")
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "hive_db")

    # MySQL Connection String
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    )

    # Optional fallback to SQLite (for testing/dev)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///hive_db.sqlite'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ----------------------------
    # Security
    # ----------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

    # ----------------------------
    # JWT Authentication
    # ----------------------------
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_BLACKLIST_ENABLED = True

    # ----------------------------
    # Adafruit IO Configuration
    # ----------------------------
    ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME", "#")
    ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY", "#")
    ADAFRUIT_BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_USERNAME}/feeds"

    # ----------------------------
    # Weather API Configuration
    # ----------------------------
    WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "#")
    WEATHER_BASE_URL = os.environ.get("WEATHER_BASE_URL", "#")

    # ----------------------------
    # Default Location (Colombo, Sri Lanka)
    # ----------------------------
    DEFAULT_LATITUDE = float(os.environ.get("DEFAULT_LATITUDE", 6.9271))
    DEFAULT_LONGITUDE = float(os.environ.get("DEFAULT_LONGITUDE", 79.8612))
