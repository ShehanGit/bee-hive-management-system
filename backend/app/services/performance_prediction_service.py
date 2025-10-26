# app/services/performance_prediction_service.py

import os
import logging
import json
from app.models.synchronized_data import SynchronizedData

logger = logging.getLogger(__name__)

# Set model paths relative to backend/app/ml_models/performance_prediction
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml_models', 'performance_prediction', 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'performance_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
META_PATH = os.path.join(MODEL_DIR, 'performance_model_meta.json')

# Cache loaded models (avoid reloading on every request)
_model_cache = None
_scaler_cache = None
_metadata_cache = None
_cache_lock = None

def get_cached_model():
    """Load and cache model artifacts (lazy loaded)"""
    global _model_cache, _scaler_cache, _metadata_cache, _cache_lock
    
    # Quick return if already loaded
    if _model_cache is not None and _scaler_cache is not None and _metadata_cache is not None:
        logger.info("Using cached model artifacts")
        return _model_cache, _scaler_cache, _metadata_cache
    
    # Initialize lock if needed
    import threading
    if _cache_lock is None:
        _cache_lock = threading.Lock()
    
    # Thread-safe loading
    with _cache_lock:
        # Double-check after acquiring lock
        if _model_cache is not None and _scaler_cache is not None and _metadata_cache is not None:
            logger.info("Using cached model artifacts (after lock)")
            return _model_cache, _scaler_cache, _metadata_cache
        
        # Import joblib only when needed (lazy loading)
        import joblib
        
        logger.info("Loading model artifacts (first time)...")
        
        # Check if files exist
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Scaler file not found: {SCALER_PATH}")
        if not os.path.exists(META_PATH):
            raise FileNotFoundError(f"Metadata file not found: {META_PATH}")
        
        try:
            logger.info(f"Loading model from: {MODEL_PATH}")
            _model_cache = joblib.load(MODEL_PATH)
            logger.info("Model loaded successfully")
            
            # ALWAYS set n_jobs to 1 to avoid multiprocessing hangs in Flask
            # This is critical - the default n_jobs=-1 causes the model to hang
            if hasattr(_model_cache, 'set_params'):
                original_n_jobs = getattr(_model_cache, 'n_jobs', None)
                _model_cache.set_params(n_jobs=1)
                logger.info(f"✅ Set model n_jobs from {original_n_jobs} to 1 to avoid threading issues")
            else:
                logger.warning("Model does not support set_params - may still have threading issues")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
        
        try:
            logger.info(f"Loading scaler from: {SCALER_PATH}")
            _scaler_cache = joblib.load(SCALER_PATH)
            logger.info("Scaler loaded successfully")
        except Exception as e:
            logger.error(f"Error loading scaler: {str(e)}")
            raise
        
        try:
            logger.info(f"Loading metadata from: {META_PATH}")
            with open(META_PATH, 'r') as f:
                _metadata_cache = json.load(f)
            logger.info("Metadata loaded successfully")
        except Exception as e:
            logger.error(f"Error loading metadata: {str(e)}")
            raise
    
    return _model_cache, _scaler_cache, _metadata_cache

