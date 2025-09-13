# # app/models/hive.py

# from app import db
# from datetime import datetime

# class Hive(db.Model):
#     __tablename__ = 'hives'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     location_lat = db.Column(db.Float, nullable=False)
#     location_lng = db.Column(db.Float, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<Hive {self.name}>"


# app/models/hive.py

from app import db
from datetime import datetime

class Hive(db.Model):
    __tablename__ = 'hives'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_lng = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Hive {self.name}>"
