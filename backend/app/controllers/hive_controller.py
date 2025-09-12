# app/controllers/hive_controller.py

from flask import Blueprint, request, jsonify
from app.services.hive_service import get_all_hives, get_hive_by_id, create_hive, update_hive, delete_hive

hive_blueprint = Blueprint('hive_blueprint', __name__)

@hive_blueprint.route('/hives', methods=['GET'])
def get_hives():
    """Get all hives."""
    hives = get_all_hives()
    results = [{
        'id': hive.id,
        'name': hive.name,
        'location_lat': hive.location_lat,
        'location_lng': hive.location_lng,
        'created_at': hive.created_at
    } for hive in hives]
    return jsonify(results), 200

@hive_blueprint.route('/hives', methods=['POST'])
def add_hive():
    """Create a new hive."""
    data = request.get_json()
    if not data or not all([data.get('name'), data.get('location_lat'), data.get('location_lng')]):
        return jsonify({"error": "Missing required fields"}), 400
    
    hive = create_hive(data['name'], data['location_lat'], data['location_lng'])
    return jsonify({
        "message": f"Hive '{hive.name}' created successfully",
        "id": hive.id
    }), 201

@hive_blueprint.route('/hives/<int:hive_id>', methods=['GET'])
def get_single_hive(hive_id):
    """Retrieve a specific hive."""
    hive = get_hive_by_id(hive_id)
    if not hive:
        return jsonify({"error": "Hive not found"}), 404

    return jsonify({
        'id': hive.id,
        'name': hive.name,
        'location_lat': hive.location_lat,
        'location_lng': hive.location_lng,
        'created_at': hive.created_at
    }), 200

@hive_blueprint.route('/hives/<int:hive_id>', methods=['PUT'])
def modify_hive(hive_id):
    """Update an existing hive."""
    data = request.get_json()
    hive = update_hive(hive_id, data.get('name'), data.get('location_lat'), data.get('location_lng'))
    
    if not hive:
        return jsonify({"error": "Hive not found"}), 404

    return jsonify({"message": f"Hive '{hive.name}' updated successfully"}), 200

@hive_blueprint.route('/hives/<int:hive_id>', methods=['DELETE'])
def remove_hive(hive_id):
    """Delete a hive."""
    hive = delete_hive(hive_id)
    
    if not hive:
        return jsonify({"error": "Hive not found"}), 404

    return jsonify({"message": "Hive deleted successfully"}), 200


