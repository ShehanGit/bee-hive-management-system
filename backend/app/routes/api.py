from flask import Blueprint
from app.controllers.hive_controller import hive_blueprint
from app.controllers.sensor_controller import sensor_blueprint
from app.controllers.iot_controller import iot_blueprint
from app.controllers.weather_controller import weather_blueprint
from app.controllers.synchronized_data_controller import synchronized_data_blueprint
from app.controllers.synchronized_monitoring_controller import synchronized_monitoring_blueprint
# from app.controllers.predictive_features_controller import predictive_features_blueprint
from app.controllers.hive_management_controller import hive_management_blueprint

#imports of threat detection component
from flask import request, jsonify
from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat, get_model_meta
from app.ml_models.threat_detection.src.alert_store import add_alert, load_alerts

# api_bp = Blueprint('api_bp', __name__)

# # Register hive-related endpoints (if you want them under /hives)
# api_bp.register_blueprint(hive_blueprint, url_prefix='/')

# # Register sensor data endpoints
# api_bp.register_blueprint(sensor_blueprint, url_prefix='/')

# # Register IoT integration endpoints under /iot
# api_bp.register_blueprint(iot_blueprint, url_prefix='/')

api_bp = Blueprint('api_bp', __name__)

# Register hive-related endpoints (if you want them under /hives)
api_bp.register_blueprint(hive_blueprint, url_prefix='/')

# Register sensor data endpoints
api_bp.register_blueprint(sensor_blueprint, url_prefix='/')

# Register IoT integration endpoints under /iot
api_bp.register_blueprint(iot_blueprint, url_prefix='/')

# Register weather data endpoints under /weather
api_bp.register_blueprint(weather_blueprint, url_prefix='/')

# Register synchronized data endpoints under /synchronized
api_bp.register_blueprint(synchronized_data_blueprint, url_prefix='/')

# Register new synchronized monitoring endpoints under /synchronized-monitoring
api_bp.register_blueprint(synchronized_monitoring_blueprint, url_prefix='/')

# Register predictive features endpoints under /predictive-features
# api_bp.register_blueprint(predictive_features_blueprint, url_prefix='/')

# Register hive management endpoints under /hive-management
api_bp.register_blueprint(hive_management_blueprint, url_prefix='/')

#Threat detection component
# Add model info route
@api_bp.route("/threat/model_info", methods=["GET"])
def threat_model_info():
    return jsonify(get_model_meta()), 200

# Prediction route (use existing or add)
@api_bp.route("/threat/predict", methods=["POST"])
def threat_predict():
    payload = request.get_json(force=True, silent=True) or {}
    result = predict_threat(payload)
    # store alert if threat (not No_Threat)
    if result.get("threat_type") and result["threat_type"] != "No_Threat":
        add_alert(result["threat_type"], result.get("probability"), result.get("used_features", {}))
    return jsonify(result), 200

@api_bp.route("/threat/alerts", methods=["GET"])
def threat_alerts():
    limit = int(request.args.get("limit", 20))
    alerts = load_alerts()
    return jsonify(alerts[:limit]), 200