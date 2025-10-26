# ===============================================================================
# 🐝 Hive Performance Data Preprocessing
# Location: Badulla District, Sri Lanka
# Research-based ML model for precision apiculture
# 
# Fix: Aggregate 1-minute data to weekly summaries for temporal alignment
# ===============================================================================

import pandas as pd
import numpy as np
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*Invalid comparison between dtype=datetime64.*')
warnings.filterwarnings('ignore')

def load_and_explore_data(file_path):
    """Load and explore the hive dataset"""
    print("\n📊 LOADING DATASET...")
    
    data = pd.read_csv(file_path)
    print(f"Dataset shape: {data.shape}")
    print(f"Columns: {list(data.columns)}")
    print(f"Missing values: {data.isnull().sum().sum()}")
    
    return data

def prepare_base_features(df):
    """
    Create base features that will later be aggregated
    """
    print("\n🔧 PREPARING BASE FEATURES FOR AGGREGATION...")
    
    data = df.copy()
    data['collection_timestamp'] = pd.to_datetime(data['collection_timestamp'])
    data = data.sort_values(['hive_id', 'collection_timestamp']).reset_index(drop=True)
    
    # Temperature management
    data['temp_differential'] = data['sensor_temperature'] - data['weather_temperature']
    data['humidity_differential'] = data['sensor_humidity'] - data['weather_humidity']
    
    # Favorable foraging conditions (binary)
    data['favorable_foraging'] = (
        (data['weather_temperature'] > 15) &
        (data['weather_rainfall'] == 0) &
        (data['weather_wind_speed'] < 25) &
        (data['weather_light_intensity'] > 1000)
    ).astype(int)
    
    # Thermal stress (binary)
    data['thermal_stress'] = (
        (data['weather_temperature'] > 35) |
        (data['weather_temperature'] < 18)
    ).astype(int)
    
    # Sound activity (0-1 normalized)
    if data['sensor_sound'].max() != data['sensor_sound'].min():
        sound_min = data['sensor_sound'].min()
        sound_max = data['sensor_sound'].max()
        data['sound_activity'] = (data['sensor_sound'] - sound_min) / (sound_max - sound_min)
    else:
        data['sound_activity'] = 0
    
    # Temporal features
    data['hour'] = data['collection_timestamp'].dt.hour
    data['day'] = data['collection_timestamp'].dt.day
    data['month'] = data['collection_timestamp'].dt.month
    
    # Day/night classification (important for tropical apiculture)
    data['is_daytime'] = (data['hour'] >= 6) & (data['hour'] <= 18)
    
    # Temperature variance (stability indicator)
    data['temp_variance'] = abs(data['sensor_temperature'] - data['sensor_temperature'].mean())
    
    return data

