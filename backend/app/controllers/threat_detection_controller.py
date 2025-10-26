from flask import Blueprint, request, jsonify
from app.services.threat_detection_service import threat_detection_service
from app.models.synchronized_data import SynchronizedData
import logging

logger = logging.getLogger(__name__)

# Create blueprint
threat_detection_bp = Blueprint('threat_detection', __name__)

@threat_detection_bp.route('/threat/predict/latest', methods=['GET'])
def predict_latest_threat():
    """
    Predict threat for the latest synchronized data
    
    Query Parameters:
        hive_id (int): Hive ID to predict for (default: 1)
    
    Returns:
        JSON response with threat prediction results
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        
        result = threat_detection_service.predict_threat_for_latest_data(hive_id)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in predict_latest_threat endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Endpoint error: {str(e)}"
        }), 500

@threat_detection_bp.route('/threat/predict/historical', methods=['GET'])
def predict_historical_threats():
    """
    Predict threats for historical synchronized data
    
    Query Parameters:
        hive_id (int): Hive ID to predict for (default: 1)
        hours (int): Number of hours of historical data (default: 24)
    
    Returns:
        JSON response with list of threat prediction results
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        # Limit hours to prevent excessive processing
        hours = min(hours, 168)  # Max 7 days
        
        predictions = threat_detection_service.predict_threat_for_historical_data(hive_id, hours)
        
        return jsonify({
            "success": True,
            "predictions": predictions,
            "count": len(predictions),
            "hive_id": hive_id,
            "hours": hours
        }), 200
        
    except Exception as e:
        logger.error(f"Error in predict_historical_threats endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Endpoint error: {str(e)}"
        }), 500

@threat_detection_bp.route('/threat/statistics', methods=['GET'])
def get_threat_statistics():
    """
    Get threat statistics for a hive
    
    Query Parameters:
        hive_id (int): Hive ID to get stats for (default: 1)
        hours (int): Number of hours of historical data (default: 24)
    
    Returns:
        JSON response with threat statistics
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        # Limit hours to prevent excessive processing
        hours = min(hours, 168)  # Max 7 days
        
        stats = threat_detection_service.get_threat_statistics(hive_id, hours)
        
        if stats.get("success"):
            return jsonify(stats), 200
        else:
            return jsonify(stats), 400
            
    except Exception as e:
        logger.error(f"Error in get_threat_statistics endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Endpoint error: {str(e)}"
        }), 500

@threat_detection_bp.route('/threat/backfill', methods=['POST'])
def backfill_threat_predictions():
    """
    Backfill threat predictions for historical data
    
    Request Body:
        hive_id (int): Hive ID to backfill for (default: 1)
        days (int): Number of days to backfill (default: 7)
    
    Returns:
        JSON response with backfill results
    """
    try:
        data = request.get_json() or {}
        hive_id = data.get('hive_id', 1)
        days = data.get('days', 7)
        
        # Limit days to prevent excessive processing
        days = min(days, 30)  # Max 30 days
        
        result = threat_detection_service.backfill_threat_predictions(hive_id, days)
        
        if result.get("success"):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error in backfill_threat_predictions endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Endpoint error: {str(e)}"
        }), 500

@threat_detection_bp.route('/threat/data/quality', methods=['GET'])
def get_data_quality():
    """
    Get data quality information for threat detection
    
    Query Parameters:
        hive_id (int): Hive ID to get quality info for (default: 1)
        hours (int): Number of hours of historical data (default: 24)
    
    Returns:
        JSON response with data quality information
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        # Get historical data
        historical_data = SynchronizedData.get_historical_data(hive_id, hours)
        
        if not historical_data:
            return jsonify({
                "success": False,
                "error": f"No data found for hive {hive_id}"
            }), 404
        
        # Calculate quality metrics
        total_records = len(historical_data)
        records_with_threat_fields = len([
            record for record in historical_data 
            if record.sensor_sound_peak_freq is not None and 
               record.sensor_vibration_hz is not None and 
               record.sensor_vibration_var is not None
        ])
        
        quality_scores = [record.get_data_quality_score() for record in historical_data]
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return jsonify({
            "success": True,
            "data_quality": {
                "total_records": total_records,
                "records_with_threat_fields": records_with_threat_fields,
                "threat_fields_completion_rate": (records_with_threat_fields / total_records * 100) if total_records > 0 else 0,
                "average_quality_score": round(avg_quality_score, 2),
                "quality_score_range": {
                    "min": min(quality_scores) if quality_scores else 0,
                    "max": max(quality_scores) if quality_scores else 0
                },
                "hive_id": hive_id,
                "hours_analyzed": hours
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_data_quality endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Endpoint error: {str(e)}"
        }), 500
