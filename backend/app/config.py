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








# # app/config.py

# import os
# from datetime import timedelta

# class Config:
#     # Example MySQL connection: 
#     # 'mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>'
#     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/hive_db'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:user@localhost/hive_db'

#     # SQLALCHEMY_DATABASE_URI = os.environ.get(
#     #     "DATABASE_URL",
#     #     "mysql+pymysql://root:root@localhost:3306/bee_hive_db"
#     # )
    
    
#     # Optional: track modifications or not
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Other config variables can go here
#     SECRET_KEY = 'your-secret-key'

#     # ✅ JWT settings
#     JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret")
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
#     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
#     JWT_ALGORITHM = "HS256"
#     JWT_TOKEN_LOCATION = ["headers"]
#     JWT_BLACKLIST_ENABLED = True

    



#Performance predict 

# import os
# from datetime import timedelta

# class Config:
#     # ----------------------------
#     # Database Configuration
#     # ----------------------------
#     # Uses environment variables for configuration, with defaults pointing to the
#     # AWS RDS instance from the main branch for production compatibility.
#     MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME", "admin")
#     MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "beehive123")
#     MYSQL_HOST = os.environ.get("MYSQL_HOST", "behive-db.cdyg48iygzhg.ap-southeast-1.rds.amazonaws.com")
#     MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "hive_db")

#     # The database connection string is built dynamically from the variables above.
#     SQLALCHEMY_DATABASE_URI = (
#         f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
#     )
    
#     # Disable modification tracking to improve performance.
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # ----------------------------
#     # Security
#     # ----------------------------
#     # A secret key is required for session management and security features.
#     SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")

#     # ----------------------------
#     # JWT Authentication
#     # ----------------------------
#     JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret")
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
#     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
#     JWT_ALGORITHM = "HS256"
#     JWT_TOKEN_LOCATION = ["headers"]
#     JWT_BLACKLIST_ENABLED = True

#     # ----------------------------
#     # Adafruit IO Configuration
#     # ----------------------------
#     ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME", "malinda_0506")
#     ADAFRUIT_KEY = os.environ.get("ADAFRUIT_KEY", "aio_ckGM96Q0lKHzRZJSylWn3KCTi1q8")
#     ADAFRUIT_BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_USERNAME}/feeds"

#     # ----------------------------
#     # Weather API Configuration
#     # ----------------------------
#     WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY", "991f4245cb918f65ec5beec666b4802e")
#     WEATHER_BASE_URL = os.environ.get("WEATHER_BASE_URL", "http://api.openweathermap.org/data/2.5/weather")

#     # ----------------------------
#     # Default Location (Colombo, Sri Lanka)
#     # ----------------------------
#     DEFAULT_LATITUDE = float(os.environ.get("DEFAULT_LATITUDE", 6.9271))
#     DEFAULT_LONGITUDE = float(os.environ.get("DEFAULT_LONGITUDE", 79.8612))

