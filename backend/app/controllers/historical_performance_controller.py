from flask import Blueprint, jsonify, request
from app.services.historical_performance_service import get_historical_performance

historical_performance_blueprint = Blueprint('historical_performance_blueprint', __name__)

@historical_performance_blueprint.route('/performance/history', methods=['GET'])
def performance_history():
    """
    Get historical hive performance predictions for a hive.
    Query params: hive_id (default 1), hours (default 24)
    """
    hive_id = request.args.get('hive_id', 1, type=int)
    hours = request.args.get('hours', 24, type=int)
    result = get_historical_performance(hive_id, hours)
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400
