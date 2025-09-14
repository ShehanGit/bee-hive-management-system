# app/controllers/performance_controller.py

from flask import Blueprint, jsonify, request
from app.services.performance_prediction_service import predict_latest_performance

performance_blueprint = Blueprint('performance_blueprint', __name__)

# New endpoint: Real-time hive performance prediction controller
@performance_blueprint.route('/performance/predict', methods=['GET'])
def performance_predict():
    """
    Predict hive performance using the latest synchronized data for a hive.
    Query param: hive_id (default 1)
    """
    hive_id = request.args.get('hive_id', 1, type=int)
    result = predict_latest_performance(hive_id)
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400
