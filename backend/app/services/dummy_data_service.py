import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class DummyDataService:
    """
    Generate realistic dummy data for bee hive monitoring
    """
    
    def __init__(self):
        self.data_history = []  # Store generated data for consistency
        self.max_history = 1000
        
        # Baseline values for normal hive conditions
        self.baseline = {
            'weather_temperature': 28.0,
            'weather_humidity': 65.0,
            'weather_wind_speed': 12.0,
            'weather_light_intensity': 800.0,
            'weather_rainfall': 0.0,
            'sensor_temperature': 27.5,
            'sensor_humidity': 68.0,
            'sensor_sound': 65.0,
            'sensor_weight': 45.0
        }
        
        # Threat scenarios for realistic variation
        self.current_scenario = "normal"
        self.scenario_start_time = datetime.now()
        
    def get_latest_synchronized_data(self, hive_id: int = 1) -> Dict[str, Any]:
        """
        Generate latest synchronized data point
        
        Args:
            hive_id: Hive ID
            
        Returns:
            Dict with synchronized sensor and weather data
        """
        data = self._generate_data_point(hive_id)
        self._add_to_history(data)
        
        logger.info(f"Generated dummy data: Temp={data['weather_temperature']:.1f}°C, "
                   f"Sound={data['sensor_sound']:.1f}dB, Scenario={self.current_scenario}")
        
        return data
    
    def get_synchronized_data(self, hive_id: int = 1, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Generate historical synchronized data
        
        Args:
            hive_id: Hive ID
            hours: Number of hours of historical data
            
        Returns:
            List of data points
        """
        data_points = []
        current_time = datetime.now()
        
        # Generate data points every 5 minutes for the specified duration
        num_points = hours * 12  # 12 points per hour (every 5 minutes)
        
        for i in range(num_points):
            timestamp = current_time - timedelta(minutes=i * 5)
            data = self._generate_data_point(hive_id, timestamp)
            data_points.append(data)
        
        # Reverse to get chronological order
        data_points.reverse()
        
        logger.info(f"Generated {len(data_points)} historical data points for {hours} hours")
        
        return data_points
    
    def _generate_data_point(self, hive_id: int, timestamp: datetime = None) -> Dict[str, Any]:
        """
        Generate a single data point with realistic variations
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        # Update scenario periodically (change every 30-60 minutes)
        self._update_scenario()
        
        # Base values with scenario-specific variations
        data = {
            'id': random.randint(1, 10000),
            'hive_id': hive_id,
            'collection_timestamp': timestamp.isoformat(),
            
            # Weather data
            'weather_temperature': self._get_weather_temperature(timestamp),
            'weather_humidity': self._get_weather_humidity(),
            'weather_wind_speed': self._get_weather_wind_speed(),
            'weather_light_intensity': self._get_light_intensity(timestamp),
            'weather_rainfall': self._get_rainfall(),
            
            # Sensor data
            'sensor_temperature': self._get_sensor_temperature(),
            'sensor_humidity': self._get_sensor_humidity(),
            'sensor_sound': self._get_sensor_sound(),
            'sensor_weight': self._get_sensor_weight(),
            
            # Metadata
            'weather_data_id': random.randint(1, 1000),
            'sensor_data_count': 4,
            'collection_success': True,
            'api_usage_weather_calls': 1,
            'api_usage_adafruit_calls': 4
        }
        
        return data
    
    def _update_scenario(self):
        """Update current threat scenario based on time"""
        elapsed = (datetime.now() - self.scenario_start_time).total_seconds() / 60
        
        # Change scenario every 30-60 minutes
        if elapsed > random.uniform(30, 60):
            scenarios = ["normal", "normal", "normal", "hot_day", "wax_moth", "predator_alert", "rainy"]
            self.current_scenario = random.choice(scenarios)
            self.scenario_start_time = datetime.now()
            logger.info(f"🔄 Scenario changed to: {self.current_scenario}")
    
    def _get_weather_temperature(self, timestamp: datetime) -> float:
        """Generate weather temperature with daily pattern"""
        hour = timestamp.hour
        
        # Daily temperature pattern (cooler at night, warmer during day)
        base_temp = self.baseline['weather_temperature']
        
        if 6 <= hour < 12:  # Morning warm-up
            temp = base_temp + (hour - 6) * 1.5
        elif 12 <= hour < 16:  # Peak heat
            temp = base_temp + 9 + random.uniform(-2, 3)
        elif 16 <= hour < 20:  # Evening cool-down
            temp = base_temp + 6 - (hour - 16) * 1.5
        else:  # Night
            temp = base_temp - 3 + random.uniform(-2, 1)
        
        # Scenario adjustments
        if self.current_scenario == "hot_day":
            temp += random.uniform(3, 6)
        elif self.current_scenario == "rainy":
            temp -= random.uniform(2, 4)
        
        return round(max(20.0, min(temp + random.uniform(-1, 1), 42.0)), 2)
    
    def _get_weather_humidity(self) -> float:
        """Generate weather humidity"""
        humidity = self.baseline['weather_humidity']
        
        if self.current_scenario == "hot_day":
            humidity -= random.uniform(10, 20)
        elif self.current_scenario == "rainy":
            humidity += random.uniform(15, 25)
        
        return round(max(30.0, min(humidity + random.uniform(-5, 5), 95.0)), 2)
    
    def _get_weather_wind_speed(self) -> float:
        """Generate wind speed"""
        wind = self.baseline['weather_wind_speed']
        
        if self.current_scenario == "rainy":
            wind += random.uniform(5, 15)
        
        return round(max(0.0, wind + random.uniform(-3, 3)), 2)
    
    def _get_light_intensity(self, timestamp: datetime) -> float:
        """Generate light intensity based on time of day"""
        hour = timestamp.hour
        
        if 6 <= hour < 18:  # Daylight
            base = 800 + (12 - abs(hour - 12)) * 50
        else:  # Night
            base = 50
        
        if self.current_scenario == "rainy":
            base *= 0.4
        
        return round(max(0.0, base + random.uniform(-100, 100)), 2)
    
    def _get_rainfall(self) -> float:
        """Generate rainfall"""
        if self.current_scenario == "rainy":
            return round(random.uniform(2, 15), 2)
        elif random.random() < 0.05:  # 5% chance of light rain
            return round(random.uniform(0.1, 1.5), 2)
        return 0.0
    
    def _get_sensor_temperature(self) -> float:
        """Generate sensor temperature (inside hive)"""
        temp = self.baseline['sensor_temperature']
        
        if self.current_scenario == "hot_day":
            temp += random.uniform(2, 5)
        
        return round(max(20.0, min(temp + random.uniform(-1.5, 1.5), 38.0)), 2)
    
    def _get_sensor_humidity(self) -> float:
        """Generate sensor humidity (inside hive)"""
        humidity = self.baseline['sensor_humidity']
        
        if self.current_scenario == "wax_moth":
            humidity += random.uniform(5, 10)  # Wax moths like humid conditions
        
        return round(max(40.0, min(humidity + random.uniform(-3, 3), 85.0)), 2)
    
    def _get_sensor_sound(self) -> float:
        """Generate sensor sound level with threat variations"""
        sound = self.baseline['sensor_sound']
        
        if self.current_scenario == "predator_alert":
            # Sudden spike in sound indicates agitation
            sound += random.uniform(15, 30)
        elif self.current_scenario == "wax_moth":
            # Slightly elevated sound from increased activity
            sound += random.uniform(5, 12)
        
        return round(max(40.0, min(sound + random.uniform(-5, 5), 95.0)), 2)
    
    def _get_sensor_weight(self) -> float:
        """Generate hive weight"""
        weight = self.baseline['sensor_weight']
        
        # Gradual weight increase during active season
        weight += random.uniform(-0.5, 1.0)
        
        if self.current_scenario == "predator_alert":
            # Weight drop from bees consuming honey in panic
            weight -= random.uniform(0.5, 2.0)
        
        return round(max(30.0, min(weight, 70.0)), 2)
    
    def _add_to_history(self, data: Dict[str, Any]):
        """Add data point to history for consistency"""
        self.data_history.append(data)
        
        if len(self.data_history) > self.max_history:
            self.data_history = self.data_history[-self.max_history:]
    
    def collect_synchronized_data(self, hive_id: int = 1) -> Dict[str, Any]:
        """
        Simulate data collection
        
        Returns:
            Collection result dict
        """
        data = self.get_latest_synchronized_data(hive_id)
        
        # Format as collection result
        result = {
            'collection_timestamp': data['collection_timestamp'],
            'hive_id': hive_id,
            'weather_data': {
                'id': data['weather_data_id'],
                'temperature': data['weather_temperature'],
                'humidity': data['weather_humidity'],
                'wind_speed': data['weather_wind_speed'],
                'light_intensity': data['weather_light_intensity'],
                'rainfall': data['weather_rainfall'],
                'timestamp': data['collection_timestamp']
            },
            'sensor_data': [
                {'sensor_type': 'temperature', 'value': data['sensor_temperature'], 'timestamp': data['collection_timestamp']},
                {'sensor_type': 'humidity', 'value': data['sensor_humidity'], 'timestamp': data['collection_timestamp']},
                {'sensor_type': 'sound', 'value': data['sensor_sound'], 'timestamp': data['collection_timestamp']},
                {'sensor_type': 'weight', 'value': data['sensor_weight'], 'timestamp': data['collection_timestamp']}
            ],
            'success': True,
            'errors': [],
            'api_usage': {
                'weather_calls': 1,
                'adafruit_calls': 4
            }
        }
        
        return result
    
    def force_scenario(self, scenario: str):
        """
        Force a specific threat scenario for testing
        
        Args:
            scenario: One of: "normal", "hot_day", "wax_moth", "predator_alert", "rainy"
        """
        valid_scenarios = ["normal", "hot_day", "wax_moth", "predator_alert", "rainy"]
        
        if scenario in valid_scenarios:
            self.current_scenario = scenario
            self.scenario_start_time = datetime.now()
            logger.info(f"🔧 Forced scenario: {scenario}")
        else:
            logger.warning(f"Invalid scenario: {scenario}. Valid: {valid_scenarios}")

# Create singleton instance
dummy_data_service = DummyDataService()