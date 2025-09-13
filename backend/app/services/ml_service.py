# app/services/ml_service.py

import joblib
import pandas as pd
import os
from app.services.potential_location_service import get_all_potential_locations, update_potential_location
from app.ml_models.src.feature_engineering import engineer_features

# Load the model using a relative path (no app context needed)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Adjust levels: from services/ to backend/
MODEL_PATH = os.path.join(base_dir, 'app', 'ml_models', 'random_forest_model.pkl')
model = joblib.load(MODEL_PATH)
expected_features = model.feature_names_in_

def predict_for_all_locations():
    """Fetch all locations, prepare DF, predict, and update honey_production in DB."""
    locs = get_all_potential_locations()
    if not locs:
        return 0  # No updates

    data_list = [{
        'hive_lat': loc.lat,  # Adjust if your model uses 'lat' instead of 'hive_lat'
        'hive_lng': loc.lng,
        'temperature': loc.temperature,
        'humidity': loc.humidity,
        'sunlight_exposure': loc.sunlight_exposure,
        'wind_speed': loc.wind_speed,
        'dist_to_water_source': loc.dist_to_water_source,
        'dist_to_flowering_area': loc.dist_to_flowering_area,
        'dist_to_feeding_station': loc.dist_to_feeding_station
    } for loc in locs]

    df = pd.DataFrame(data_list)
    df = engineer_features(df)  # Apply engineering (e.g., adds dist_to_resource)

    # Handle missing features
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0
    df = df[expected_features]

    # Predict
    predictions = model.predict(df)

    # Update DB
    updated_count = 0
    for loc, pred in zip(locs, predictions):
        update_potential_location(loc.id, {'honey_production': pred})
        updated_count += 1
    return updated_count