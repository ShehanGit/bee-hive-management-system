# app/controllers/weather_controller.py

from flask import Blueprint, request, jsonify
from app.services.weather__for_location_service import get_current_weather

weather_blueprint = Blueprint('weather_blueprint', __name__)

@weather_blueprint.route('/weather', methods=['GET'])
def get_weather():
    """
    Get current weather for a location.
    
    Query Params:
        - lat (float): Required. Latitude (e.g., 6.9271).
        - lon (float): Required. Longitude (e.g., 79.8612).
        - units (str): Optional. 'metric' (default), 'imperial', or 'standard'.
    """
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    units = request.args.get('units', 'metric')
    
    if not lat or not lon:
        return jsonify({"error": "Missing required parameters: lat and lon"}), 400
    
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "Invalid lat/lon: must be numbers"}), 400
    
    weather_data = get_current_weather(lat, lon, units)
    
    if weather_data is None:
        return jsonify({"error": "Failed to fetch weather data"}), 500
    
    return jsonify({
        "location": {"lat": lat, "lon": lon},
        "data": weather_data
    }), 200