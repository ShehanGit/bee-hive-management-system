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



# app/config.py


# app/config.py

class Config:
    # MySQL Database Configuration
    # Update these values according to your MySQL setup
    MYSQL_USERNAME = 'root'  # Change to your MySQL username
    MYSQL_PASSWORD = 'root'  # Change to your MySQL password
    MYSQL_HOST = 'localhost'  # Change if MySQL is on different host
    MYSQL_DATABASE = 'hive_db'  # Database name
    
    # MySQL Connection String
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'
    
    # Fallback to SQLite if MySQL connection fails
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///hive_db.sqlite'
    
    
    # Optional: track modifications or not
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other config variables can go here
    SECRET_KEY = 'your-secret-key'
