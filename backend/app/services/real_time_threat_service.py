import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
import numpy as np

logger = logging.getLogger(__name__)

class RealTimeThreatService:
    """
    Service to perform real-time threat detection on synchronized hive data
    """
    
    def __init__(self):
        self.last_analysis_time = None
        self.threat_history = []  # Store recent threats for trend analysis
        self.max_history_size = 100
        
    def analyze_synchronized_data(self, sync_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze synchronized data point and detect threats
        
        Args:
            sync_data: Dictionary from SynchronizedData.to_dict() or dummy data
            
        Returns:
            Dict containing threat analysis results or None if no analysis performed
        """
        try:
            # Import here to avoid circular dependencies
            from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat
            from app.ml_models.threat_detection.src.recommendation_service import get_recommendations
            from app.ml_models.threat_detection.src.alert_store import add_alert
            
            # Extract sensor and weather data
            if not sync_data:
                logger.warning("No synchronized data provided for analysis")
                return None
            
            # Build payload for ML model
            payload = self._build_prediction_payload(sync_data)
            
            if not payload:
                logger.warning("Could not build prediction payload - missing critical data")
                return None
            
            # Get threat prediction
            prediction = predict_threat(payload)
            
            threat_type = prediction["threat_type"]
            probability = prediction["probability"]
            used_features = prediction["used_features"]
            
            logger.info(f"Threat Detection: {threat_type} (probability: {probability:.3f})")
            
            # Determine severity based on threat type and probability
            severity = self._calculate_severity(threat_type, probability)
            
            # Get actionable recommendations
            recommendations = get_recommendations(threat_type)
            
            # Add severity to recommendations
            recommendations["severity"] = severity
            recommendations["probability"] = probability
            recommendations["detection_timestamp"] = sync_data.get("collection_timestamp")
            
            # Store alert in database if threat is significant
            if threat_type != "No_Threat" or probability > 0.3:
                alert = add_alert(
                    threat_type=threat_type,
                    probability=probability,
                    used_features=used_features,
                    recommendations=recommendations
                )
                
                logger.info(f"✅ Alert stored: {threat_type} with {severity} severity")
            else:
                alert = None
                logger.info(f"ℹ️ No threat detected (probability: {probability:.3f})")
            
            # Update threat history for trend analysis
            self._update_threat_history(threat_type, probability, sync_data.get("collection_timestamp"))
            
            # Build comprehensive result
            result = {
                "threat_type": threat_type,
                "probability": probability,
                "severity": severity,
                "recommendations": recommendations,
                "used_features": used_features,
                "timestamp": sync_data.get("collection_timestamp"),
                "hive_id": sync_data.get("hive_id"),
                "alert_stored": alert is not None,
                "alert_id": alert.get("timestamp") if alert else None
            }
            
            self.last_analysis_time = datetime.now()
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing synchronized data: {str(e)}")
            return None
    
    def _build_prediction_payload(self, sync_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Build prediction payload from synchronized data
        Maps database fields to ML model features
        
        Args:
            sync_data: Synchronized data dictionary
            
        Returns:
            Payload dict for ML model or None if critical data missing
        """
        try:
            # Extract timestamp
            timestamp = sync_data.get("collection_timestamp")
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            elif timestamp is None:
                timestamp = datetime.now()
            
            # Map database fields to model features
            payload = {
                # Weather features (from weather data)
                "weather_temp_c": sync_data.get("weather_temperature"),
                "weather_humidity_pct": sync_data.get("weather_humidity"),
                
                # Hive sensor features
                "hive_sound_db": sync_data.get("sensor_sound", 70.0),  # Default if not available
                "hive_sound_peak_freq": 200.0,  # Derived feature (we'll estimate from sound)
                
                # Vibration features (estimated from sound and weight changes)
                "vibration_hz": self._estimate_vibration(sync_data),
                "vibration_var": 10.0,  # Default variance
                
                # Timestamp for time-based features
                "timestamp": timestamp
            }
            
            # Check if critical weather data is available
            if payload["weather_temp_c"] is None or payload["weather_humidity_pct"] is None:
                logger.warning("Missing critical weather data")
                return None
            
            # Estimate peak frequency from sound level (heuristic)
            if payload["hive_sound_db"]:
                # Higher sound usually means higher frequency activity
                payload["hive_sound_peak_freq"] = 150 + (payload["hive_sound_db"] - 60) * 5
            
            return payload
            
        except Exception as e:
            logger.error(f"Error building prediction payload: {str(e)}")
            return None
    
    def _estimate_vibration(self, sync_data: Dict[str, Any]) -> float:
        """
        Estimate vibration frequency from available sensor data
        
        This is a heuristic estimation since we don't have direct vibration sensors.
        Uses sound level and weight changes as proxies.
        """
        sound_level = sync_data.get("sensor_sound", 70.0)
        
        # Base vibration correlates with sound activity
        # Normal hive: 180-220 Hz, Active: 220-280 Hz, Disturbed: >280 Hz
        base_vibration = 200.0
        
        # Adjust based on sound level
        if sound_level > 80:
            base_vibration += (sound_level - 80) * 2  # Higher sound = higher vibration
        elif sound_level < 60:
            base_vibration -= (60 - sound_level) * 1.5  # Lower sound = lower vibration
        
        return max(150.0, min(base_vibration, 350.0))  # Clamp to realistic range
    
    def _calculate_severity(self, threat_type: str, probability: float) -> str:
        """
        Calculate threat severity based on type and probability
        
        Returns: "Critical", "High", "Medium", "Low"
        """
        if threat_type == "No_Threat":
            return "Low"
        
        # Predator threats are always critical
        if threat_type == "Predator":
            if probability > 0.7:
                return "Critical"
            elif probability > 0.5:
                return "High"
            else:
                return "Medium"
        
        # Wax Moth threats
        if threat_type == "Wax_Moth":
            if probability > 0.8:
                return "High"
            elif probability > 0.6:
                return "Medium"
            else:
                return "Low"
        
        # Environmental threats
        if threat_type == "Environmental":
            if probability > 0.75:
                return "High"
            elif probability > 0.5:
                return "Medium"
            else:
                return "Low"
        
        # Default severity calculation
        if probability > 0.8:
            return "High"
        elif probability > 0.6:
            return "Medium"
        else:
            return "Low"
    
    def _update_threat_history(self, threat_type: str, probability: float, timestamp: Any):
        """
        Update threat history for trend analysis
        """
        self.threat_history.append({
            "threat_type": threat_type,
            "probability": probability,
            "timestamp": timestamp
        })
        
        # Keep only recent history
        if len(self.threat_history) > self.max_history_size:
            self.threat_history = self.threat_history[-self.max_history_size:]
    
    def get_threat_trends(self, hours: int = 24) -> Dict[str, Any]:
        """
        Analyze threat trends over specified time period
        
        Args:
            hours: Number of hours to analyze
            
        Returns:
            Dict containing trend analysis
        """
        try:
            if not self.threat_history:
                return {
                    "status": "no_data",
                    "message": "No threat history available"
                }
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter recent threats
            recent_threats = []
            for t in self.threat_history:
                ts = t["timestamp"]
                if isinstance(ts, str):
                    try:
                        ts = datetime.fromisoformat(ts)
                    except:
                        continue
                
                if isinstance(ts, datetime) and ts > cutoff_time:
                    recent_threats.append(t)
            
            if not recent_threats:
                return {
                    "status": "no_recent_data",
                    "message": f"No threats detected in last {hours} hours"
                }
            
            # Count threats by type
            threat_counts = {}
            threat_probs = {}
            
            for threat in recent_threats:
                ttype = threat["threat_type"]
                threat_counts[ttype] = threat_counts.get(ttype, 0) + 1
                
                if ttype not in threat_probs:
                    threat_probs[ttype] = []
                threat_probs[ttype].append(threat["probability"])
            
            # Calculate averages
            threat_stats = {}
            for ttype, probs in threat_probs.items():
                threat_stats[ttype] = {
                    "count": threat_counts[ttype],
                    "avg_probability": float(np.mean(probs)),
                    "max_probability": float(np.max(probs)),
                    "trend": "increasing" if len(probs) > 1 and probs[-1] > probs[0] else "stable"
                }
            
            return {
                "status": "success",
                "time_period_hours": hours,
                "total_detections": len(recent_threats),
                "threat_statistics": threat_stats,
                "most_common_threat": max(threat_counts, key=threat_counts.get) if threat_counts else "None",
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing threat trends: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_current_threat_status(self, hive_id: int = 1) -> Dict[str, Any]:
        """
        Get current threat status for a hive
        
        Args:
            hive_id: Hive ID to check
            
        Returns:
            Dict containing current threat status
        """
        try:
            # Try to import the appropriate data service
            try:
                from app.scheduler import USE_DUMMY_DATA
                
                if USE_DUMMY_DATA:
                    from app.services.dummy_data_service import dummy_data_service
                    latest_data = dummy_data_service.get_latest_synchronized_data(hive_id)
                else:
                    from app.services.synchronized_monitoring_service import synchronized_monitoring_service
                    latest_data = synchronized_monitoring_service.get_latest_synchronized_data(hive_id)
            except ImportError:
                # Fallback to dummy data if scheduler module not available
                from app.services.dummy_data_service import dummy_data_service
                latest_data = dummy_data_service.get_latest_synchronized_data(hive_id)
            
            if not latest_data:
                return {
                    "status": "no_data",
                    "message": "No recent data available for threat analysis",
                    "hive_id": hive_id
                }
            
            # Analyze latest data
            threat_result = self.analyze_synchronized_data(latest_data)
            
            if not threat_result:
                return {
                    "status": "analysis_failed",
                    "message": "Could not analyze threat from latest data",
                    "hive_id": hive_id,
                    "latest_data_timestamp": latest_data.get("collection_timestamp")
                }
            
            return {
                "status": "success",
                "hive_id": hive_id,
                "current_threat": threat_result,
                "data_timestamp": latest_data.get("collection_timestamp")
            }
            
        except Exception as e:
            logger.error(f"Error getting current threat status: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "hive_id": hive_id
            }

# Create singleton instance
real_time_threat_service = RealTimeThreatService()