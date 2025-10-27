# app/services/weather_service.py

import requests
from app import app  # For logging/config access
from flask import current_app

def get_current_weather(lat, lon, units='metric'):
    """
    Fetch current weather from OpenWeatherMap API.
    
    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        units (str): 'metric' (Celsius), 'imperial' (Fahrenheit), or 'standard' (Kelvin). Default: 'metric'.
    
    Returns:
        dict: Weather data {'temperature': 28.5, 'humidity': 75, 'wind_speed': 4.2, ...} or None on error.
    """
    api_key = app.config['WEATHER_API_KEY']
    base_url = app.config['WEATHER_BASE_URL']
    
    if not api_key:
        current_app.logger.error("Weather API key not configured")
        return None
    
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': units
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise error for bad status
        
        data = response.json()
        if data['cod'] != 200:
            current_app.logger.error(f"Weather API error: {data.get('message', 'Unknown')}")
            return None
        
        # Extract relevant fields
        weather = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'weather_description': data['weather'][0]['description'],
            'city': data.get('name', 'Unknown'),
            'country': data['sys']['country']
        }
        
        current_app.logger.info(f"Weather fetched for {lat}, {lon}: {weather['temperature']}°C")
        return weather
        
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Request error for weather API: {e}")
        return None
    except KeyError as e:
        current_app.logger.error(f"Unexpected API response format: {e}")
        return None