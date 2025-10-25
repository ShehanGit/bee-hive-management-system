import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from app import db
from app.models.synchronized_data import SynchronizedData

logger = logging.getLogger(__name__)

class ThreatDetectionService:
    """
    Service for threat detection using SynchronizedData
    Integrates with existing threat detection ML model
    """
    
    def __init__(self):
        self.threat_model = None
        self._load_threat_model()
    
    def _load_threat_model(self):
        """Load the threat detection model"""
        try:
            from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat
            self.predict_threat = predict_threat
            logger.info("Threat detection model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load threat detection model: {str(e)}")
            self.predict_threat = None
    
    def predict_threat_from_synchronized_data(self, synchronized_data: SynchronizedData) -> Dict[str, Any]:
        """
        Predict threat using SynchronizedData
        
        Args:
            synchronized_data: SynchronizedData instance
            
        Returns:
            Dict containing threat prediction results
        """
        try:
            if not self.predict_threat:
                return {
                    "success": False,
                    "error": "Threat detection model not available"
                }
            
            # Get threat detection payload from SynchronizedData
            payload = synchronized_data.get_threat_detection_payload()
            
            # Make prediction
            prediction_result = self.predict_threat(payload)
            
            # Add metadata
            result = {
                "success": True,
                "prediction": prediction_result,
                "data_source": {
                    "hive_id": synchronized_data.hive_id,
                    "timestamp": synchronized_data.collection_timestamp.isoformat(),
                    "data_quality_score": synchronized_data.get_data_quality_score()
                },
                "generated_fields": {
                    "sound_peak_freq": synchronized_data.sensor_sound_peak_freq,
                    "vibration_hz": synchronized_data.sensor_vibration_hz,
                    "vibration_var": synchronized_data.sensor_vibration_var
                }
            }
            
            logger.info(f"Threat prediction completed for hive {synchronized_data.hive_id}: {prediction_result['threat_type']}")
            return result
            
        except Exception as e:
            logger.error(f"Error predicting threat from synchronized data: {str(e)}")
            return {
                "success": False,
                "error": f"Prediction failed: {str(e)}"
            }
    
    def predict_threat_for_latest_data(self, hive_id: int = 1) -> Dict[str, Any]:
        """
        Predict threat for the latest synchronized data
        
        Args:
            hive_id: The hive ID to predict for
            
        Returns:
            Dict containing threat prediction results
        """
        try:
            # Get latest synchronized data
            latest_data = SynchronizedData.get_latest(hive_id)
            
            if not latest_data:
                return {
                    "success": False,
                    "error": f"No synchronized data found for hive {hive_id}"
                }
            
            return self.predict_threat_from_synchronized_data(latest_data)
            
        except Exception as e:
            logger.error(f"Error predicting threat for latest data: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to get latest data: {str(e)}"
            }
    
    def predict_threat_for_historical_data(self, hive_id: int = 1, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Predict threats for historical synchronized data
        
        Args:
            hive_id: The hive ID to predict for
            hours: Number of hours of historical data
            
        Returns:
            List of threat prediction results
        """
        try:
            # Get historical synchronized data
            historical_data = SynchronizedData.get_historical_data(hive_id, hours)
            
            if not historical_data:
                return []
            
            predictions = []
            for data_point in historical_data:
                prediction = self.predict_threat_from_synchronized_data(data_point)
                predictions.append(prediction)
            
            logger.info(f"Generated {len(predictions)} threat predictions for hive {hive_id}")
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting threats for historical data: {str(e)}")
            return []
    
    def get_threat_statistics(self, hive_id: int = 1, hours: int = 24) -> Dict[str, Any]:
        """
        Get threat statistics for a hive
        
        Args:
            hive_id: The hive ID to get stats for
            hours: Number of hours of historical data
            
        Returns:
            Dict containing threat statistics
        """
        try:
            predictions = self.predict_threat_for_historical_data(hive_id, hours)
            
            if not predictions:
                return {
                    "success": False,
                    "error": f"No threat predictions available for hive {hive_id}"
                }
            
            # Calculate statistics
            successful_predictions = [p for p in predictions if p.get("success", False)]
            threat_types = [p["prediction"]["threat_type"] for p in successful_predictions]
            
            # Count threat types
            threat_counts = {}
            for threat_type in threat_types:
                threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
            
            # Calculate average probability
            probabilities = [p["prediction"]["probability"] for p in successful_predictions if p["prediction"].get("probability")]
            avg_probability = sum(probabilities) / len(probabilities) if probabilities else 0
            
            # Find most common threat
            most_common_threat = max(threat_counts.items(), key=lambda x: x[1]) if threat_counts else ("No_Threat", 0)
            
            return {
                "success": True,
                "statistics": {
                    "total_predictions": len(predictions),
                    "successful_predictions": len(successful_predictions),
                    "threat_type_counts": threat_counts,
                    "most_common_threat": {
                        "type": most_common_threat[0],
                        "count": most_common_threat[1],
                        "percentage": (most_common_threat[1] / len(successful_predictions) * 100) if successful_predictions else 0
                    },
                    "average_probability": round(avg_probability, 3),
                    "time_range_hours": hours,
                    "hive_id": hive_id
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting threat statistics: {str(e)}")
            return {
                "success": False,
                "error": f"Failed to get threat statistics: {str(e)}"
            }
    
    def backfill_threat_predictions(self, hive_id: int = 1, days: int = 7) -> Dict[str, Any]:
        """
        Backfill threat predictions for historical data
        
        Args:
            hive_id: The hive ID to backfill for
            days: Number of days to backfill
            
        Returns:
            Dict containing backfill results
        """
        try:
            hours = days * 24
            historical_data = SynchronizedData.get_historical_data(hive_id, hours)
            
            if not historical_data:
                return {
                    "success": False,
                    "error": f"No historical data found for hive {hive_id}"
                }
            
            # Filter records that don't have threat detection fields calculated
            records_to_process = [
                record for record in historical_data 
                if record.sensor_sound_peak_freq is None or 
                   record.sensor_vibration_hz is None or 
                   record.sensor_vibration_var is None
            ]
            
            if not records_to_process:
                return {
                    "success": True,
                    "message": "All records already have threat detection fields calculated",
                    "records_processed": 0
                }
            
            # Calculate threat detection fields for each record
            processed_count = 0
            for record in records_to_process:
                try:
                    record.calculate_threat_detection_fields()
                    processed_count += 1
                except Exception as e:
                    logger.error(f"Error calculating threat fields for record {record.id}: {str(e)}")
            
            # Commit changes
            db.session.commit()
            
            logger.info(f"Backfilled threat detection fields for {processed_count} records")
            
            return {
                "success": True,
                "message": f"Successfully processed {processed_count} records",
                "records_processed": processed_count,
                "total_records": len(historical_data)
            }
            
        except Exception as e:
            logger.error(f"Error backfilling threat predictions: {str(e)}")
            db.session.rollback()
            return {
                "success": False,
                "error": f"Backfill failed: {str(e)}"
            }

# Create singleton instance
threat_detection_service = ThreatDetectionService()
