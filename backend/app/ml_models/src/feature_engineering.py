import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate great-circle distance between two points on Earth using Haversine formula.
    """
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create new features based on existing columns. For example:
    - Distance from known water source
    - Seasonal or categorical encodings
    - Normalization/Scaling
    """
    # Example: Calculate distance to a known resource (lat=6.9271, lng=79.8612) just for demonstration
    # Replace with your actual resource lat/lng.
    resource_lat, resource_lng = 6.9271, 79.8612
    
    df['dist_to_resource'] = df.apply(
        lambda row: haversine_distance(
            row['hive_lat'], row['hive_lng'], resource_lat, resource_lng
        ), axis=1
    )
    
    # Example: Add a normalized version of your honey_production or distance
    df['dist_to_resource_norm'] = (df['dist_to_resource'] - df['dist_to_resource'].mean()) / df['dist_to_resource'].std()
    
    # More advanced feature engineering or transformations can be added here
    return df

if __name__ == "__main__":
    # Example usage:
    from data_preprocessing import load_and_clean_data
    data = load_and_clean_data("./data/hive_data.xlsx")
    data_fe = engineer_features(data)
    print(data_fe.head())
