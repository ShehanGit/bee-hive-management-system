from app.models.synchronized_data import SynchronizedData
from app.ml_models.performance_prediction.src.prediction_service_performance import HivePerformancePredictor
import os
import pandas as pd

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'performance_prediction', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'performance_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
META_PATH = os.path.join(MODEL_DIR, 'performance_model_meta.json')

predictor = HivePerformancePredictor(
    model_path=MODEL_PATH,
    scaler_path=SCALER_PATH,
    metadata_path=META_PATH
)

def get_historical_performance(hive_id=1, hours=24):
    # Get historical synchronized data
    historical = SynchronizedData.get_historical_data(hive_id, hours)
    if not historical:
        return {'success': False, 'error': 'No historical data found'}

    # Prepare DataFrame for batch prediction
    data_rows = []
    timestamps = []
    for entry in historical:
        data_rows.append({
            'collection_timestamp': entry.collection_timestamp,
            'sensor_temperature': entry.sensor_temperature,
            'sensor_humidity': entry.sensor_humidity,
            'sensor_sound': entry.sensor_sound,
            'sensor_weight': entry.sensor_weight,
            'weather_temperature': entry.weather_temperature,
            'weather_humidity': entry.weather_humidity,
            'weather_wind_speed': entry.weather_wind_speed,
            'weather_light_intensity': entry.weather_light_intensity,
            'weather_rainfall': entry.weather_rainfall
        })
        timestamps.append(entry.collection_timestamp)
    df = pd.DataFrame(data_rows)
    try:
        preds = predictor.predict_batch(df)
        # Attach timestamps to predictions
        for i, pred in enumerate(preds):
            pred['collection_timestamp'] = timestamps[i].isoformat() if timestamps[i] else None
        return {'success': True, 'history': preds}
    except Exception as e:
        return {'success': False, 'error': str(e)}
