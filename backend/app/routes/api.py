# backend/app/routes/api.py
from flask import Blueprint, request, jsonify
# existing blueprints
from app.controllers.hive_controller import hive_blueprint
from app.controllers.sensor_controller import sensor_blueprint
from app.controllers.iot_controller import iot_blueprint

# threat detection imports
from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat, get_model_meta
from app.ml_models.threat_detection.src.alert_store import add_alert, load_alerts
from app.ml_models.threat_detection.src.recommendation_service import get_recommendations

# In app/api.py, add:
from app.controllers.potential_location_controller import potential_loc_blueprint

# In app/api.py, add or update:
from app.controllers.ml_controller import ml_blueprint


# Missing controller imports
from app.controllers.weather_controller import weather_blueprint
from app.controllers.synchronized_data_controller import synchronized_data_blueprint
from app.controllers.synchronized_monitoring_controller import synchronized_monitoring_blueprint
from app.controllers.hive_management_controller import hive_management_blueprint
from app.controllers.performance_controller import performance_blueprint
from app.controllers.historical_performance_controller import historical_performance_blueprint
from app.controllers.threat_detection_controller import threat_detection_bp

api_bp = Blueprint('api_bp', __name__)

# register existing blueprints (keep your existing ones)
api_bp.register_blueprint(hive_blueprint, url_prefix='/')
api_bp.register_blueprint(sensor_blueprint, url_prefix='/')
api_bp.register_blueprint(iot_blueprint, url_prefix='/')


api_bp.register_blueprint(potential_loc_blueprint, url_prefix='/')

api_bp.register_blueprint(ml_blueprint, url_prefix='/')


# Performance Predict blueprint registrations
api_bp.register_blueprint(weather_blueprint, url_prefix='/')
api_bp.register_blueprint(synchronized_data_blueprint, url_prefix='/')
api_bp.register_blueprint(synchronized_monitoring_blueprint, url_prefix='/')
api_bp.register_blueprint(hive_management_blueprint, url_prefix='/')
api_bp.register_blueprint(performance_blueprint, url_prefix='/')
api_bp.register_blueprint(historical_performance_blueprint, url_prefix='/')
api_bp.register_blueprint(threat_detection_bp, url_prefix='/')



#Threat detection component
# Add model info route

@api_bp.route("/threat/model_info", methods=["GET"])
def threat_model_info():
    return jsonify(get_model_meta()), 200

# Prediction route
@api_bp.route("/threat/predict", methods=["POST"])
def threat_predict():
    try:
        payload = request.get_json(force=True, silent=True) or {}
    except Exception:
        payload = {}

    result = predict_threat(payload)  # {'threat_type', 'probability', 'used_features'}

    # attach recommendations (always attach, even for No_Threat)
    threat = result.get("threat_type")
    recs = get_recommendations(threat) if threat else get_recommendations("No_Threat")
    result["recommendations"] = recs

    # store alert if not No_Threat (optional: store all; here we store only threats)
    if threat and threat != "No_Threat":
        try:
            add_alert(threat, result.get("probability"), result.get("used_features", {}), recommendations=recs)
        except Exception:
            # don't break response if saving fails
            pass

    return jsonify(result), 200

# Alerts
@api_bp.route("/threat/alerts", methods=["GET"])
def threat_alerts():
    limit = int(request.args.get("limit", 20))
    alerts = load_alerts()
    return jsonify(alerts[:limit]), 200
