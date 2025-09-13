from flask import Blueprint, request, jsonify
from app.services.synchronized_monitoring_service import synchronized_monitoring_service
import logging

logger = logging.getLogger(__name__)

# Create blueprint
hive_management_blueprint = Blueprint('hive_management', __name__)

@hive_management_blueprint.route('/api/hive/<int:hive_id>/update', methods=['PUT'])
def update_hive(hive_id):
    """
    Update hive name and location
    
    Expected JSON payload:
    {
        "name": "New Hive Name",
        "latitude": 6.9271,
        "longitude": 79.8612
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        # Extract parameters
        name = data.get('name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Validate latitude and longitude if provided
        if latitude is not None and (latitude < -90 or latitude > 90):
            return jsonify({
                "success": False,
                "error": "Latitude must be between -90 and 90"
            }), 400
        
        if longitude is not None and (longitude < -180 or longitude > 180):
            return jsonify({
                "success": False,
                "error": "Longitude must be between -180 and 180"
            }), 400
        
        # Update hive
        result = synchronized_monitoring_service.update_hive_location(
            hive_id=hive_id,
            name=name,
            latitude=latitude,
            longitude=longitude
        )
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error updating hive {hive_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@hive_management_blueprint.route('/api/hive/<int:hive_id>', methods=['GET'])
def get_hive(hive_id):
    """
    Get hive information
    """
    try:
        from app.models.hive import Hive
        
        hive = Hive.query.get(hive_id)
        
        if not hive:
            return jsonify({
                "success": False,
                "error": f"Hive {hive_id} not found"
            }), 404
        
        return jsonify({
            "success": True,
            "hive": {
                "id": hive.id,
                "name": hive.name,
                "location_lat": hive.location_lat,
                "location_lng": hive.location_lng,
                "created_at": hive.created_at.isoformat() if hive.created_at else None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting hive {hive_id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@hive_management_blueprint.route('/api/hives', methods=['GET'])
def get_all_hives():
    """
    Get all hives
    """
    try:
        from app.models.hive import Hive
        
        hives = Hive.query.all()
        
        return jsonify({
            "success": True,
            "hives": [{
                "id": hive.id,
                "name": hive.name,
                "location_lat": hive.location_lat,
                "location_lng": hive.location_lng,
                "created_at": hive.created_at.isoformat() if hive.created_at else None
            } for hive in hives]
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting all hives: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
