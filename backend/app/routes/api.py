from flask import Blueprint, request, jsonify

# --- Combined Blueprint Imports ---
# Existing blueprints from the repository
from app.controllers.hive_controller import hive_blueprint
from app.controllers.sensor_controller import sensor_blueprint
from app.controllers.iot_controller import iot_blueprint
from app.controllers.potential_location_controller import potential_loc_blueprint
from app.controllers.ml_controller import ml_blueprint

# Your new blueprints
from app.controllers.weather_controller import weather_blueprint
from app.controllers.synchronized_data_controller import synchronized_data_blueprint
from app.controllers.synchronized_monitoring_controller import synchronized_monitoring_blueprint
from app.controllers.hive_management_controller import hive_management_blueprint
from app.controllers.performance_controller import performance_blueprint

# --- Machine Learning & Threat Detection Imports ---
from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat, get_model_meta
from app.ml_models.threat_detection.src.alert_store import add_alert, load_alerts
from app.ml_models.threat_detection.src.recommendation_service import get_recommendations


# --- Main API Blueprint Initialization ---
api_bp = Blueprint('api_bp', __name__)


# --- Register All Blueprints ---
# Registering all blueprints in one consolidated section
api_bp.register_blueprint(hive_blueprint, url_prefix='/')
api_bp.register_blueprint(sensor_blueprint, url_prefix='/')
api_bp.register_blueprint(iot_blueprint, url_prefix='/')
api_bp.register_blueprint(weather_blueprint, url_prefix='/')
api_bp.register_blueprint(synchronized_data_blueprint, url_prefix='/')
api_bp.register_blueprint(synchronized_monitoring_blueprint, url_prefix='/')
api_bp.register_blueprint(hive_management_blueprint, url_prefix='/')
api_bp.register_blueprint(potential_loc_blueprint, url_prefix='/')
api_bp.register_blueprint(performance_blueprint, url_prefix='/')
api_bp.register_blueprint(ml_blueprint, url_prefix='/')


# --- Threat Detection API Routes ---

# Model Info Route
@api_bp.route("/threat/model_info", methods=["GET"])
def threat_model_info():
    """Returns metadata about the threat detection model."""
    return jsonify(get_model_meta()), 200

# Prediction Route
@api_bp.route("/threat/predict", methods=["POST"])
def threat_predict():
    """Predicts a threat based on the JSON payload and returns recommendations."""
    try:
        payload = request.get_json(force=True, silent=True) or {}
    except Exception:
        payload = {}

    result = predict_threat(payload)  # {'threat_type', 'probability', 'used_features'}

    # Attach recommendations (always attach, even for No_Threat)
    threat = result.get("threat_type")
    recs = get_recommendations(threat) if threat else get_recommendations("No_Threat")
    result["recommendations"] = recs

    # Store an alert if a threat is detected
    if threat and threat != "No_Threat":
        try:
            add_alert(threat, result.get("probability"), result.get("used_features", {}), recommendations=recs)
        except Exception as e:
            # Don't break the response if saving the alert fails
            # In a production environment, you would log this error (e.g., current_app.logger.error(...))
            pass

    return jsonify(result), 200

# Alerts Route
@api_bp.route("/threat/alerts", methods=["GET"])
def threat_alerts():
    """Retrieves a list of the most recent threat alerts."""
    limit = int(request.args.get("limit", 20))
    alerts = load_alerts()
    return jsonify(alerts[:limit]), 200