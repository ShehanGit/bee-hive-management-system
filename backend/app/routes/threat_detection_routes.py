from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import logging

from app.services.real_time_threat_service import real_time_threat_service
from app.services.synchronized_monitoring_service import synchronized_monitoring_service
from app.ml_models.threat_detection.src.alert_store import load_alerts

logger = logging.getLogger(__name__)

threat_bp = Blueprint('threat_detection', __name__, url_prefix='/api/threat-detection')


@threat_bp.route('/current-status/<int:hive_id>', methods=['GET'])
def get_current_threat_status(hive_id):
    """
    Get current threat status for a specific hive
    
    GET /api/threat-detection/current-status/1
    """
    try:
        # Check if using dummy data mode
        from app.scheduler import USE_DUMMY_DATA
        
        if USE_DUMMY_DATA:
            from app.services.dummy_data_service import dummy_data_service
            latest_data = dummy_data_service.get_latest_synchronized_data(hive_id)
        else:
            from app.services.synchronized_monitoring_service import synchronized_monitoring_service
            latest_data = synchronized_monitoring_service.get_latest_synchronized_data(hive_id)
        
        if not latest_data:
            return jsonify({
                "status": "no_data",
                "message": "No recent data available",
                "data_mode": "dummy" if USE_DUMMY_DATA else "real"
            }), 404
        
        # Analyze threats
        threat_result = real_time_threat_service.analyze_synchronized_data(latest_data)
        
        if threat_result:
            return jsonify({
                "status": "success",
                "hive_id": hive_id,
                "current_threat": threat_result,
                "data_timestamp": latest_data.get("collection_timestamp"),
                "data_mode": "dummy" if USE_DUMMY_DATA else "real"
            }), 200
        else:
            return jsonify({
                "status": "analysis_failed",
                "message": "Could not analyze threat",
                "data_mode": "dummy" if USE_DUMMY_DATA else "real"
            }), 500
    
    except Exception as e:
        logger.error(f"Error getting current threat status: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@threat_bp.route('/analyze-latest/<int:hive_id>', methods=['POST'])
def analyze_latest_data(hive_id):
    """
    Manually trigger threat analysis on latest data
    
    POST /api/threat-detection/analyze-latest/1
    """
    try:
        # Get latest synchronized data
        latest_data = synchronized_monitoring_service.get_latest_synchronized_data(hive_id)
        
        if not latest_data:
            return jsonify({
                "success": False,
                "message": "No recent data available for analysis"
            }), 404
        
        # Analyze for threats
        result = real_time_threat_service.analyze_synchronized_data(latest_data)
        
        if result:
            return jsonify({
                "success": True,
                "threat_analysis": result
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "Analysis failed"
            }), 500
    
    except Exception as e:
        logger.error(f"Error analyzing latest data: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@threat_bp.route('/alerts', methods=['GET'])
def get_threat_alerts():
    """
    Get all stored threat alerts
    
    GET /api/threat-detection/alerts?limit=50
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        
        # Load alerts from storage
        alerts = load_alerts()
        
        # Limit results
        alerts = alerts[:limit] if alerts else []
        
        return jsonify({
            "success": True,
            "count": len(alerts),
            "alerts": alerts
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting threat alerts: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e),
            "alerts": []
        }), 500


@threat_bp.route('/alerts/recent/<int:hours>', methods=['GET'])
def get_recent_alerts(hours):
    """
    Get threat alerts from the last N hours
    
    GET /api/threat-detection/alerts/recent/24
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Load all alerts
        all_alerts = load_alerts()
        
        # Filter by time
        recent_alerts = []
        for alert in all_alerts:
            try:
                alert_time = datetime.fromisoformat(alert["timestamp"])
                if alert_time > cutoff_time:
                    recent_alerts.append(alert)
            except Exception:
                continue
        
        return jsonify({
            "success": True,
            "time_period_hours": hours,
            "count": len(recent_alerts),
            "alerts": recent_alerts
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting recent alerts: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e),
            "alerts": []
        }), 500


@threat_bp.route('/trends/<int:hive_id>', methods=['GET'])
def get_threat_trends(hive_id):
    """
    Get threat trend analysis for a hive
    
    GET /api/threat-detection/trends/1?hours=24
    """
    try:
        hours = request.args.get('hours', 24, type=int)
        
        trends = real_time_threat_service.get_threat_trends(hours=hours)
        
        return jsonify(trends), 200
    
    except Exception as e:
        logger.error(f"Error getting threat trends: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@threat_bp.route('/statistics/<int:hive_id>', methods=['GET'])
def get_threat_statistics(hive_id):
    """
    Get comprehensive threat statistics for a hive
    
    GET /api/threat-detection/statistics/1?hours=24
    """
    try:
        hours = request.args.get('hours', 24, type=int)
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Load alerts
        all_alerts = load_alerts()
        
        # Filter recent alerts
        recent_alerts = []
        for alert in all_alerts:
            try:
                alert_time = datetime.fromisoformat(alert["timestamp"])
                if alert_time > cutoff_time:
                    recent_alerts.append(alert)
            except Exception:
                continue
        
        # Count by threat type
        threat_counts = {}
        severity_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        
        for alert in recent_alerts:
            # Count threat types
            threat_type = alert.get("threat_type", "Unknown")
            threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
            
            # Count severity levels
            recommendations = alert.get("recommendations", {})
            if isinstance(recommendations, dict):
                severity = recommendations.get("severity", "Unknown")
                if severity in severity_counts:
                    severity_counts[severity] += 1
        
        # Calculate percentages
        total_alerts = len(recent_alerts)
        threat_percentages = {}
        if total_alerts > 0:
            for threat_type, count in threat_counts.items():
                threat_percentages[threat_type] = round((count / total_alerts) * 100, 2)
        
        return jsonify({
            "success": True,
            "hive_id": hive_id,
            "time_period_hours": hours,
            "total_alerts": total_alerts,
            "threat_counts": threat_counts,
            "threat_percentages": threat_percentages,
            "severity_distribution": severity_counts,
            "analysis_timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting threat statistics: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@threat_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """
    Get ML model information
    
    GET /api/threat-detection/model-info
    """
    try:
        from app.ml_models.threat_detection.src.prediction_service_threat import get_model_meta
        
        meta = get_model_meta()
        
        return jsonify({
            "success": True,
            "model_info": {
                "threat_classes": meta.get("classes", []),
                "feature_count": len(meta.get("features", [])),
                "features": meta.get("features", [])
            }
        }), 200
    
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@threat_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for threat detection service
    
    GET /api/threat-detection/health
    """
    try:
        last_analysis = real_time_threat_service.last_analysis_time
        
        return jsonify({
            "status": "healthy",
            "service": "Real-Time Threat Detection",
            "last_analysis_time": last_analysis.isoformat() if last_analysis else None,
            "threat_history_size": len(real_time_threat_service.threat_history),
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": str(e)
        }), 500


# Export blueprint
def register_threat_routes(app):
    """Register threat detection routes with Flask app"""
    app.register_blueprint(threat_bp)
    logger.info("✅ Threat detection routes registered")