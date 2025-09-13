import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from app import db
from app.models.weather import WeatherData
from app.models.sensor_data import SensorData
from app.services.weather_service import weather_service
from app.services.iot_integration_service import fetch_and_save_iot_data

logger = logging.getLogger(__name__)

class SynchronizedDataService:
    """
    Service to collect and synchronize sensor and weather data with aligned timestamps
    """
    
    def __init__(self):
        self.collection_interval_minutes = 5  # Collect every 5 minutes for better alignment
        self.last_collection_time = None
    
    def collect_synchronized_data(self, hive_id: int = 1) -> Dict:
        """
        Collect both sensor and weather data with synchronized timestamps
        
        Args:
            hive_id: The hive ID to collect data for
            
        Returns:
            Dict containing collection results and synchronized data
        """
        try:
            # Use a single timestamp for all data in this collection cycle
            collection_timestamp = datetime.utcnow()
            
            logger.info(f"Starting synchronized data collection at {collection_timestamp}")
            
            results = {
                "collection_timestamp": collection_timestamp.isoformat(),
                "hive_id": hive_id,
                "weather_data": None,
                "sensor_data": [],
                "success": False,
                "errors": []
            }
            
            # 1. Collect weather data
            try:
                weather_data = weather_service.fetch_weather_data()
                if weather_data:
                    # Override timestamp with collection timestamp
                    weather_data["timestamp"] = collection_timestamp
                    
                    # Save weather data
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
                    results["weather_data"] = weather_record.to_dict()
                    logger.info("Weather data collected and saved successfully")
                else:
                    results["errors"].append("Failed to fetch weather data")
                    
            except Exception as e:
                error_msg = f"Weather data collection error: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
            
            # 2. Collect sensor data with synchronized timestamp
            try:
                # Get sensor data from IoT device
                sensor_types = ["temperature", "humidity", "light", "gps_lat", "gps_lng"]
                sensor_values = self._fetch_sensor_values()
                
                for sensor_type, value in sensor_values.items():
                    if value is not None:
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
                            "timestamp": collection_timestamp.isoformat()
                        })
                
                logger.info(f"Collected {len(results['sensor_data'])} sensor readings")
                
            except Exception as e:
                error_msg = f"Sensor data collection error: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)
            
            # 3. Commit all data together
            try:
                db.session.commit()
                results["success"] = True
                self.last_collection_time = collection_timestamp
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
                "errors": [f"Collection failed: {str(e)}"]
            }
    
    def _fetch_sensor_values(self) -> Dict[str, Optional[float]]:
        """
        Fetch sensor values from IoT device
        
        Returns:
            Dict mapping sensor types to their values
        """
        sensor_values = {}
        
        try:
            # This would normally fetch from IoT device
            # For now, return mock data that matches weather conditions
            sensor_values = {
                "temperature": 26.0,  # Match weather temperature
                "humidity": 65.0,     # Match weather humidity
                "light": 85.0,        # Match weather light intensity
                "gps_lat": 6.9271,    # Colombo coordinates
                "gps_lng": 79.8612
            }
            
        except Exception as e:
            logger.error(f"Error fetching sensor values: {str(e)}")
            # Return None values on error
            sensor_values = {
                "temperature": None,
                "humidity": None,
                "light": None,
                "gps_lat": None,
                "gps_lng": None
            }
        
        return sensor_values
    
    def get_synchronized_data(self, hive_id: int = 1, hours: int = 24) -> List[Dict]:
        """
        Get synchronized sensor and weather data for analysis
        
        Args:
            hive_id: The hive ID to get data for
            hours: Number of hours of historical data
            
        Returns:
            List of synchronized data points
        """
        try:
            since_time = datetime.utcnow() - timedelta(hours=hours)
            
            # Get weather data
            weather_data = WeatherData.query.filter(
                WeatherData.timestamp >= since_time
            ).order_by(WeatherData.timestamp.asc()).all()
            
            # Get sensor data
            sensor_data = SensorData.query.filter(
                SensorData.hive_id == hive_id,
                SensorData.created_at >= since_time
            ).order_by(SensorData.created_at.asc()).all()
            
            # Group sensor data by timestamp
            sensor_groups = {}
            for sensor in sensor_data:
                timestamp_key = sensor.created_at.isoformat()
                if timestamp_key not in sensor_groups:
                    sensor_groups[timestamp_key] = {}
                sensor_groups[timestamp_key][sensor.sensor_type] = sensor.sensor_value
            
            # Create synchronized data points
            synchronized_data = []
            
            for weather in weather_data:
                weather_timestamp = weather.timestamp.isoformat()
                
                # Find closest sensor data (within 5 minutes)
                closest_sensors = None
                min_time_diff = float('inf')
                
                for sensor_timestamp, sensors in sensor_groups.items():
                    time_diff = abs((weather.timestamp - datetime.fromisoformat(sensor_timestamp)).total_seconds())
                    if time_diff < min_time_diff and time_diff <= 300:  # 5 minutes
                        min_time_diff = time_diff
                        closest_sensors = sensors
                
                data_point = {
                    "timestamp": weather_timestamp,
                    "weather": weather.to_dict(),
                    "sensors": closest_sensors or {},
                    "time_alignment_seconds": min_time_diff if closest_sensors else None
                }
                
                synchronized_data.append(data_point)
            
            return synchronized_data
            
        except Exception as e:
            logger.error(f"Error getting synchronized data: {str(e)}")
            return []
    
    def get_data_alignment_stats(self, hive_id: int = 1, hours: int = 24) -> Dict:
        """
        Get statistics about data alignment between sensor and weather data
        
        Returns:
            Dict containing alignment statistics
        """
        try:
            synchronized_data = self.get_synchronized_data(hive_id, hours)
            
            if not synchronized_data:
                return {"error": "No synchronized data available"}
            
            time_diffs = [dp["time_alignment_seconds"] for dp in synchronized_data if dp["time_alignment_seconds"] is not None]
            
            if not time_diffs:
                return {"error": "No aligned data points found"}
            
            stats = {
                "total_data_points": len(synchronized_data),
                "aligned_data_points": len(time_diffs),
                "alignment_percentage": (len(time_diffs) / len(synchronized_data)) * 100,
                "average_time_difference_seconds": sum(time_diffs) / len(time_diffs),
                "min_time_difference_seconds": min(time_diffs),
                "max_time_difference_seconds": max(time_diffs),
                "perfect_alignment_count": len([td for td in time_diffs if td == 0]),
                "good_alignment_count": len([td for td in time_diffs if td <= 60]),  # Within 1 minute
                "poor_alignment_count": len([td for td in time_diffs if td > 300])   # More than 5 minutes
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating alignment stats: {str(e)}")
            return {"error": str(e)}

# Create singleton instance
synchronized_data_service = SynchronizedDataService()