def aggregate_to_weekly_data(df):
    """
    ✅ KEY FIX: Aggregate 1-minute data to weekly summaries
    This matches the temporal scale of your labels
    """
    print("\n📅 AGGREGATING DATA TO WEEKLY LEVELS...")
    
    data = df.copy()
    data['week'] = data['collection_timestamp'].dt.isocalendar().week
    data['year'] = data['collection_timestamp'].dt.year
    
    print(f"   Data spans from {data['collection_timestamp'].min()} to {data['collection_timestamp'].max()}")
    print(f"   Analyzing {data['hive_id'].nunique()} hives across {data['week'].nunique()} weeks")
    
    # Initialize weekly data structure
    weekly_data = []
    
    # Process each hive-week combination
    for (hive_id, year, week), group in data.groupby(['hive_id', 'year', 'week']):
        
        if len(group) < 100:  # Skip if insufficient data points
            continue
        
        # ==========================================
        # AGGREGATE NUMERICAL FEATURES
        # ==========================================
        
        weekly_row = {
            'hive_id': hive_id,
            'year': year,
            'week': week,
            'week_start': group['collection_timestamp'].min(),
            'week_end': group['collection_timestamp'].max(),
            'data_points': len(group)
        }
        
        # Weather aggregations
        weekly_row['avg_weather_temp'] = group['weather_temperature'].mean()
        weekly_row['min_weather_temp'] = group['weather_temperature'].min()
        weekly_row['max_weather_temp'] = group['weather_temperature'].max()
        weekly_row['avg_weather_humidity'] = group['weather_humidity'].mean()
        weekly_row['avg_weather_wind'] = group['weather_wind_speed'].mean()
        weekly_row['avg_weather_light'] = group['weather_light_intensity'].mean()
        weekly_row['total_weather_rainfall'] = group['weather_rainfall'].sum()
        
        # Sensor aggregations
        weekly_row['avg_sensor_temp'] = group['sensor_temperature'].mean()
        weekly_row['std_sensor_temp'] = group['sensor_temperature'].std()
        weekly_row['min_sensor_temp'] = group['sensor_temperature'].min()
        weekly_row['max_sensor_temp'] = group['sensor_temperature'].max()
        weekly_row['avg_sensor_humidity'] = group['sensor_humidity'].mean()
        weekly_row['avg_sensor_sound'] = group['sensor_sound'].mean()
        weekly_row['max_sensor_sound'] = group['sensor_sound'].max()
        
        # Weight metrics (CRITICAL for performance calculation)
        weekly_row['start_weight'] = group['sensor_weight'].iloc[0]
        weekly_row['end_weight'] = group['sensor_weight'].iloc[-1]
        weekly_row['min_weight'] = group['sensor_weight'].min()
        weekly_row['max_weight'] = group['sensor_weight'].max()
        weekly_row['avg_weight'] = group['sensor_weight'].mean()
        
        # Calculate weight change percentage
        if weekly_row['start_weight'] > 0:
            weight_change = weekly_row['end_weight'] - weekly_row['start_weight']
            weekly_row['weight_change_abs'] = weight_change
            weekly_row['weight_change_pct'] = (weight_change / weekly_row['start_weight']) * 100
        else:
            weekly_row['weight_change_abs'] = 0
            weekly_row['weight_change_pct'] = 0
        
        # ==========================================
        # AGGREGATE DERIVED FEATURES
        # ==========================================
        
        # Temperature differential (hive vs environment)
        weekly_row['avg_temp_differential'] = group['temp_differential'].mean()
        weekly_row['max_temp_differential'] = group['temp_differential'].max()
        weekly_row['min_temp_differential'] = group['temp_differential'].min()
        
        # Humidity differential
        weekly_row['avg_humidity_differential'] = group['humidity_differential'].mean()
        
        # ==========================================
        # AGGREGATE BINARY EVENTS (COUNT/PERCENTAGE)
        # ==========================================
        
        # Favorable foraging hours (count total minutes where conditions were good)
        weekly_row['total_favorable_foraging_minutes'] = group['favorable_foraging'].sum()
        weekly_row['pct_favorable_foraging'] = (group['favorable_foraging'].sum() / len(group)) * 100
        
        # Thermal stress events (count stressful periods)
        weekly_row['total_thermal_stress_minutes'] = group['thermal_stress'].sum()
        weekly_row['pct_thermal_stress'] = (group['thermal_stress'].sum() / len(group)) * 100
        
        # Sound activity (daytime vs nighttime)
        daytime_group = group[group['is_daytime'] == True]
        nighttime_group = group[group['is_daytime'] == False]
        
        weekly_row['avg_sound_activity_daytime'] = daytime_group['sound_activity'].mean() if len(daytime_group) > 0 else 0
        weekly_row['avg_sound_activity_nighttime'] = nighttime_group['sound_activity'].mean() if len(nighttime_group) > 0 else 0
        weekly_row['sound_activity_ratio'] = weekly_row['avg_sound_activity_daytime'] / (weekly_row['avg_sound_activity_nighttime'] + 0.001)
        
        # Temperature variance (stability)
        weekly_row['avg_temp_variance'] = group['temp_variance'].mean()
        weekly_row['max_temp_variance'] = group['temp_variance'].max()
        
        # ==========================================
        # TIME-BASED PATTERNS
        # ==========================================
        
        # Average hour of peak activity (when is hive most active?)
        weekly_row['peak_activity_hour'] = group.loc[group['sensor_sound'].idxmax(), 'hour']
        
        # Activity distribution by time of day
        weekly_row['activity_morning'] = group[(group['hour'] >= 6) & (group['hour'] < 12)]['sensor_sound'].mean()
        weekly_row['activity_afternoon'] = group[(group['hour'] >= 12) & (group['hour'] < 18)]['sensor_sound'].mean()
        weekly_row['activity_evening'] = group[(group['hour'] >= 18) & (group['hour'] < 22)]['sensor_sound'].mean()
        
        # Month (for seasonal patterns)
        weekly_row['month'] = group['month'].iloc[0]
        weekly_row['yala_season'] = weekly_row['month'] in [5, 6, 7, 8]
        weekly_row['maha_season'] = weekly_row['month'] in [10, 11, 12, 1]
        
        # Calculate PERFORMANCE LEVEL based on weight change
        weekly_row['performance_level'] = calculate_performance_level(weekly_row['weight_change_pct'])
        
        weekly_data.append(weekly_row)
    
    # Convert to DataFrame
    weekly_df = pd.DataFrame(weekly_data)
    
    print(f"\n✅ Weekly aggregation complete!")
    print(f"   Original: {len(data)} minute-level records")
    print(f"   Aggregated: {len(weekly_df)} week-level records")
    print(f"\n   Performance level distribution:")
    print(weekly_df['performance_level'].value_counts().sort_index())
    
    return weekly_df

