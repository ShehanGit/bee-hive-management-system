# app/config.py

class Config:
    # Example MySQL connection: 
    # 'mysql+pymysql://<USERNAME>:<PASSWORD>@<HOST>/<DATABASE>'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/hive_db'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/hive_db'
    
    
    # Optional: track modifications or not
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Other config variables can go here
    SECRET_KEY = 'your-secret-key'
