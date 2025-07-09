from flask import Blueprint
from app.controllers.hive_controller import hive_blueprint
from app.controllers.sensor_controller import sensor_blueprint
from app.controllers.iot_controller import iot_blueprint

api_bp = Blueprint('api_bp', __name__)

# Register hive-related endpoints (if you want them under /hives)
api_bp.register_blueprint(hive_blueprint, url_prefix='/')

# Register sensor data endpoints
api_bp.register_blueprint(sensor_blueprint, url_prefix='/')

# Register IoT integration endpoints under /iot
api_bp.register_blueprint(iot_blueprint, url_prefix='/')

