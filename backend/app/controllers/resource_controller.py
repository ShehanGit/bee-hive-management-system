# app/controllers/resource_controller.py

from flask import Blueprint, request, jsonify
from app.services.resource_service import (
    get_all_resources, get_resource_by_id,
    create_resource, update_resource, delete_resource
)

resource_blueprint = Blueprint('resource_blueprint', __name__)

@resource_blueprint.route('/resources', methods=['GET'])
def get_resources():
    resources = get_all_resources()
    results = [{
        'id': res.id,
        'type': res.type,
        'lat': res.lat,
        'lng': res.lng,
        'created_at': res.created_at
    } for res in resources]
    return jsonify(results), 200

@resource_blueprint.route('/resources', methods=['POST'])
def add_resource():
    data = request.get_json()
    required_fields = ['type', 'lat', 'lng']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    res = create_resource(data)
    return jsonify({"message": "Resource created", "id": res.id}), 201

@resource_blueprint.route('/resources/<int:res_id>', methods=['GET'])
def get_single_resource(res_id):
    res = get_resource_by_id(res_id)
    if not res:
        return jsonify({"error": "Resource not found"}), 404
    return jsonify({
        'id': res.id,
        'type': res.type,
        'lat': res.lat,
        'lng': res.lng,
        'created_at': res.created_at
    }), 200

@resource_blueprint.route('/resources/<int:res_id>', methods=['PUT'])
def update_single_resource(res_id):
    data = request.get_json()
    res = update_resource(res_id, data)
    if not res:
        return jsonify({"error": "Resource not found"}), 404
    return jsonify({"message": "Resource updated"}), 200

@resource_blueprint.route('/resources/<int:res_id>', methods=['DELETE'])
def delete_single_resource(res_id):
    res = delete_resource(res_id)
    if not res:
        return jsonify({"error": "Resource not found"}), 404
    return jsonify({"message": "Resource deleted"}), 200