# ===============================================================================
# 🐝 Hive Performance Data Preprocessing
# Location: Badulla District, Sri Lanka
# Research-based ML model for precision apiculture
# ===============================================================================

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_and_explore_data(file_path):
    """Load and explore the hive dataset"""
    print("\n📊 LOADING DATASET...")
    
    data = pd.read_csv(file_path)
    print(f"Dataset shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    print(f"Missing values: {data.isnull().sum().sum()}")
    print(f"Data types:\n{data.dtypes}")
    
    return data

def create_advanced_features(df):
    """
    Create research-based features for Sri Lankan hive monitoring
    Based on methodology for tropical climate conditions
    """
    print("\n🔧 CREATING ADVANCED FEATURES...")
    
    data = df.copy()
    
    # Convert timestamp and sort
    data['collection_timestamp'] = pd.to_datetime(data['collection_timestamp'])
    data = data.sort_values(['hive_id', 'collection_timestamp']).reset_index(drop=True)
    
    # ================================
    # CORE PREDICTIVE FEATURES
    # ================================
    
    # Temperature management (key indicator of colony health)
    data['temp_differential'] = data['sensor_temperature'] - data['weather_temperature']
    data['humidity_differential'] = data['sensor_humidity'] - data['weather_humidity']
    
    # Sri Lankan tropical foraging conditions
    data['favorable_foraging'] = (
        (data['weather_temperature'] > 15) &
        (data['weather_rainfall'] == 0) &
        (data['weather_wind_speed'] < 25) &
        (data['weather_light_intensity'] > 1000)
    ).astype(int)
    
    # Thermal stress for tropical climate
    data['thermal_stress'] = (
        (data['weather_temperature'] > 35) |
        (data['weather_temperature'] < 18)
    ).astype(int)
    
    # Sound activity normalization
    if data['sensor_sound'].max() != data['sensor_sound'].min():
        sound_min = data['sensor_sound'].min()
        sound_max = data['sensor_sound'].max()
        data['sound_activity'] = (data['sensor_sound'] - sound_min) / (sound_max - sound_min)
    else:
        data['sound_activity'] = 0
    
    # ================================
    # TEMPORAL FEATURES (Cyclical)
    # ================================
    data['hour'] = data['collection_timestamp'].dt.hour
    data['day_of_week'] = data['collection_timestamp'].dt.dayofweek
    data['month'] = data['collection_timestamp'].dt.month
    
    # Cyclical encoding
    data['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24)
    data['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24)
    data['month_sin'] = np.sin(2 * np.pi * data['month'] / 12)
    data['month_cos'] = np.cos(2 * np.pi * data['month'] / 12)
    
    # Sri Lankan monsoon seasons
    data['yala_season'] = data['month'].isin([5, 6, 7, 8]).astype(int)  # May-Aug
    data['maha_season'] = data['month'].isin([10, 11, 12, 1]).astype(int)  # Oct-Jan
    
    # ================================
    # ROLLING WINDOW FEATURES
    # ================================
    
    # Sort by hive and time for rolling calculations
    data = data.sort_values(['hive_id', 'collection_timestamp'])
    
    # 1-hour rolling features (60 minutes = 60 samples at 1-minute intervals)
    window_1h = 60
    
    # Temperature variance (brood nest health indicator)
    data['temp_variance_1h'] = data.groupby('hive_id')['sensor_temperature'].rolling(
        window=window_1h, min_periods=1
    ).var().reset_index(0, drop=True)
    
    # Sound trend
    data['sound_trend_1h'] = data.groupby('hive_id')['sensor_sound'].rolling(
        window=window_1h, min_periods=1
    ).mean().reset_index(0, drop=True)
    
    # Weather stability
    data['weather_stability_1h'] = data.groupby('hive_id')['weather_temperature'].rolling(
        window=window_1h, min_periods=1
    ).std().reset_index(0, drop=True)
    
    # Fill NaN values
    data['temp_variance_1h'] = data['temp_variance_1h'].fillna(0)
    data['sound_trend_1h'] = data['sound_trend_1h'].fillna(data['sensor_sound'].median())
    data['weather_stability_1h'] = data['weather_stability_1h'].fillna(0)
    
    # ================================
    # PERFORMANCE LEVEL CALCULATION
    # ================================
    
    # Weekly weight change calculation
    data['week'] = data['collection_timestamp'].dt.isocalendar().week
    data['year'] = data['collection_timestamp'].dt.year
    
    def calculate_weekly_performance(group):
        """Calculate weekly weight change percentage"""
        if len(group) < 2:
            return 3  # Default moderate
        
        first_weight = group['sensor_weight'].iloc[0]
        last_weight = group['sensor_weight'].iloc[-1]
        
        if first_weight == 0:
            return 3
        
        weight_change_pct = ((last_weight - first_weight) / first_weight) * 100
        
        # Research-based performance levels
        if weight_change_pct > 3:
            return 1  # Excellent
        elif 1 <= weight_change_pct <= 3:
            return 2  # Good
        elif -1 <= weight_change_pct <= 1:
            return 3  # Moderate
        elif -3 <= weight_change_pct < -1:
            return 4  # Poor
        else:  # < -3
            return 5  # Critical
    
    # Calculate performance by week and hive
    weekly_performance = data.groupby(['hive_id', 'year', 'week']).apply(
        calculate_weekly_performance
    ).reset_index(name='performance_level')
    
    # Merge back to main dataset
    data = data.merge(weekly_performance, on=['hive_id', 'year', 'week'], how='left')
    data['performance_level'] = data['performance_level'].fillna(3).astype(int)
    
    print(f"✅ Feature engineering complete!")
    print(f"Dataset shape: {data.shape}")
    print(f"Performance level distribution:")
    print(data['performance_level'].value_counts().sort_index())
    
    return data

def get_feature_columns():
    """Return the list of feature columns used for training"""
    return [
        'weather_temperature', 'weather_humidity', 'weather_wind_speed',
        'weather_light_intensity', 'weather_rainfall',
        'sensor_temperature', 'sensor_humidity', 'sensor_sound',
        'temp_differential', 'humidity_differential', 'favorable_foraging',
        'thermal_stress', 'sound_activity',
        'hour_sin', 'hour_cos', 'month_sin', 'month_cos',
        'yala_season', 'maha_season',
        'temp_variance_1h', 'sound_trend_1h', 'weather_stability_1h'
    ]

def preprocess_data(file_path):
    """Main preprocessing pipeline"""
    # Load data
    raw_data = load_and_explore_data(file_path)
    
    # Create features
    processed_data = create_advanced_features(raw_data)
    
    # Get feature columns
    feature_cols = get_feature_columns()
    
    return processed_data, feature_cols

if __name__ == "__main__":
    # Example usage
    file_path = "data/bee_performance_dataset_synthetic.csv"
    data, features = preprocess_data(file_path)
    print(f"Preprocessing completed. Features: {len(features)}")