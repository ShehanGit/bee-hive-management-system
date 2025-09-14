from flask import Blueprint, jsonify, request
from app.services.synchronized_data_service import synchronized_data_service
import logging

logger = logging.getLogger(__name__)

synchronized_data_blueprint = Blueprint('synchronized_data_blueprint', __name__)

@synchronized_data_blueprint.route('/synchronized/collect', methods=['POST'])
def collect_synchronized_data():
    """
    Manually trigger synchronized data collection
    
    Returns:
        JSON response with collection results
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        
        result = synchronized_data_service.collect_synchronized_data(hive_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Synchronized data collection completed successfully',
                'data': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Synchronized data collection failed',
                'errors': result['errors'],
                'data': result
            }), 500
            
    except Exception as e:
        logger.error(f"Error in collect_synchronized_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to collect synchronized data',
            'message': str(e)
        }), 500

@synchronized_data_blueprint.route('/synchronized/data', methods=['GET'])
def get_synchronized_data():
    """
    Get synchronized sensor and weather data
    
    Query Parameters:
        hive_id (int): Hive ID (default: 1)
        hours (int): Number of hours of data (default: 24)
        
    Returns:
        JSON response with synchronized data
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        # Limit hours to prevent excessive data
        if hours > 168:  # Max 1 week
            hours = 168
        
        synchronized_data = synchronized_data_service.get_synchronized_data(hive_id, hours)
        
        return jsonify({
            'success': True,
            'hive_id': hive_id,
            'hours': hours,
            'data_points': len(synchronized_data),
            'data': synchronized_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_synchronized_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get synchronized data',
            'message': str(e)
        }), 500

@synchronized_data_blueprint.route('/synchronized/alignment-stats', methods=['GET'])
def get_alignment_stats():
    """
    Get statistics about data alignment between sensor and weather data
    
    Query Parameters:
        hive_id (int): Hive ID (default: 1)
        hours (int): Number of hours of data (default: 24)
        
    Returns:
        JSON response with alignment statistics
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        stats = synchronized_data_service.get_data_alignment_stats(hive_id, hours)
        
        if 'error' in stats:
            return jsonify({
                'success': False,
                'error': stats['error']
            }), 400
        
        return jsonify({
            'success': True,
            'hive_id': hive_id,
            'hours': hours,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_alignment_stats: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get alignment statistics',
            'message': str(e)
        }), 500

@synchronized_data_blueprint.route('/synchronized/status', methods=['GET'])
def get_synchronized_status():
    """
    Get status of synchronized data collection service
    
    Returns:
        JSON response with service status
    """
    try:
        status = {
            'service_status': 'active',
            'collection_interval_minutes': synchronized_data_service.collection_interval_minutes,
            'last_collection_time': synchronized_data_service.last_collection_time.isoformat() if synchronized_data_service.last_collection_time else None,
            'features': [
                'Synchronized timestamp collection',
                'Weather and sensor data alignment',
                'Data correlation analysis',
                'Alignment statistics'
            ]
        }
        
        return jsonify({
            'success': True,
            'status': status
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_synchronized_status: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get synchronized status',
            'message': str(e)
        }), 500

