# app/controllers/performance_controller.py

from flask import Blueprint, jsonify, request
from app.services.performance_prediction_service import predict_latest_performance
from app.models.synchronized_data import SynchronizedData

performance_blueprint = Blueprint('performance_blueprint', __name__)

@performance_blueprint.route('/performance/predict', methods=['POST'])
def performance_predict():
    """
    Manually trigger hive performance prediction using the latest synchronized data.
    Request body: { "hive_id": 1 } (default: 1)
    """
    try:
        import logging
        logger = logging.getLogger(__name__)
        
        data = request.get_json() or {}
        hive_id = data.get('hive_id', 1)
        
        logger.info(f"Received prediction request for hive_id: {hive_id}")
        
        result = predict_latest_performance(hive_id)
        
        logger.info(f"Prediction result: {result}")
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            logger.error(f"Prediction failed: {result.get('error')}")
            return jsonify(result), 400
            
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Exception in performance_predict: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to predict performance: {str(e)}'
        }), 500

@performance_blueprint.route('/performance/history', methods=['GET'])
def get_performance_history():
    """
    Get historical performance predictions for a hive.
    Query params: hive_id (default 1), hours (default 24)
    
    Note: Historical predictions use the prediction service with weekly aggregation
    """
    try:
        hive_id = request.args.get('hive_id', 1, type=int)
        hours = request.args.get('hours', 24, type=int)
        
        from datetime import datetime, timedelta
        import logging
        logger = logging.getLogger(__name__)
        
        # For historical predictions, we aggregate the available data
        # up to the requested time range (weekly approach)
        
        # Calculate time window for aggregation
        since_time = datetime.now() - timedelta(hours=hours)
        
        # Get all synchronized data within time range
        records = SynchronizedData.query.filter(
            SynchronizedData.hive_id == hive_id,
            SynchronizedData.collection_timestamp >= since_time
        ).order_by(SynchronizedData.collection_timestamp.asc()).all()
        
        if len(records) < 100:
            return jsonify({
                'success': True,
                'hive_id': hive_id,
                'hours': hours,
                'history': [],
                'warning': 'Insufficient data for historical predictions'
            }), 200
        
        # Use the prediction service to get current prediction
        # For full history, you would need to slide a window or store predictions
        from app.services.performance_prediction_service import predict_latest_performance
        
        result = predict_latest_performance(hive_id)
        
        if result.get('success') and result.get('prediction'):
            # Return current prediction as the most recent history entry
            prediction = result['prediction']
            history = [{
                'predicted_level': prediction.get('predicted_level'),
                'interpretation': prediction.get('interpretation'),
                'confidence': prediction.get('confidence'),
                'risk_assessment': prediction.get('risk_assessment'),
                'all_probabilities': prediction.get('all_probabilities', {}),
                'timestamp': prediction.get('timestamp'),
                'collection_timestamp': records[-1].collection_timestamp.isoformat() if records else datetime.now().isoformat(),
                'data_points_used': prediction.get('data_points_used', len(records))
            }]
            
            return jsonify({
                'success': True,
                'hive_id': hive_id,
                'hours': hours,
                'history': history
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate historical prediction'
            }), 400
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in get_performance_history: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Failed to get performance history: {str(e)}'
        }), 500
