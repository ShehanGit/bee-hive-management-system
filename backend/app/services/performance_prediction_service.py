# app/services/performance_prediction_service.py

import os
from app.models.synchronized_data import SynchronizedData
from app.ml_models.performance_prediction.src.prediction_service_performance import HivePerformancePredictor

# Set model paths relative to backend/app/ml_models/performance_prediction
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'performance_prediction', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'performance_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
META_PATH = os.path.join(MODEL_DIR, 'performance_model_meta.json')

predictor = HivePerformancePredictor(
    model_path=MODEL_PATH,
    scaler_path=SCALER_PATH,
    metadata_path=META_PATH
)

def predict_latest_performance(hive_id=1):
    # Get latest synchronized data
    latest = SynchronizedData.get_latest(hive_id)
    if not latest:
        return {'success': False, 'error': 'No synchronized data found'}

    # Flatten to dict for model
    data_row = {
        'collection_timestamp': latest.collection_timestamp,
        'sensor_temperature': latest.sensor_temperature,
        'sensor_humidity': latest.sensor_humidity,
        'sensor_sound': latest.sensor_sound,
        'sensor_weight': latest.sensor_weight,
        'weather_temperature': latest.weather_temperature,
        'weather_humidity': latest.weather_humidity,
        'weather_wind_speed': latest.weather_wind_speed,
        'weather_light_intensity': latest.weather_light_intensity,
        'weather_rainfall': latest.weather_rainfall
    }
    try:
        pred = predictor.predict_single(data_row)
        return {'success': True, 'prediction': pred}
    except Exception as e:
        return {'success': False, 'error': str(e)}
