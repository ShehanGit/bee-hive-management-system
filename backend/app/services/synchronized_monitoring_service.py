import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from app import db
from app.models.weather import WeatherData
from app.models.sensor_data import SensorData
from app.models.hive import Hive

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SynchronizedMonitoringService:
    """
    Service for synchronized collection of weather and sensor data
    with perfect timestamp alignment for future prediction models
    """
    
    def __init__(self):
        from app.config import Config
        
        # Weather API configuration
        self.weather_api_key = Config.WEATHER_API_KEY
        self.weather_base_url = Config.WEATHER_BASE_URL
        self.weather_latitude = Config.DEFAULT_LATITUDE
        self.weather_longitude = Config.DEFAULT_LONGITUDE
        
        # Adafruit IO configuration (using centralized config)
        self.adafruit_username = Config.ADAFRUIT_USERNAME
        self.adafruit_key = Config.ADAFRUIT_KEY
        self.adafruit_base_url = Config.ADAFRUIT_BASE_URL
        self.adafruit_headers = {"X-AIO-Key": self.adafruit_key}
        
        # Collection configuration
        self.collection_interval_minutes = 1
        self.last_collection_time = None
        
        # API rate limiting
        self.weather_calls_made = 0
        self.weather_calls_reset_time = datetime.now()
        self.adafruit_calls_made = 0
        self.adafruit_calls_reset_time = datetime.now()
    
    def collect_synchronized_data(self, hive_id: int = 1) -> Dict[str, Any]:
        """
        Collect both weather and sensor data with synchronized timestamp
        
        Args:
            hive_id: The hive ID to collect data for
            
        Returns:
            Dict containing synchronized collection results
        """
        try:
            # Ensure hive exists, create if it doesn't
            hive = self._ensure_hive_exists(hive_id)
            
            # Use local timestamp for all data in this collection cycle
            collection_timestamp = datetime.now()
            
            logger.info(f"Starting synchronized data collection at {collection_timestamp}")
            
            results = {
                "collection_timestamp": collection_timestamp.isoformat(),
                "hive_id": hive_id,
                "weather_data": None,
                "sensor_data": [],
                "success": False,
                "errors": [],
                "api_usage": {
                    "weather_calls": 0,
                    "adafruit_calls": 0
                }
            }
            
            # 1. Collect weather data
            try:
                weather_data = self._fetch_weather_data(hive_id)
                if weather_data:
                    # Override timestamp with collection timestamp
                    weather_data["timestamp"] = collection_timestamp
                    
                    # Save weather data (only specified fields)
                    weather_record = WeatherData(
                        timestamp=weather_data["timestamp"],
                        temperature=weather_data["temperature"],
                        humidity=weather_data["humidity"],
                        wind_speed=weather_data["wind_speed"],
                        light_intensity=weather_data["light_intensity"],
                        rainfall=weather_data["rainfall"]
                    )
                    
                    db.session.add(weather_record)
                    results["weather_data"] = weather_record.to_dict()
                    results["api_usage"]["weather_calls"] = 1
                    logger.info("Weather data collected and saved successfully")
                else:
                    results["errors"].append("Failed to fetch weather data")
                    
            except Exception as e:
                error_msg = f"Weather data collection error: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
            
            # 2. Collect sensor data with synchronized timestamp
            try:
                sensor_values = self._fetch_sensor_data_from_adafruit(hive_id)
                results["api_usage"]["adafruit_calls"] = len(sensor_values)
                
                for sensor_type, value in sensor_values.items():
                    if value is not None:
                        # Handle non-numeric values (like status)
                        if isinstance(value, str):
                            # For string values, we'll store them in the synchronized_data table
                            # but skip the sensor_data table since it expects float values
                            results["sensor_data"].append({
                                "sensor_type": sensor_type,
                                "value": value,
                                "timestamp": collection_timestamp.isoformat(),
                                "is_string": True
                            })
                        else:
                            # For numeric values, store in both tables
                            sensor_record = SensorData(
                                hive_id=hive_id,
                                sensor_type=sensor_type,
                                sensor_value=value,
                                created_at=collection_timestamp  # Use synchronized timestamp
                            )
                            
                            db.session.add(sensor_record)
                            results["sensor_data"].append({
                                "sensor_type": sensor_type,
                                "value": value,
                                "timestamp": collection_timestamp.isoformat(),
                                "is_string": False
                            })
                
                logger.info(f"Collected {len(results['sensor_data'])} sensor readings")
                
            except Exception as e:
                error_msg = f"Sensor data collection error: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
            
            # 3. Create SynchronizedData record
            try:
                from app.models.synchronized_data import SynchronizedData
                
                # Extract sensor values for SynchronizedData (only Temperature, Humidity, Sound, Weight)
                sensor_data_dict = {}
                for sensor in results["sensor_data"]:
                    sensor_type = sensor["sensor_type"]
                    value = sensor["value"]
                    
                    if sensor_type == "temperature":
                        sensor_data_dict["sensor_temperature"] = value if not sensor.get("is_string", False) else None
                    elif sensor_type == "humidity":
                        sensor_data_dict["sensor_humidity"] = value if not sensor.get("is_string", False) else None
                    elif sensor_type == "sound":
                        sensor_data_dict["sensor_sound"] = value if not sensor.get("is_string", False) else None
                    elif sensor_type == "weight":
                        sensor_data_dict["sensor_weight"] = value if not sensor.get("is_string", False) else None
                
                # Create SynchronizedData record (only specified fields)
                synchronized_record = SynchronizedData(
                    collection_timestamp=collection_timestamp,
                    hive_id=hive_id,
                    # Weather data (only Temperature, Humidity, Wind Speed, Light Intensity, Rainfall)
                    weather_temperature=results["weather_data"]["temperature"] if results["weather_data"] else None,
                    weather_humidity=results["weather_data"]["humidity"] if results["weather_data"] else None,
                    weather_wind_speed=results["weather_data"]["wind_speed"] if results["weather_data"] else None,
                    weather_light_intensity=results["weather_data"]["light_intensity"] if results["weather_data"] else None,
                    weather_rainfall=results["weather_data"]["rainfall"] if results["weather_data"] else None,
                    # Sensor data (only Temperature, Humidity, Sound, Weight)
                    **sensor_data_dict,
                    # Metadata
                    weather_data_id=results["weather_data"]["id"] if results["weather_data"] else None,
                    sensor_data_count=len([s for s in results["sensor_data"] if not s.get("is_string", False)]),
                    collection_success=True,
                    api_usage_weather_calls=results["api_usage"]["weather_calls"],
                    api_usage_adafruit_calls=results["api_usage"]["adafruit_calls"]
                )
                
                # Calculate threat detection fields from existing data
                synchronized_record.calculate_threat_detection_fields()
                
                db.session.add(synchronized_record)
                
            except Exception as e:
                error_msg = f"SynchronizedData creation error: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
            
            # 4. Commit all data together
            try:
                db.session.commit()
                results["success"] = True
                self.last_collection_time = collection_timestamp
                
                # Update API usage tracking
                self._update_api_usage_tracking(results["api_usage"])
                
                logger.info("Synchronized data collection completed successfully")
                
            except Exception as e:
                db.session.rollback()
                error_msg = f"Database commit error: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
            
            return results
            
        except Exception as e:
            logger.error(f"Synchronized data collection failed: {str(e)}")
            return {
                "collection_timestamp": datetime.utcnow().isoformat(),
                "hive_id": hive_id,
                "success": False,
                "errors": [f"Collection failed: {str(e)}"],
                "api_usage": {"weather_calls": 0, "adafruit_calls": 0}
            }
    
    def _ensure_hive_exists(self, hive_id: int) -> Hive:
        """
        Ensure a hive exists, create if it doesn't with default location
        
        Args:
            hive_id: The hive ID to check/create
            
        Returns:
            Hive instance (existing or newly created)
        """
        try:
            hive = Hive.query.get(hive_id)
            
            if not hive:
                # Create new hive with default values
                hive = Hive(
                    id=hive_id,
                    name=f"Hive {hive_id}",
                    location_lat=self.weather_latitude,
                    location_lng=self.weather_longitude,
                    created_at=datetime.now()
                )
                db.session.add(hive)
                db.session.commit()
                logger.info(f"Created new hive {hive_id} with default location (Colombo, Sri Lanka)")
            else:
                # Update default location if not set
                if hive.location_lat is None or hive.location_lng is None:
                    hive.location_lat = self.weather_latitude
                    hive.location_lng = self.weather_longitude
                    db.session.commit()
                    logger.info(f"Updated hive {hive_id} with default location (Colombo, Sri Lanka)")
            
            return hive
            
        except Exception as e:
            logger.error(f"Error ensuring hive exists: {str(e)}")
            # Return a minimal hive object if database operations fail
            return Hive(
                id=hive_id,
                name=f"Hive {hive_id}",
                location_lat=self.weather_latitude,
                location_lng=self.weather_longitude,
                created_at=datetime.now()
            )

    def _fetch_weather_data(self, hive_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data from OpenWeatherMap API
        
        Args:
            hive_id: Hive ID whose location should be used
        
        Returns:
            Dict containing weather data or None if fetch fails
        """
        try:
            # Check rate limits
            if not self._check_weather_rate_limit():
                logger.warning("Weather API rate limit reached, skipping collection")
                return None
            
            # Resolve coordinates from hive
            latitude = self.weather_latitude
            longitude = self.weather_longitude
            try:
                hive = Hive.query.filter_by(id=hive_id).first()
                if hive and hive.location_lat is not None and hive.location_lng is not None:
                    latitude = hive.location_lat
                    longitude = hive.location_lng
                    logger.info(f"Using hive {hive_id} coordinates for weather: lat={latitude}, lon={longitude}")
                else:
                    logger.info(
                        f"Hive {hive_id} has no coordinates; falling back to default lat={latitude}, lon={longitude}"
                    )
            except Exception as e:
                logger.warning(f"Could not resolve hive coordinates (id={hive_id}), using defaults: {str(e)}")
            
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.weather_api_key,
                "units": "metric"
            }
            
            logger.info(f"Fetching weather data for coordinates: {latitude}, {longitude}")
            response = requests.get(self.weather_base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            logger.info("Successfully fetched weather data from OpenWeatherMap")
            
            return {
                "timestamp": datetime.now(),
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"] * 3.6,  # Convert m/s to km/h
                "light_intensity": data.get("visibility", 0),  # Use visibility as light intensity in lux
                "rainfall": data.get("rain", {}).get("1h", 0)
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
    
    def _fetch_sensor_data_from_adafruit(self, hive_id: int) -> Dict[str, Optional[float]]:
        """
        Fetch sensor data from Adafruit IO feeds
        
        Args:
            hive_id: The hive ID to fetch data for
            
        Returns:
            Dict mapping sensor types to their values
        """
        sensor_values = {}
        
        try:
            # Check rate limits
            if not self._check_adafruit_rate_limit():
                logger.warning("Adafruit API rate limit reached, using fallback data")
                return self._get_fallback_sensor_data()
            
            # Define sensor feeds for this hive (only Temperature, Humidity, Sound, Weight)
            sensor_feeds = {
                'temperature': f'hive-{hive_id}-temperature',
                'humidity': f'hive-{hive_id}-humidity',
                'sound': f'hive-{hive_id}-sound',
                'weight': f'hive-{hive_id}-weight'
            }
            
            for sensor_type, feed_name in sensor_feeds.items():
                try:
                    value = self._fetch_adafruit_feed_value(feed_name)
                    sensor_values[sensor_type] = value
                    
                except Exception as e:
                    logger.error(f"Error fetching {sensor_type} from {feed_name}: {str(e)}")
                    sensor_values[sensor_type] = None
            
            logger.info(f"Successfully fetched {len([v for v in sensor_values.values() if v is not None])} sensor values")
            
        except Exception as e:
            logger.error(f"Error fetching sensor data from Adafruit: {str(e)}")
            # Return fallback data on error
            sensor_values = self._get_fallback_sensor_data()
        
        return sensor_values
    
    def _fetch_adafruit_feed_value(self, feed_name: str) -> Optional[float]:
        """
        Fetch latest value from a specific Adafruit feed
        
        Args:
            feed_name: Name of the Adafruit feed
            
        Returns:
            Feed value or None if fetch fails
        """
        try:
            url = f"{self.adafruit_base_url}/{feed_name}/data?limit=1"
            response = requests.get(url, headers=self.adafruit_headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data and len(data) > 0:
                value = data[0].get("value")
                # Try to convert to float, keep as string if not numeric
                try:
                    return float(value) if value is not None else None
                except (ValueError, TypeError):
                    return value
            else:
                logger.warning(f"No data available for feed {feed_name}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching feed {feed_name}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error fetching feed {feed_name}: {str(e)}")
            return None
    
    def _get_fallback_sensor_data(self) -> Dict[str, Optional[float]]:
        """
        Get fallback sensor data when API calls fail
        
        Returns:
            Dict with fallback sensor values (only Temperature, Humidity, Sound, Weight)
        """
        return {
            "temperature": 25.0,  # Default temperature
            "humidity": 60.0,     # Default humidity
            "sound": 40.0,        # Default sound level
            "weight": 50.0        # Default weight
        }
    
    def _check_weather_rate_limit(self) -> bool:
        """
        Check if weather API rate limit allows another call
        
        Returns:
            True if rate limit allows, False otherwise
        """
        now = datetime.now()
        
        # Reset counter every minute
        if (now - self.weather_calls_reset_time).total_seconds() >= 60:
            self.weather_calls_made = 0
            self.weather_calls_reset_time = now
        
        # Check if under limit (60 calls per minute)
        if self.weather_calls_made >= 60:
            return False
        
        return True
    
    def _check_adafruit_rate_limit(self) -> bool:
        """
        Check if Adafruit API rate limit allows another call
        
        Returns:
            True if rate limit allows, False otherwise
        """
        now = datetime.now()
        
        # Reset counter every minute
        if (now - self.adafruit_calls_reset_time).total_seconds() >= 60:
            self.adafruit_calls_made = 0
            self.adafruit_calls_reset_time = now
        
        # Check if under limit (30 calls per minute)
        if self.adafruit_calls_made >= 30:
            return False
        
        return True
    
    def _update_api_usage_tracking(self, api_usage: Dict[str, int]):
        """
        Update API usage tracking counters
        
        Args:
            api_usage: Dict containing API call counts
        """
        self.weather_calls_made += api_usage.get("weather_calls", 0)
        self.adafruit_calls_made += api_usage.get("adafruit_calls", 0)
    
    def get_synchronized_data(self, hive_id: int = 1, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get synchronized sensor and weather data for analysis
        
        Args:
            hive_id: The hive ID to get data for
            hours: Number of hours of historical data
            
        Returns:
            List of synchronized data points
        """
        try:
            from app.models.synchronized_data import SynchronizedData
            
            since_time = datetime.now() - timedelta(hours=hours)
            
            # Get synchronized data from the SynchronizedData table
            synchronized_records = SynchronizedData.query.filter(
                SynchronizedData.hive_id == hive_id,
                SynchronizedData.collection_timestamp >= since_time
            ).order_by(SynchronizedData.collection_timestamp.desc()).all()
            
            return [record.to_dict() for record in synchronized_records]
             
        except Exception as e:
            logger.error(f"Error getting synchronized data: {str(e)}")
            return []

    def get_latest_synchronized_data(self, hive_id: int = 1) -> Optional[Dict[str, Any]]:
        """
        Get the latest synchronized data for a hive
        
        Args:
            hive_id: The hive ID to get data for
            
        Returns:
            Latest synchronized data point or None
        """
        try:
            from app.models.synchronized_data import SynchronizedData
            
            latest_record = SynchronizedData.query.filter(
                SynchronizedData.hive_id == hive_id
            ).order_by(SynchronizedData.collection_timestamp.desc()).first()
            
            return latest_record.to_dict() if latest_record else None
            
        except Exception as e:
            logger.error(f"Error getting latest synchronized data: {str(e)}")
            return None

    def get_data_alignment_stats(self, hive_id: int = 1, hours: int = 24) -> Dict[str, Any]:
        """
        Get statistics about data alignment between sensor and weather data
        
        Args:
            hive_id: The hive ID to get stats for
            hours: Number of hours of historical data
            
        Returns:
            Dict containing alignment statistics
        """
        try:
            from app.models.synchronized_data import SynchronizedData
            
            since_time = datetime.now() - timedelta(hours=hours)
            
            # Get synchronized data records
            records = SynchronizedData.query.filter(
                SynchronizedData.hive_id == hive_id,
                SynchronizedData.collection_timestamp >= since_time
            ).all()
            
            if not records:
                return {
                    'error': f'No synchronized data found for hive {hive_id} in the last {hours} hours'
                }
            
            total_records = len(records)
            successful_collections = len([r for r in records if r.collection_success])
            
            # Calculate alignment statistics
            weather_data_count = len([r for r in records if r.weather_temperature is not None])
            sensor_data_count = len([r for r in records if r.sensor_temperature is not None])
            
            # Calculate average sensor data count per record
            avg_sensor_data = sum(r.sensor_data_count for r in records) / total_records if total_records > 0 else 0
            
            return {
                'total_records': total_records,
                'successful_collections': successful_collections,
                'success_rate': (successful_collections / total_records * 100) if total_records > 0 else 0,
                'weather_data_points': weather_data_count,
                'sensor_data_points': sensor_data_count,
                'average_sensor_data_per_record': round(avg_sensor_data, 2),
                'perfect_alignment_rate': (weather_data_count / total_records * 100) if total_records > 0 else 0,
                'time_range': {
                    'start': min(r.collection_timestamp for r in records).isoformat(),
                    'end': max(r.collection_timestamp for r in records).isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting data alignment stats: {str(e)}")
            return {
                'error': f'Failed to get alignment statistics: {str(e)}'
            }
    
    def update_hive_location(self, hive_id: int, name: str = None, latitude: float = None, longitude: float = None) -> Dict[str, Any]:
        """
        Update hive location and name
        
        Args:
            hive_id: The hive ID to update
            name: New hive name (optional)
            latitude: New latitude (optional)
            longitude: New longitude (optional)
            
        Returns:
            Dict containing update results
        """
        try:
            hive = Hive.query.get(hive_id)
            
            if not hive:
                return {
                    "success": False,
                    "error": f"Hive {hive_id} not found"
                }
            
            # Update fields if provided
            if name is not None:
                hive.name = name
                logger.info(f"Updated hive {hive_id} name to: {name}")
            
            if latitude is not None:
                hive.location_lat = latitude
                logger.info(f"Updated hive {hive_id} latitude to: {latitude}")
            
            if longitude is not None:
                hive.location_lng = longitude
                logger.info(f"Updated hive {hive_id} longitude to: {longitude}")
            
            db.session.commit()
            
            return {
                "success": True,
                "message": f"Hive {hive_id} updated successfully",
                "hive": {
                    "id": hive.id,
                    "name": hive.name,
                    "location_lat": hive.location_lat,
                    "location_lng": hive.location_lng
                }
            }
            
        except Exception as e:
            logger.error(f"Error updating hive {hive_id}: {str(e)}")
            db.session.rollback()
            return {
                "success": False,
                "error": f"Failed to update hive: {str(e)}"
            }

    def get_collection_status(self) -> Dict[str, Any]:
        """
        Get current collection service status
        
        Returns:
            Dict containing service status information
        """
        return {
            "service_status": "active",
            "collection_interval_minutes": self.collection_interval_minutes,
            "last_collection_time": self.last_collection_time.isoformat() if self.last_collection_time else None,
            "api_usage": {
                "weather_calls_made": self.weather_calls_made,
                "weather_calls_remaining": max(0, 60 - self.weather_calls_made),
                "adafruit_calls_made": self.adafruit_calls_made,
                "adafruit_calls_remaining": max(0, 30 - self.adafruit_calls_made)
            },
            "rate_limit_reset_times": {
                "weather": self.weather_calls_reset_time.isoformat(),
                "adafruit": self.adafruit_calls_reset_time.isoformat()
            }
        }

# Create singleton instance
synchronized_monitoring_service = SynchronizedMonitoringService()
