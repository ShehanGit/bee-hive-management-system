from flask import Blueprint, jsonify, request
from app.services.iot_integration_service import fetch_and_save_iot_data

iot_blueprint = Blueprint('iot_blueprint', __name__)

@iot_blueprint.route('/iot/fetch', methods=['GET'])
def fetch_iot_data():
    """
    Call the IoT device endpoints, save the sensor data to the database,
    and return a success or error message.
    """
    # Optionally, you can pass a hive_id as a query parameter. Here we use a default.
    hive_id = request.args.get("hive_id", 1, type=int)
    success = fetch_and_save_iot_data(hive_id)
    if success:
        return jsonify({"message": "IoT data fetched and saved successfully"}), 200
    else:
        return jsonify({"error": "Failed to fetch IoT data"}), 500