def calculate_performance_level(weight_change_pct):
    """
    Calculate performance level based on weekly weight change
    """
        if weight_change_pct > 3:
            return 1  # Excellent
        elif 1 <= weight_change_pct <= 3:
            return 2  # Good
        elif -1 <= weight_change_pct <= 1:
            return 3  # Moderate
        elif -3 <= weight_change_pct < -1:
            return 4  # Poor
    else:  # weight_change_pct < -3
            return 5  # Critical
    
def get_feature_columns():
    """Return the list of weekly feature columns used for training"""
    return [
        # Weather features
        'avg_weather_temp', 'min_weather_temp', 'max_weather_temp',
        'avg_weather_humidity', 'avg_weather_wind',
        'avg_weather_light', 'total_weather_rainfall',
        
        # Sensor features
        'avg_sensor_temp', 'std_sensor_temp', 'min_sensor_temp', 'max_sensor_temp',
        'avg_sensor_humidity',
        'avg_sensor_sound', 'max_sensor_sound',
        
        # Weight features
        'start_weight', 'end_weight', 'avg_weight', 'min_weight', 'max_weight',
        
        # Differential features
        'avg_temp_differential', 'max_temp_differential', 'min_temp_differential',
        'avg_humidity_differential',
        
        # Aggregated binary features
        'pct_favorable_foraging', 'total_favorable_foraging_minutes',
        'pct_thermal_stress', 'total_thermal_stress_minutes',
        
        # Sound activity patterns
        'avg_sound_activity_daytime', 'avg_sound_activity_nighttime', 'sound_activity_ratio',
        
        # Temperature stability
        'avg_temp_variance', 'max_temp_variance',
        
        # Activity patterns
        'peak_activity_hour',
        'activity_morning', 'activity_afternoon', 'activity_evening',
        
        # Seasonal
        'month', 'yala_season', 'maha_season'
    ]

def preprocess_data(file_path):
    """Main preprocessing pipeline with weekly aggregation"""
    
    # Load data
    print("\n" + "="*80)
    print("🐝 HIVE PERFORMANCE PREPROCESSING - WEEKLY AGGREGATION")
    print("="*80)
    
    raw_data = load_and_explore_data(file_path)
    
    # Prepare base features
    processed_data = prepare_base_features(raw_data)
    
    # ✅ AGGREGATE to weekly level
    weekly_data = aggregate_to_weekly_data(processed_data)
    
    # Get feature columns
    feature_cols = get_feature_columns()
    
    # Filter to only include features that exist in our aggregated data
    available_features = [f for f in feature_cols if f in weekly_data.columns]
    
    print(f"\n✅ Preprocessing complete!")
    print(f"   Weekly records: {len(weekly_data)}")
    print(f"   Features: {len(available_features)}")
    
    return weekly_data, available_features

if __name__ == "__main__":
    # Example usage
    file_path = "data/hive_data3.csv"
    data, features = preprocess_data(file_path)
    
    print(f"\n📊 FINAL DATASET INFO:")
    print(f"   Shape: {data.shape}")
    print(f"   Features: {len(features)}")
    print(f"   Target distribution: {data['performance_level'].value_counts().sort_index().to_dict()}")

