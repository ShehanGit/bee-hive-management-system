# from app import db
# from datetime import datetime

# class SensorData(db.Model):
#     __tablename__ = 'sensor_data'

#     id = db.Column(db.Integer, primary_key=True)
#     hive_id = db.Column(db.Integer, db.ForeignKey('hives.id'), nullable=False)
#     sensor_type = db.Column(db.String(50), nullable=False)
#     sensor_value = db.Column(db.Float, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return f"<SensorData {self.sensor_type}: {self.sensor_value}>"


from app import db
from datetime import datetime

class SensorData(db.Model):
    __tablename__ = 'sensor_data'

    id = db.Column(db.Integer, primary_key=True)
    hive_id = db.Column(db.Integer, db.ForeignKey('hives.id'), nullable=False)
    sensor_type = db.Column(db.String(50), nullable=False)
    sensor_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<SensorData {self.sensor_type}: {self.sensor_value}>"
