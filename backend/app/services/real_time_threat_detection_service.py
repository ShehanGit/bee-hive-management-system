import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from app import db
from app.models.synchronized_data import SynchronizedData
from app.services.threat_detection_service import threat_detection_service
from app.ml_models.threat_detection.src.alert_store import add_alert, load_alerts
from app.ml_models.threat_detection.src.recommendation_service import get_recommendations
from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat
import numpy as np
from collections import deque
import threading
import time

logger = logging.getLogger(__name__)

class RealTimeThreatDetectionService:
    """
    Real-time threat detection service for continuous monitoring
    Implements advanced ML-based threat detection with alerting
    """
    
    def __init__(self):
        self.threat_model = None
        self.alert_thresholds = {
            'Environmental': 0.7,
            'Predator': 0.8,
            'Wax_Moth': 0.75,
            'No_Threat': 0.5
        }
        
        # Real-time monitoring state
        self.monitoring_active = False
        self.last_prediction_time = None
        self.prediction_history = deque(maxlen=100)  # Keep last 100 predictions
        
        # Alert cooldown to prevent spam
        self.alert_cooldowns = {
            'Environmental': 300,  # 5 minutes
            'Predator': 180,       # 3 minutes
            'Wax_Moth': 240,      # 4 minutes
            'No_Threat': 600      # 10 minutes
        }
        self.last_alert_times = {}
        
        # Performance metrics
        self.prediction_count = 0
        self.alert_count = 0
        self.start_time = datetime.now()
        
        self._load_model()
    
    def _load_model(self):
        """Load the threat detection model"""
        try:
            # Model is loaded via threat_detection_service
            logger.info("Real-time threat detection model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load threat detection model: {str(e)}")
    
    def start_monitoring(self, hive_id: int = 1, interval_seconds: int = 60):
        """
        Start real-time threat monitoring
        
        Args:
            hive_id: Hive ID to monitor
            interval_seconds: Monitoring interval in seconds
        """
        if self.monitoring_active:
            logger.warning("Monitoring is already active")
            return
        
        self.monitoring_active = True
        logger.info(f"Starting real-time threat monitoring for hive {hive_id} (interval: {interval_seconds}s)")
        
        def monitoring_loop():
            while self.monitoring_active:
                try:
                    self.process_latest_data(hive_id)
                    time.sleep(interval_seconds)
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {str(e)}")
                    time.sleep(interval_seconds)
        
        # Start monitoring in separate thread
        monitoring_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop real-time threat monitoring"""
        self.monitoring_active = False
        logger.info("Real-time threat monitoring stopped")
    
    def process_latest_data(self, hive_id: int = 1) -> Dict[str, Any]:
        """
        Process latest synchronized data for threat detection
        
        Args:
            hive_id: Hive ID to process
            
        Returns:
            Dict containing processing results and any alerts generated
        """
        try:
            # Get latest synchronized data
            latest_data = SynchronizedData.get_latest(hive_id)
            
            if not latest_data:
                return {
                    "success": False,
                    "error": f"No synchronized data found for hive {hive_id}",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Check if threat detection fields are populated
            if not self._has_threat_detection_fields(latest_data):
                logger.warning(f"Latest data for hive {hive_id} missing threat detection fields")
                return {
                    "success": False,
                    "error": "Missing threat detection fields",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Make threat prediction
            prediction_result = threat_detection_service.predict_threat_from_synchronized_data(latest_data)
            
            if not prediction_result.get("success"):
                return {
                    "success": False,
                    "error": prediction_result.get("error", "Prediction failed"),
                    "timestamp": datetime.now().isoformat()
                }
            
            prediction = prediction_result["prediction"]
            threat_type = prediction["threat_type"]
            probability = prediction.get("probability", 0.0)
            
            # Store prediction in history
            self.prediction_history.append({
                "timestamp": datetime.now(),
                "threat_type": threat_type,
                "probability": probability,
                "hive_id": hive_id
            })
            
            self.prediction_count += 1
            self.last_prediction_time = datetime.now()
            
            # Check if alert should be generated
            alert_generated = False
            alert_data = None
            
            if self._should_generate_alert(threat_type, probability):
                alert_data = self._generate_alert(latest_data, prediction_result)
                alert_generated = True
                self.alert_count += 1
            
            # Calculate threat trend
            threat_trend = self._calculate_threat_trend()
            
            result = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "hive_id": hive_id,
                "prediction": prediction,
                "data_quality": prediction_result["data_source"]["data_quality_score"],
                "alert_generated": alert_generated,
                "alert_data": alert_data,
                "threat_trend": threat_trend,
                "monitoring_stats": self._get_monitoring_stats()
            }
            
            logger.info(f"Processed latest data for hive {hive_id}: {threat_type} (prob: {probability:.3f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing latest data: {str(e)}")
            return {
                "success": False,
                "error": f"Processing failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def process_historical_data(self, hive_id: int = 1, hours: int = 24) -> Dict[str, Any]:
        """
        Process historical data for threat detection analysis
        
        Args:
            hive_id: Hive ID to process
            hours: Number of hours of historical data
            
        Returns:
            Dict containing processing results
        """
        try:
            # Get historical predictions
            predictions = threat_detection_service.predict_threat_for_historical_data(hive_id, hours)
            
            if not predictions:
                return {
                    "success": False,
                    "error": f"No historical predictions available for hive {hive_id}"
                }
            
            # Analyze threat patterns
            threat_analysis = self._analyze_threat_patterns(predictions)
            
            # Generate historical alerts for high-probability threats
            historical_alerts = []
            for pred in predictions:
                if pred.get("success") and pred["prediction"].get("probability", 0) > 0.8:
                    threat_type = pred["prediction"]["threat_type"]
                    if threat_type != "No_Threat":
                        alert_data = self._generate_historical_alert(pred)
                        if alert_data:
                            historical_alerts.append(alert_data)
            
            result = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "hive_id": hive_id,
                "hours_analyzed": hours,
                "total_predictions": len(predictions),
                "threat_analysis": threat_analysis,
                "historical_alerts": historical_alerts,
                "alert_count": len(historical_alerts)
            }
            
            logger.info(f"Processed {len(predictions)} historical predictions for hive {hive_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing historical data: {str(e)}")
            return {
                "success": False,
                "error": f"Historical processing failed: {str(e)}"
            }
    
    def get_threat_dashboard_data(self, hive_id: int = 1, hours: int = 24) -> Dict[str, Any]:
        """
        Get comprehensive threat detection data for dashboard
        
        Args:
            hive_id: Hive ID to get data for
            hours: Number of hours of data
            
        Returns:
            Dict containing dashboard data
        """
        try:
            # Get threat statistics
            stats = threat_detection_service.get_threat_statistics(hive_id, hours)
            
            # Get recent alerts
            recent_alerts = load_alerts()
            
            # Get prediction history
            recent_predictions = list(self.prediction_history)[-20:]  # Last 20 predictions
            
            # Calculate threat level
            threat_level = self._calculate_threat_level(recent_predictions)
            
            # Get data quality info
            data_quality = self._get_data_quality_info(hive_id, hours)
            
            result = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "hive_id": hive_id,
                "hours": hours,
                "threat_statistics": stats.get("statistics", {}) if stats.get("success") else {},
                "recent_alerts": recent_alerts[:10],  # Last 10 alerts
                "recent_predictions": recent_predictions,
                "threat_level": threat_level,
                "data_quality": data_quality,
                "monitoring_status": {
                    "active": self.monitoring_active,
                    "prediction_count": self.prediction_count,
                    "alert_count": self.alert_count,
                    "uptime_hours": (datetime.now() - self.start_time).total_seconds() / 3600
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {str(e)}")
            return {
                "success": False,
                "error": f"Dashboard data failed: {str(e)}"
            }
    
    def _has_threat_detection_fields(self, data: SynchronizedData) -> bool:
        """Check if synchronized data has threat detection fields populated"""
        return all([
            data.sensor_sound_peak_freq is not None,
            data.sensor_vibration_hz is not None,
            data.sensor_vibration_var is not None
        ])
    
    def _should_generate_alert(self, threat_type: str, probability: float) -> bool:
        """Determine if an alert should be generated based on threat type and probability"""
        if threat_type == "No_Threat":
            return False
        
        threshold = self.alert_thresholds.get(threat_type, 0.7)
        if probability < threshold:
            return False
        
        # Check cooldown period
        now = datetime.now()
        last_alert_time = self.last_alert_times.get(threat_type)
        
        if last_alert_time:
            cooldown_seconds = self.alert_cooldowns.get(threat_type, 300)
            if (now - last_alert_time).total_seconds() < cooldown_seconds:
                return False
        
        return True
    
    def _generate_alert(self, data: SynchronizedData, prediction_result: Dict) -> Optional[Dict]:
        """Generate an alert for a threat detection"""
        try:
            prediction = prediction_result["prediction"]
            threat_type = prediction["threat_type"]
            probability = prediction.get("probability", 0.0)
            
            # Get recommendations
            recommendations = get_recommendations(threat_type)
            
            # Prepare used features
            used_features = {
                "weather_temp_c": data.weather_temperature,
                "weather_humidity_pct": data.weather_humidity,
                "hive_sound_db": data.sensor_sound,
                "hive_sound_peak_freq": data.sensor_sound_peak_freq,
                "vibration_hz": data.sensor_vibration_hz,
                "vibration_var": data.sensor_vibration_var,
                "timestamp": data.collection_timestamp.isoformat()
            }
            
            # Add alert to store
            alert_data = add_alert(
                threat_type=threat_type,
                probability=probability,
                used_features=used_features,
                recommendations=recommendations
            )
            
            # Update last alert time
            self.last_alert_times[threat_type] = datetime.now()
            
            logger.warning(f"🚨 THREAT ALERT: {threat_type} detected with {probability:.3f} probability")
            
            return alert_data
            
        except Exception as e:
            logger.error(f"Error generating alert: {str(e)}")
            return None
    
    def _generate_historical_alert(self, prediction_result: Dict) -> Optional[Dict]:
        """Generate alert for historical high-probability threat"""
        try:
            prediction = prediction_result["prediction"]
            threat_type = prediction["threat_type"]
            probability = prediction.get("probability", 0.0)
            
            # Get recommendations
            recommendations = get_recommendations(threat_type)
            
            # Prepare used features
            used_features = prediction_result.get("generated_fields", {})
            
            # Add alert to store
            alert_data = add_alert(
                threat_type=threat_type,
                probability=probability,
                used_features=used_features,
                recommendations=recommendations
            )
            
            return alert_data
            
        except Exception as e:
            logger.error(f"Error generating historical alert: {str(e)}")
            return None
    
    def _calculate_threat_trend(self) -> Dict[str, Any]:
        """Calculate threat trend from recent predictions"""
        if len(self.prediction_history) < 5:
            return {"trend": "insufficient_data", "direction": "stable"}
        
        recent_predictions = list(self.prediction_history)[-10:]  # Last 10 predictions
        
        # Calculate trend
        threat_scores = []
        for pred in recent_predictions:
            threat_type = pred["threat_type"]
            probability = pred["probability"]
            
            # Convert threat type to numeric score
            if threat_type == "No_Threat":
                score = 0
            elif threat_type == "Environmental":
                score = probability * 0.5
            elif threat_type == "Wax_Moth":
                score = probability * 0.8
            elif threat_type == "Predator":
                score = probability * 1.0
            else:
                score = probability * 0.6
            
            threat_scores.append(score)
        
        # Calculate trend direction
        if len(threat_scores) >= 3:
            recent_avg = np.mean(threat_scores[-3:])
            earlier_avg = np.mean(threat_scores[:-3]) if len(threat_scores) > 3 else threat_scores[0]
            
            if recent_avg > earlier_avg * 1.1:
                direction = "increasing"
            elif recent_avg < earlier_avg * 0.9:
                direction = "decreasing"
            else:
                direction = "stable"
        else:
            direction = "stable"
        
        return {
            "trend": "calculated",
            "direction": direction,
            "current_threat_level": np.mean(threat_scores[-3:]) if len(threat_scores) >= 3 else 0,
            "prediction_count": len(recent_predictions)
        }
    
    def _analyze_threat_patterns(self, predictions: List[Dict]) -> Dict[str, Any]:
        """Analyze threat patterns from historical predictions"""
        if not predictions:
            return {"error": "No predictions to analyze"}
        
        successful_predictions = [p for p in predictions if p.get("success")]
        
        if not successful_predictions:
            return {"error": "No successful predictions to analyze"}
        
        # Extract threat types and probabilities
        threat_types = [p["prediction"]["threat_type"] for p in successful_predictions]
        probabilities = [p["prediction"].get("probability", 0) for p in successful_predictions]
        
        # Calculate statistics
        threat_counts = {}
        for threat_type in threat_types:
            threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
        
        avg_probability = np.mean(probabilities)
        max_probability = np.max(probabilities)
        min_probability = np.min(probabilities)
        
        # Find most common threat
        most_common_threat = max(threat_counts.items(), key=lambda x: x[1]) if threat_counts else ("No_Threat", 0)
        
        # Calculate threat intensity over time
        time_windows = []
        window_size = max(1, len(successful_predictions) // 5)  # 5 time windows
        
        for i in range(0, len(successful_predictions), window_size):
            window_predictions = successful_predictions[i:i+window_size]
            window_threats = [p["prediction"]["threat_type"] for p in window_predictions]
            window_probs = [p["prediction"].get("probability", 0) for p in window_predictions]
            
            time_windows.append({
                "window": i // window_size + 1,
                "threat_types": window_threats,
                "avg_probability": np.mean(window_probs),
                "max_probability": np.max(window_probs)
            })
        
        return {
            "total_predictions": len(successful_predictions),
            "threat_distribution": threat_counts,
            "most_common_threat": {
                "type": most_common_threat[0],
                "count": most_common_threat[1],
                "percentage": (most_common_threat[1] / len(successful_predictions)) * 100
            },
            "probability_stats": {
                "average": round(avg_probability, 3),
                "maximum": round(max_probability, 3),
                "minimum": round(min_probability, 3)
            },
            "time_analysis": time_windows
        }
    
    def _calculate_threat_level(self, recent_predictions: List[Dict]) -> Dict[str, Any]:
        """Calculate current threat level based on recent predictions"""
        if not recent_predictions:
            return {"level": "unknown", "score": 0, "description": "No recent data"}
        
        # Calculate threat score
        threat_scores = []
        for pred in recent_predictions:
            threat_type = pred["threat_type"]
            probability = pred["probability"]
            
            if threat_type == "No_Threat":
                score = 0
            elif threat_type == "Environmental":
                score = probability * 0.3
            elif threat_type == "Wax_Moth":
                score = probability * 0.7
            elif threat_type == "Predator":
                score = probability * 1.0
            else:
                score = probability * 0.5
            
            threat_scores.append(score)
        
        avg_score = np.mean(threat_scores)
        
        # Determine threat level
        if avg_score >= 0.8:
            level = "critical"
            description = "High threat level detected"
        elif avg_score >= 0.6:
            level = "high"
            description = "Elevated threat level"
        elif avg_score >= 0.4:
            level = "moderate"
            description = "Moderate threat level"
        elif avg_score >= 0.2:
            level = "low"
            description = "Low threat level"
        else:
            level = "minimal"
            description = "Minimal threat level"
        
        return {
            "level": level,
            "score": round(avg_score, 3),
            "description": description,
            "prediction_count": len(recent_predictions)
        }
    
    def _get_data_quality_info(self, hive_id: int, hours: int) -> Dict[str, Any]:
        """Get data quality information"""
        try:
            historical_data = SynchronizedData.get_historical_data(hive_id, hours)
            
            if not historical_data:
                return {"error": "No data available"}
            
            total_records = len(historical_data)
            records_with_threat_fields = len([
                record for record in historical_data 
                if self._has_threat_detection_fields(record)
            ])
            
            quality_scores = [record.get_data_quality_score() for record in historical_data]
            avg_quality_score = np.mean(quality_scores) if quality_scores else 0
            
            return {
                "total_records": total_records,
                "records_with_threat_fields": records_with_threat_fields,
                "threat_fields_completion_rate": (records_with_threat_fields / total_records * 100) if total_records > 0 else 0,
                "average_quality_score": round(avg_quality_score, 2),
                "quality_score_range": {
                    "min": round(min(quality_scores), 2) if quality_scores else 0,
                    "max": round(max(quality_scores), 2) if quality_scores else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting data quality info: {str(e)}")
            return {"error": str(e)}
    
    def _get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        uptime_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        
        return {
            "monitoring_active": self.monitoring_active,
            "prediction_count": self.prediction_count,
            "alert_count": self.alert_count,
            "uptime_hours": round(uptime_hours, 2),
            "last_prediction_time": self.last_prediction_time.isoformat() if self.last_prediction_time else None,
            "prediction_history_size": len(self.prediction_history)
        }

# Create singleton instance
real_time_threat_detection_service = RealTimeThreatDetectionService()
