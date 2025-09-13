from flask import Blueprint, jsonify, request
from app.services.weather_service import weather_service
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

weather_blueprint = Blueprint('weather_blueprint', __name__)

@weather_blueprint.route('/weather/latest', methods=['GET'])
def get_latest_weather():
    """
    Get the most recent weather data
    
    Returns:
        JSON response with latest weather data
    """
    try:
        latest_weather = weather_service.get_latest_weather()
        
        if latest_weather:
            return jsonify({
                'success': True,
                'data': latest_weather.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No weather data available',
                'data': {
                    'temperature': None,
                    'humidity': None,
                    'wind_speed': None,
                    'rainfall': None,
                    'light_intensity': None,
                    'weather_description': None,
                    'pressure': None,
                    'visibility': None,
                    'timestamp': None
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Error in get_latest_weather: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve weather data',
            'message': str(e)
        }), 500

@weather_blueprint.route('/weather/historical', methods=['GET'])
def get_historical_weather():
    """
    Get historical weather data
    
    Query Parameters:
        hours (int): Number of hours of historical data (default: 24)
        
    Returns:
        JSON response with historical weather data
    """
    try:
        hours = request.args.get('hours', 24, type=int)
        
        # Limit hours to prevent excessive data retrieval
        if hours > 168:  # Max 1 week
            hours = 168
        
        historical_data = weather_service.get_historical_weather(hours)
        
        return jsonify({
            'success': True,
            'hours': hours,
            'count': len(historical_data),
            'data': [weather.to_dict() for weather in historical_data]
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_historical_weather: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve historical weather data',
            'message': str(e)
        }), 500

@weather_blueprint.route('/weather/fetch', methods=['POST'])
def fetch_weather_data():
    """
    Manually trigger weather data fetch and save
    
    Returns:
        JSON response indicating success or failure
    """
    try:
        success = weather_service.fetch_and_save_weather()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Weather data fetched and saved successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to fetch or save weather data'
            }), 500
            
    except Exception as e:
        logger.error(f"Error in fetch_weather_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch weather data',
            'message': str(e)
        }), 500

@weather_blueprint.route('/weather/status', methods=['GET'])
def get_weather_status():
    """
    Get weather service status and latest data info
    
    Returns:
        JSON response with service status
    """
    try:
        latest_weather = weather_service.get_latest_weather()
        
        status = {
            'service_status': 'active',
            'api_key_configured': bool(weather_service.api_key),
            'location': weather_service.location,
            'coordinates': {
                'latitude': weather_service.latitude,
                'longitude': weather_service.longitude
            }
        }
        
        if latest_weather:
            status['latest_data'] = {
                'timestamp': latest_weather.timestamp.isoformat(),
                'temperature': latest_weather.temperature,
                'humidity': latest_weather.humidity
            }
            status['data_age_minutes'] = (datetime.utcnow() - latest_weather.timestamp).total_seconds() / 60
        else:
            status['latest_data'] = None
            status['data_age_minutes'] = None
        
        return jsonify({
            'success': True,
            'status': status
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_weather_status: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get weather status',
            'message': str(e)
        }), 500
