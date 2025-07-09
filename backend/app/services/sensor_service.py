from app import db
from app.models.sensor_data import SensorData

def get_all_sensor_data():
    """Retrieve all sensor data entries."""
    return SensorData.query.all()

def get_sensor_data_by_id(sensor_id):
    """Retrieve a specific sensor data record by its ID."""
    return SensorData.query.get(sensor_id)

def get_sensor_data_by_hive(hive_id):
    """Retrieve all sensor data for a given hive."""
    return SensorData.query.filter_by(hive_id=hive_id).all()

def create_sensor_data(hive_id, sensor_type, sensor_value):
    """Create a new sensor data entry."""
    sensor_data = SensorData(hive_id=hive_id, sensor_type=sensor_type, sensor_value=sensor_value)
    db.session.add(sensor_data)
    db.session.commit()
    return sensor_data

def update_sensor_data(sensor_id, sensor_type=None, sensor_value=None):
    """Update an existing sensor data record."""
    sensor_data = get_sensor_data_by_id(sensor_id)
    if not sensor_data:
        return None
    if sensor_type:
        sensor_data.sensor_type = sensor_type
    if sensor_value:
        sensor_data.sensor_value = sensor_value
    db.session.commit()
    return sensor_data

def delete_sensor_data(sensor_id):
    """Delete a sensor data record."""
    sensor_data = get_sensor_data_by_id(sensor_id)
    if not sensor_data:
        return None
    db.session.delete(sensor_data)
    db.session.commit()
    return sensor_data