def predict_latest_performance(hive_id=1):
    """
    Predict hive performance by aggregating last 7 days of data
    
    Note: Model expects weekly aggregates (same features as training)
    """
    try:
        from datetime import datetime, timedelta
        import pandas as pd
        import numpy as np
        
        import time
        
        logger.info(f"Starting performance prediction for hive_id: {hive_id}")
        total_start_time = time.time()
        
        # Get last 7 days of data
        since_time = datetime.now() - timedelta(days=7)
        
        start_time = time.time()
        
        logger.info(f"Querying database for records since {since_time}...")
        # Use very small limit for faster queries - 1000 records is sufficient for weekly aggregation
        # This gives us ~7 hours of data at 1-minute intervals
        records = SynchronizedData.query.filter(
            SynchronizedData.hive_id == hive_id,
            SynchronizedData.collection_timestamp >= since_time
        ).order_by(SynchronizedData.collection_timestamp.asc()).limit(1000).all()
        
        query_time = time.time() - start_time
        logger.info(f"Database query completed in {query_time:.2f}s, got {len(records)} records")
        
        # If we got too many records, sample evenly for faster processing
        if len(records) > 500:
            logger.info(f"Sampling records for faster processing...")
            import random
            records = random.sample(records, 500)
            logger.info(f"Sampled down to {len(records)} records")
        
        if not records:
            logger.warning(f"No data found for hive_id: {hive_id}")
            return {'success': False, 'error': 'No data available'}
        
        logger.info(f"Found {len(records)} records for hive {hive_id}")
        
        # Check if we have enough data (at least 100 data points = ~7 hours)
        if len(records) < 100:
            logger.warning(f"Insufficient data: {len(records)} records (< 100 required)")
            # Return optimistic default prediction
            return {
                'success': True,
                'prediction': {
                    'predicted_level': 3,  # Moderate
                    'interpretation': 'Insufficient data for accurate prediction - need at least 7 hours of data',
                    'confidence': 0.50,
                    'risk_assessment': 'INSUFFICIENT DATA - Collecting baseline',
                    'data_points_used': len(records),
                    'warning': 'Prediction based on limited data. Accuracy will improve with more data.'
                }
            }
        
        # Convert to DataFrame for aggregation
        logger.info("Creating DataFrame...")
        df_start_time = time.time()
        
        try:
            df = pd.DataFrame([{
                'collection_timestamp': r.collection_timestamp,
                'weather_temperature': r.weather_temperature,
                'weather_humidity': r.weather_humidity,
                'weather_wind_speed': r.weather_wind_speed,
                'weather_light_intensity': r.weather_light_intensity,
                'weather_rainfall': r.weather_rainfall,
                'sensor_temperature': r.sensor_temperature,
                'sensor_humidity': r.sensor_humidity,
                'sensor_sound': r.sensor_sound,
                'sensor_weight': r.sensor_weight
            } for r in records])
            
            df_time = time.time() - df_start_time
            logger.info(f"DataFrame created in {df_time:.2f}s with {len(df)} rows, starting aggregation...")
        except Exception as e:
            logger.error(f"Error creating DataFrame: {str(e)}")
            raise
        
        # Prepare base features (same as preprocessing)  
        df['collection_timestamp'] = pd.to_datetime(df['collection_timestamp'])
        
        # Fill any NaN values in numeric columns with 0 to prevent errors
        numeric_cols = ['weather_temperature', 'weather_humidity', 'weather_wind_speed', 
                      'weather_light_intensity', 'weather_rainfall', 'sensor_temperature', 
                      'sensor_humidity', 'sensor_sound', 'sensor_weight']
        df[numeric_cols] = df[numeric_cols].fillna(0)
        
        df['temp_differential'] = df['sensor_temperature'] - df['weather_temperature']
        df['humidity_differential'] = df['sensor_humidity'] - df['weather_humidity']
        
        df['favorable_foraging'] = (
            (df['weather_temperature'] > 15) &
            (df['weather_rainfall'] == 0) &
            (df['weather_wind_speed'] < 25) &
            (df['weather_light_intensity'] > 1000)
        ).astype(int)
        
        df['thermal_stress'] = (
            (df['weather_temperature'] > 35) |
            (df['weather_temperature'] < 18)
        ).astype(int)
        
        # Sound activity normalization
        if df['sensor_sound'].max() != df['sensor_sound'].min():
            df['sound_activity'] = (df['sensor_sound'] - df['sensor_sound'].min()) / (df['sensor_sound'].max() - df['sensor_sound'].min())
        else:
            df['sound_activity'] = 0
        
        df['hour'] = df['collection_timestamp'].dt.hour
        df['is_daytime'] = (df['hour'] >= 6) & (df['hour'] <= 18)
        df['temp_variance'] = abs(df['sensor_temperature'] - df['sensor_temperature'].mean())
        
        # Aggregate to weekly features (same as training) - OPTIMIZED
        agg_start_time = time.time()
        logger.info("Starting aggregation...")
        weekly_features = {}
        
        try:
            # Use numpy for faster aggregations
            np_df = df  # Keep pandas for datetime operations
            
            # Weather aggregations - vectorized
            weekly_features['avg_weather_temp'] = df['weather_temperature'].mean()
            weekly_features['min_weather_temp'] = df['weather_temperature'].min()
            weekly_features['max_weather_temp'] = df['weather_temperature'].max()
            weekly_features['avg_weather_humidity'] = df['weather_humidity'].mean()
            weekly_features['avg_weather_wind'] = df['weather_wind_speed'].mean()
            weekly_features['avg_weather_light'] = df['weather_light_intensity'].mean()
            weekly_features['total_weather_rainfall'] = df['weather_rainfall'].sum()
            
            # Sensor aggregations - vectorized
            weekly_features['avg_sensor_temp'] = df['sensor_temperature'].mean()
            weekly_features['std_sensor_temp'] = df['sensor_temperature'].std() if len(df) > 1 else 0
            weekly_features['min_sensor_temp'] = df['sensor_temperature'].min()
            weekly_features['max_sensor_temp'] = df['sensor_temperature'].max()
            weekly_features['avg_sensor_humidity'] = df['sensor_humidity'].mean()
            weekly_features['avg_sensor_sound'] = df['sensor_sound'].mean()
            weekly_features['max_sensor_sound'] = df['sensor_sound'].max()
            
            # Weight metrics
            weekly_features['start_weight'] = df['sensor_weight'].iloc[0]
            weekly_features['end_weight'] = df['sensor_weight'].iloc[-1]
            weekly_features['min_weight'] = df['sensor_weight'].min()
            weekly_features['max_weight'] = df['sensor_weight'].max()
            weekly_features['avg_weight'] = df['sensor_weight'].mean()
            
            # Weight change calculations REMOVED - not in model's expected features
            # Model expects: start_weight, end_weight, avg_weight, min_weight, max_weight (already computed above)
            
            # Differential aggregations - vectorized
            weekly_features['avg_temp_differential'] = df['temp_differential'].mean()
            weekly_features['max_temp_differential'] = df['temp_differential'].max()
            weekly_features['min_temp_differential'] = df['temp_differential'].min()
            weekly_features['avg_humidity_differential'] = df['humidity_differential'].mean()
            
            # Binary event aggregations - vectorized
            weekly_features['total_favorable_foraging_minutes'] = df['favorable_foraging'].sum()
            weekly_features['pct_favorable_foraging'] = (df['favorable_foraging'].sum() / len(df)) * 100
            weekly_features['total_thermal_stress_minutes'] = df['thermal_stress'].sum()
            weekly_features['pct_thermal_stress'] = (df['thermal_stress'].sum() / len(df)) * 100
            
            # Sound activity by time of day - optimized
            daytime_mask = df['is_daytime'] == True
            daytime_sound = df.loc[daytime_mask, 'sound_activity']
            nighttime_sound = df.loc[~daytime_mask, 'sound_activity']
            
            weekly_features['avg_sound_activity_daytime'] = daytime_sound.mean() if len(daytime_sound) > 0 else 0
            weekly_features['avg_sound_activity_nighttime'] = nighttime_sound.mean() if len(nighttime_sound) > 0 else 0
            weekly_features['sound_activity_ratio'] = weekly_features['avg_sound_activity_daytime'] / (weekly_features['avg_sound_activity_nighttime'] + 0.001)
            
            # Temperature stability
            weekly_features['avg_temp_variance'] = df['temp_variance'].mean()
            weekly_features['max_temp_variance'] = df['temp_variance'].max()
            
            # Activity patterns - optimized
            max_sound_idx = df['sensor_sound'].idxmax()
            weekly_features['peak_activity_hour'] = df.loc[max_sound_idx, 'hour'] if max_sound_idx in df.index else 12
            
            # Pre-filter by hour to avoid multiple scans
            hour = df['hour']
            sound = df['sensor_sound']
            
            morning_mask = (hour >= 6) & (hour < 12)
            afternoon_mask = (hour >= 12) & (hour < 18)
            evening_mask = (hour >= 18) & (hour < 22)
            
            weekly_features['activity_morning'] = sound[morning_mask].mean() if morning_mask.sum() > 0 else 0
            weekly_features['activity_afternoon'] = sound[afternoon_mask].mean() if afternoon_mask.sum() > 0 else 0
            weekly_features['activity_evening'] = sound[evening_mask].mean() if evening_mask.sum() > 0 else 0
            
            # Seasonal
            weekly_features['month'] = df['collection_timestamp'].dt.month.iloc[0]
            weekly_features['yala_season'] = int(weekly_features['month'] in [5, 6, 7, 8])
            weekly_features['maha_season'] = int(weekly_features['month'] in [10, 11, 12, 1])
            
            agg_time = time.time() - agg_start_time
            logger.info(f"Aggregation complete in {agg_time:.2f}s, {len(weekly_features)} features calculated")
            
        except Exception as e:
            agg_time = time.time() - agg_start_time
            logger.error(f"Error during aggregation after {agg_time:.2f}s: {str(e)}")
            raise
        
        # Prepare features in correct order
        X = pd.DataFrame([weekly_features])
        
        # Get cached models (loaded once, reused)
        model_start_time = time.time()
        logger.info("Loading model artifacts...")
        
        try:
            model, scaler, metadata = get_cached_model()
            model_time = time.time() - model_start_time
            logger.info(f"Model artifacts loaded in {model_time:.2f}s")
            
            feature_cols = metadata['feature_columns']
            
            # Fill missing features with 0
            for feat in feature_cols:
                if feat not in X.columns:
                    X[feat] = 0
            
            # Extract features in correct order
            X_features = X[feature_cols].fillna(0)
            
            # Scale features
            logger.info("Scaling features...")
            X_scaled = scaler.transform(X_features)
            
            # Make prediction - FIXED: Set n_jobs to avoid hanging
            logger.info("Making prediction...")
            
            # Ensure n_jobs=1 to avoid multiprocessing issues in Flask
            if hasattr(model, 'set_params'):
                model.set_params(n_jobs=1)
            elif hasattr(model, 'estimators_'):
                # For ensemble models, set n_jobs on all estimators
                if hasattr(model, 'n_jobs'):
                    model.set_params(n_jobs=1)
                
            prediction = model.predict(X_scaled)[0]
            
            # Use predict_proba only if available (some models may not support it)
            try:
                probabilities = model.predict_proba(X_scaled)[0]
            except AttributeError:
                # If predict_proba not available, create default probabilities
                probabilities = [0.0, 0.0, 0.0, 0.0, 0.0]
                probabilities[int(prediction)] = 1.0
            
            logger.info("Prediction complete")
            
        except Exception as e:
            model_time = time.time() - model_start_time
            logger.error(f"Error during model prediction after {model_time:.2f}s: {str(e)}")
            raise
        
        total_time = time.time() - total_start_time
        logger.info(f"🎯 TOTAL PREDICTION TIME: {total_time:.2f}s")
        
        # Validate timing
        if total_time > 45:
            logger.warning(f"PREDICTION TOOK {total_time:.2f}s - MAY TIMEOUT AT 60s!")
        
        # Convert to performance level (1-5)
        prediction_level = prediction + 1
        
        level_meanings = {
            1: 'Excellent - Strong nectar flow, high foraging activity',
            2: 'Good - Consistent foraging, stable colony growth',
            3: 'Moderate - Maintenance phase, consumption equals collection',
            4: 'Poor - Colony consuming stored honey, stress indicators',
            5: 'Critical - Significant stress, potential collapse risk'
        }
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'predicted_level': int(prediction_level),
            'interpretation': level_meanings.get(prediction_level, 'Unknown'),
            'confidence': float(max(probabilities)),
            'all_probabilities': {
                f'Level_{i+1}': float(prob) for i, prob in enumerate(probabilities)
            },
            'data_points_used': len(records)
        }
        
        # Risk assessment
        if prediction_level >= 4:
            if max(probabilities) > 0.8:
                result['risk_assessment'] = "HIGH RISK - Immediate intervention recommended"
            else:
                result['risk_assessment'] = "MODERATE RISK - Monitor closely"
        elif prediction_level == 3:
            result['risk_assessment'] = "LOW RISK - Regular monitoring sufficient"
        else:
            result['risk_assessment'] = "OPTIMAL - Colony performing well"
        
        logger.info(f"Prediction successful: Level {prediction_level}, Confidence {max(probabilities):.2%}")
        return {'success': True, 'prediction': result}
        
    except Exception as e:
        logger.error(f"Error in predict_latest_performance: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}
