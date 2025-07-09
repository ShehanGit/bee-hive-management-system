from flask import Blueprint, request, jsonify
from app.services.sensor_service import (
    get_all_sensor_data,
    get_sensor_data_by_id,
    create_sensor_data,
    update_sensor_data,
    delete_sensor_data
)

sensor_blueprint = Blueprint('sensor_blueprint', __name__)

@sensor_blueprint.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    """Endpoint to get all sensor data."""
    sensor_data_list = get_all_sensor_data()
    results = [{
        'id': sensor_data.id,
        'hive_id': sensor_data.hive_id,
        'sensor_type': sensor_data.sensor_type,
        'sensor_value': sensor_data.sensor_value,
        'created_at': sensor_data.created_at
    } for sensor_data in sensor_data_list]
    return jsonify(results), 200

@sensor_blueprint.route('/sensor-data', methods=['POST'])
def add_sensor_data():
    """Endpoint to create a new sensor data record."""
    data = request.get_json()
    if not data or not all([data.get('hive_id'), data.get('sensor_type'), data.get('sensor_value')]):
        return jsonify({"error": "Missing required fields"}), 400
    sensor_data = create_sensor_data(data['hive_id'], data['sensor_type'], data['sensor_value'])
    return jsonify({
        "message": "Sensor data created successfully",
        "id": sensor_data.id
    }), 201

@sensor_blueprint.route('/sensor-data/<int:sensor_id>', methods=['GET'])
def get_single_sensor_data(sensor_id):
    """Endpoint to get a specific sensor data record."""
    sensor_data = get_sensor_data_by_id(sensor_id)
    if not sensor_data:
        return jsonify({"error": "Sensor data not found"}), 404
    return jsonify({
        'id': sensor_data.id,
        'hive_id': sensor_data.hive_id,
        'sensor_type': sensor_data.sensor_type,
        'sensor_value': sensor_data.sensor_value,
        'created_at': sensor_data.created_at
    }), 200

@sensor_blueprint.route('/sensor-data/<int:sensor_id>', methods=['PUT'])
def modify_sensor_data(sensor_id):
    """Endpoint to update a sensor data record."""
    data = request.get_json()
    sensor_data = update_sensor_data(sensor_id, data.get('sensor_type'), data.get('sensor_value'))
    if not sensor_data:
        return jsonify({"error": "Sensor data not found"}), 404
    return jsonify({"message": "Sensor data updated successfully"}), 200

@sensor_blueprint.route('/sensor-data/<int:sensor_id>', methods=['DELETE'])
def remove_sensor_data(sensor_id):
    """Endpoint to delete a sensor data record."""
    sensor_data = delete_sensor_data(sensor_id)
    if not sensor_data:
        return jsonify({"error": "Sensor data not found"}), 404
    return jsonify({"message": "Sensor data deleted successfully"}), 200
