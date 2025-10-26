from app.models.synchronized_data import SynchronizedData
from app.services.performance_prediction_service import predict_latest_performance
import logging

logger = logging.getLogger(__name__)

def get_historical_performance(hive_id=1, hours=24):
    """
    Get historical performance predictions for a hive.
    
    Note: Now uses the weekly aggregation approach - returns current prediction
    based on available historical data.
    """
    try:
        from datetime import datetime, timedelta
        
        # Get historical synchronized data
        since_time = datetime.now() - timedelta(hours=hours)
        
        historical = SynchronizedData.query.filter(
            SynchronizedData.hive_id == hive_id,
            SynchronizedData.collection_timestamp >= since_time
        ).order_by(SynchronizedData.collection_timestamp.asc()).all()
        
        if not historical:
            return {'success': False, 'error': 'No historical data found'}
        
        # Use the main prediction service which handles aggregation correctly
        result = predict_latest_performance(hive_id)
        
        if result.get('success') and result.get('prediction'):
            prediction = result['prediction']
            
            # Return in expected format
            return {
                'success': True,
                'history': [{
                    'predicted_level': prediction.get('predicted_level'),
                    'interpretation': prediction.get('interpretation'),
                    'confidence': prediction.get('confidence'),
                    'risk_assessment': prediction.get('risk_assessment'),
                    'collection_timestamp': prediction.get('timestamp'),
                    'data_points_used': prediction.get('data_points_used', len(historical)),
                    'weight_change_pct': prediction.get('weight_change_pct', 0)
                }]
            }
        else:
            return {'success': False, 'error': 'Failed to generate prediction'}
            
    except Exception as e:
        logger.error(f"Error in get_historical_performance: {str(e)}")
        return {'success': False, 'error': str(e)}
