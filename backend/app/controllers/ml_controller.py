# app/controllers/ml_controller.py

from flask import Blueprint, jsonify
from app.services.ml_service import predict_for_all_locations

ml_blueprint = Blueprint('ml_blueprint', __name__)

@ml_blueprint.route('/ml/predict-all', methods=['GET'])
def predict_all():
    updated_count = predict_for_all_locations()
    if updated_count == 0:
        return jsonify({"message": "No locations to predict"}), 200
    return jsonify({"message": f"Predictions updated for {updated_count} locations"}), 200