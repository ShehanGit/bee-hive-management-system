# app/routes/api.py (update to register new blueprint)

from flask import Blueprint
from app.controllers.hive_controller import hive_blueprint
from app.controllers.sensor_controller import sensor_blueprint
from app.controllers.iot_controller import iot_blueprint

# Imports of threat detection component
from flask import request, jsonify
from app.ml_models.threat_detection.src.prediction_service_threat import predict_threat, get_model_meta
from app.ml_models.threat_detection.src.alert_store import add_alert, load_alerts

# Existing imports for potential locations and ML
from app.controllers.potential_location_controller import potential_loc_blueprint
from app.controllers.ml_controller import ml_blueprint

# New import for resources
from app.controllers.resource_controller import resource_blueprint

api_bp = Blueprint('api_bp', __name__)

# Register blueprints
api_bp.register_blueprint(hive_blueprint, url_prefix='/')
api_bp.register_blueprint(sensor_blueprint, url_prefix='/')
api_bp.register_blueprint(iot_blueprint, url_prefix='/')
api_bp.register_blueprint(potential_loc_blueprint, url_prefix='/')
api_bp.register_blueprint(ml_blueprint, url_prefix='/')
api_bp.register_blueprint(resource_blueprint, url_prefix='/')  # New

# Threat detection routes...
@api_bp.route("/threat/model_info", methods=["GET"])
def threat_model_info():
    return jsonify(get_model_meta()), 200

@api_bp.route("/threat/predict", methods=["POST"])
def threat_predict():
    payload = request.get_json(force=True, silent=True) or {}
    result = predict_threat(payload)
    if result.get("threat_type") and result["threat_type"] != "No_Threat":
        add_alert(result["threat_type"], result.get("probability"), result.get("used_features", {}))
    return jsonify(result), 200

@api_bp.route("/threat/alerts", methods=["GET"])
def threat_alerts():
    limit = int(request.args.get("limit", 20))
    alerts = load_alerts()
    return jsonify(alerts[:limit]), 200