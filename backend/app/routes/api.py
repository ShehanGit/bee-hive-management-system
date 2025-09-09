from flask import Blueprint
from app.controllers.hive_controller import hive_blueprint
from app.controllers.sensor_controller import sensor_blueprint
from app.controllers.iot_controller import iot_blueprint

#imports of threat detection component
from flask import request, jsonify
from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat, get_model_meta
from app.ml_models.threat_detection.src.alert_store import add_alert, load_alerts

api_bp = Blueprint('api_bp', __name__)

# Register hive-related endpoints (if you want them under /hives)
api_bp.register_blueprint(hive_blueprint, url_prefix='/')

# Register sensor data endpoints
api_bp.register_blueprint(sensor_blueprint, url_prefix='/')

# Register IoT integration endpoints under /iot
api_bp.register_blueprint(iot_blueprint, url_prefix='/')

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