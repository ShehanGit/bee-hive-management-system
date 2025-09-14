from flask import Blueprint, jsonify, request
from app.services.synchronized_monitoring_service import synchronized_monitoring_service
from app.models.synchronized_data import SynchronizedData
import logging

logger = logging.getLogger(__name__)

synchronized_monitoring_blueprint = Blueprint('synchronized_monitoring_blueprint', __name__)

@synchronized_monitoring_blueprint.route('/synchronized/collect', methods=['POST'])
def collect_synchronized_data():
    """
    Manually trigger synchronized data collection
    
    Query Parameters:
        hive_id (int): Hive ID (default: 1)
        
    Returns:
        JSON response with collection results
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        
        result = synchronized_monitoring_service.collect_synchronized_data(hive_id)
        
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

@synchronized_monitoring_blueprint.route('/synchronized/latest', methods=['GET'])
def get_latest_synchronized_data():
    """
    Get the most recent synchronized data
    
    Query Parameters:
        hive_id (int): Hive ID (default: 1)
        
    Returns:
        JSON response with latest synchronized data
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        
        latest_data = SynchronizedData.get_latest(hive_id)
        
        if latest_data:
            return jsonify({
                'success': True,
                'data': latest_data.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'No synchronized data available',
                'data': None
            }), 200
            
    except Exception as e:
        logger.error(f"Error in get_latest_synchronized_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get latest synchronized data',
            'message': str(e)
        }), 500

@synchronized_monitoring_blueprint.route('/synchronized/historical', methods=['GET'])
def get_historical_synchronized_data():
    """
    Get historical synchronized data
    
    Query Parameters:
        hive_id (int): Hive ID (default: 1)
        hours (int): Number of hours of data (default: 24)
        perfect_alignment_only (bool): Only return perfectly aligned data (default: false)
        
    Returns:
        JSON response with historical synchronized data
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        perfect_alignment_only = request.args.get('perfect_alignment_only', 'false').lower() == 'true'
        
        # Limit hours to prevent excessive data
        if hours > 168:  # Max 1 week
            hours = 168
        
        if perfect_alignment_only:
            historical_data = SynchronizedData.get_perfect_alignment_data(hive_id, hours)
        else:
            historical_data = SynchronizedData.get_historical_data(hive_id, hours)
        
        return jsonify({
            'success': True,
            'hive_id': hive_id,
            'hours': hours,
            'perfect_alignment_only': perfect_alignment_only,
            'data_points': len(historical_data),
            'data': [record.to_dict() for record in historical_data]
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_historical_synchronized_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get historical synchronized data',
            'message': str(e)
        }), 500

@synchronized_monitoring_blueprint.route('/synchronized/alignment-stats', methods=['GET'])
def get_alignment_statistics():
    """
    Get statistics about data alignment quality
    
    Query Parameters:
        hive_id (int): Hive ID (default: 1)
        hours (int): Number of hours of data (default: 24)
        
    Returns:
        JSON response with alignment statistics
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        stats = SynchronizedData.get_alignment_statistics(hive_id, hours)
        
        return jsonify({
            'success': True,
            'hive_id': hive_id,
            'hours': hours,
            'statistics': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_alignment_statistics: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get alignment statistics',
            'message': str(e)
        }), 500

@synchronized_monitoring_blueprint.route('/synchronized/status', methods=['GET'])
def get_synchronized_status():
    """
    Get status of synchronized monitoring service
    
    Returns:
        JSON response with service status
    """
    try:
        status = synchronized_monitoring_service.get_collection_status()
        
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

@synchronized_monitoring_blueprint.route('/synchronized/data-quality', methods=['GET'])
def get_data_quality_analysis():
    """
    Get data quality analysis for synchronized data
    
    Query Parameters:
        hive_id (int): Hive ID (default: 1)
        hours (int): Number of hours of data (default: 24)
        
    Returns:
        JSON response with data quality analysis
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        # Get historical data
        historical_data = SynchronizedData.get_historical_data(hive_id, hours)
        
        if not historical_data:
            return jsonify({
                'success': False,
                'message': 'No data available for analysis'
            }), 200
        
        # Calculate quality metrics
        total_records = len(historical_data)
        perfect_alignment_count = sum(1 for record in historical_data if record.is_perfectly_aligned())
        
        quality_scores = [record.get_data_quality_score() for record in historical_data]
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Temperature correlation analysis
        temp_differences = []
        humidity_differences = []
        
        for record in historical_data:
            if record.is_perfectly_aligned():
                temp_diff = record.calculate_temperature_difference()
                humidity_diff = record.calculate_humidity_difference()
                
                if temp_diff is not None:
                    temp_differences.append(temp_diff)
                if humidity_diff is not None:
                    humidity_differences.append(humidity_diff)
        
        analysis = {
            'total_records': total_records,
            'perfect_alignment_count': perfect_alignment_count,
            'alignment_percentage': (perfect_alignment_count / total_records * 100) if total_records > 0 else 0,
            'average_quality_score': round(avg_quality_score, 2),
            'temperature_analysis': {
                'correlation_count': len(temp_differences),
                'average_difference': round(sum(temp_differences) / len(temp_differences), 2) if temp_differences else None,
                'min_difference': round(min(temp_differences), 2) if temp_differences else None,
                'max_difference': round(max(temp_differences), 2) if temp_differences else None
            },
            'humidity_analysis': {
                'correlation_count': len(humidity_differences),
                'average_difference': round(sum(humidity_differences) / len(humidity_differences), 2) if humidity_differences else None,
                'min_difference': round(min(humidity_differences), 2) if humidity_differences else None,
                'max_difference': round(max(humidity_differences), 2) if humidity_differences else None
            }
        }
        
        return jsonify({
            'success': True,
            'hive_id': hive_id,
            'hours': hours,
            'analysis': analysis
        }), 200
        
    except Exception as e:
        logger.error(f"Error in get_data_quality_analysis: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get data quality analysis',
            'message': str(e)
        }), 500
