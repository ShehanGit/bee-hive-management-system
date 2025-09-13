import requests
import logging
from datetime import datetime
from typing import Dict, Optional, Any
from app import db
from app.models.weather import WeatherData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherService:
    """
    Service for fetching and managing weather data from OpenWeatherMap API
    """
    
    def __init__(self):
        self.api_key = "991f4245cb918f65ec5beec666b4802e"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.location = "Colombo,lk"
        self.latitude = 6.9271
        self.longitude = 79.8612
        
    def fetch_weather_data(self) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data from OpenWeatherMap API
        
        Returns:
            Dict containing weather data or None if fetch fails
        """
        try:
            params = {
                "lat": self.latitude,
                "lon": self.longitude,
                "appid": self.api_key,
                "units": "metric"  # Use Celsius for temperature
            }
            
            logger.info(f"Fetching weather data for coordinates: {self.latitude}, {self.longitude}")
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Successfully fetched weather data from OpenWeatherMap")
            
            return {
                "timestamp": datetime.utcnow(),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "light_intensity": data.get("visibility", 0) / 100,  # Convert visibility to percentage
                "rainfall": data.get("rain", {}).get("1h", 0),
                "weather_description": data["weather"][0]["description"],
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility", 0)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while fetching weather data: {str(e)}")
            return None
        except KeyError as e:
            logger.error(f"Missing key in weather API response: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching weather data: {str(e)}")
            return None
    
    def save_weather_data(self, weather_data: Dict[str, Any]) -> Optional[WeatherData]:
        """
        Save weather data to the database
        
        Args:
            weather_data: Dictionary containing weather data
            
        Returns:
            WeatherData instance if saved successfully, None otherwise
        """
        try:
            weather_record = WeatherData(
                timestamp=weather_data["timestamp"],
                temperature=weather_data["temperature"],
                humidity=weather_data["humidity"],
                wind_speed=weather_data["wind_speed"],
                light_intensity=weather_data["light_intensity"],
                rainfall=weather_data["rainfall"],
                weather_description=weather_data["weather_description"],
                pressure=weather_data["pressure"],
                visibility=weather_data["visibility"]
            )
            
            db.session.add(weather_record)
            db.session.commit()
            
            logger.info(f"Successfully saved weather data: {weather_record.temperature}°C, {weather_record.humidity}% humidity")
            return weather_record
            
        except Exception as e:
            logger.error(f"Error saving weather data to database: {str(e)}")
            db.session.rollback()
            return None
    
    def fetch_and_save_weather(self) -> bool:
        """
        Fetch weather data from API and save to database
        
        Returns:
            True if successful, False otherwise
        """
        try:
            weather_data = self.fetch_weather_data()
            if weather_data is None:
                logger.warning("Failed to fetch weather data from API")
                return False
            
            weather_record = self.save_weather_data(weather_data)
            if weather_record is None:
                logger.warning("Failed to save weather data to database")
                return False
            
            logger.info("Weather data fetch and save completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error in fetch_and_save_weather: {str(e)}")
            return False
    
    def get_latest_weather(self) -> Optional[WeatherData]:
        """
        Get the most recent weather data from database
        
        Returns:
            Latest WeatherData instance or None
        """
        try:
            return WeatherData.get_latest()
        except Exception as e:
            logger.error(f"Error getting latest weather data: {str(e)}")
            return None
    
    def get_historical_weather(self, hours: int = 24) -> list:
        """
        Get historical weather data from database
        
        Args:
            hours: Number of hours of historical data to retrieve
            
        Returns:
            List of WeatherData instances
        """
        try:
            return WeatherData.get_historical_data(hours)
        except Exception as e:
            logger.error(f"Error getting historical weather data: {str(e)}")
            return []

# Create a singleton instance
weather_service = WeatherService()

