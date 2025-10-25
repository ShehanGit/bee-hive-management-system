# ===============================================================================
# 🐝 Hive Performance Prediction Service
# Location: Badulla District, Sri Lanka
# Research-based ML model for precision apiculture
# ===============================================================================

import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime
import warnings

# Suppress pandas warnings for datetime comparisons
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*Invalid comparison between dtype=datetime64.*')
warnings.filterwarnings('ignore')

class HivePerformancePredictor:
    """Hive Performance Prediction Service"""
    
    def __init__(self, model_path="models/performance_model.pkl", 
                 scaler_path="models/scaler.pkl",
                 metadata_path="models/performance_model_meta.json"):
        """Initialize the prediction service"""
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.metadata_path = metadata_path
        self.model = None
        self.scaler = None
        self.metadata = None
        self.feature_cols = None
        self.load_model_artifacts()
        
    def load_model_artifacts(self):
        """Load trained model, scaler, and metadata"""
        try:
            print("📦 Loading model artifacts...")
            
            # Load model
            self.model = joblib.load(self.model_path)
            print(f"✅ Model loaded: {self.model_path}")
            
            # Load scaler
            self.scaler = joblib.load(self.scaler_path)
            print(f"✅ Scaler loaded: {self.scaler_path}")
            
            # Load metadata
            with open(self.metadata_path, 'r') as f:
                self.metadata = json.load(f)
            print(f"✅ Metadata loaded: {self.metadata_path}")
            
            # Extract feature columns
            self.feature_cols = self.metadata['feature_columns']
            print(f"✅ Feature columns loaded: {len(self.feature_cols)} features")
            
        except Exception as e:
            print(f"❌ Error loading model artifacts: {str(e)}")
            raise
    
    def preprocess_single_observation(self, data_row):
        """Preprocess a single observation for prediction"""
        # Convert to DataFrame if it's a dictionary
        if isinstance(data_row, dict):
            data = pd.DataFrame([data_row])
        else:
            data = data_row.copy()
        
        # Apply feature engineering (simplified version)
        try:
            # Suppress pandas warnings
            import warnings
            warnings.filterwarnings('ignore', category=FutureWarning)
            
            # Convert timestamp
            if 'collection_timestamp' in data.columns:
                data['collection_timestamp'] = pd.to_datetime(data['collection_timestamp'])
            else:
                data['collection_timestamp'] = pd.to_datetime(datetime.now())
            
            # Core predictive features
            if 'sensor_temperature' in data.columns and 'weather_temperature' in data.columns:
                data['temp_differential'] = data['sensor_temperature'] - data['weather_temperature']
            else:
                data['temp_differential'] = 0
                
            if 'sensor_humidity' in data.columns and 'weather_humidity' in data.columns:
                data['humidity_differential'] = data['sensor_humidity'] - data['weather_humidity']
            else:
                data['humidity_differential'] = 0
            
            # Favorable foraging conditions
            data['favorable_foraging'] = 0
            if all(col in data.columns for col in ['weather_temperature', 'weather_rainfall', 'weather_wind_speed', 'weather_light_intensity']):
                data['favorable_foraging'] = (
                    (data['weather_temperature'] > 15) &
                    (data['weather_rainfall'] == 0) &
                    (data['weather_wind_speed'] < 25) &
                    (data['weather_light_intensity'] > 1000)
                ).astype(int)
            
            # Thermal stress
            data['thermal_stress'] = 0
            if 'weather_temperature' in data.columns:
                data['thermal_stress'] = (
                    (data['weather_temperature'] > 35) |
                    (data['weather_temperature'] < 18)
                ).astype(int)
            
            # Sound activity normalization
            if 'sensor_sound' in data.columns:
                # Use fixed normalization values or defaults
                data['sound_activity'] = np.clip(data['sensor_sound'] / 100.0, 0, 1)  # Assuming max sound ~100
            else:
                data['sound_activity'] = 0.5
            
            # Temporal features
            data['hour'] = data['collection_timestamp'].dt.hour
            data['month'] = data['collection_timestamp'].dt.month
            
            # Cyclical encoding
            data['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24)
            data['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24)
            data['month_sin'] = np.sin(2 * np.pi * data['month'] / 12)
            data['month_cos'] = np.cos(2 * np.pi * data['month'] / 12)
            
            # Sri Lankan monsoon seasons
            data['yala_season'] = data['month'].isin([5, 6, 7, 8]).astype(int)
            data['maha_season'] = data['month'].isin([10, 11, 12, 1]).astype(int)
            
            # Rolling features (simplified - use defaults for single predictions)
            data['temp_variance_1h'] = 0.5  # Default variance
            data['sound_trend_1h'] = data.get('sensor_sound', 50)  # Use current sound or default
            data['weather_stability_1h'] = 1.0  # Default stability
            
        except Exception as e:
            print(f"⚠️ Warning in feature engineering: {str(e)}")
            # Set default values for missing features
            for col in self.feature_cols:
                if col not in data.columns:
                    data[col] = 0
        
        return data
    
    def predict_single(self, data_row):
        """Make prediction for a single observation"""
        try:
            # Preprocess data
            processed_data = self.preprocess_single_observation(data_row)
            
            # Extract features
            X = processed_data[self.feature_cols].fillna(0)
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make prediction
            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]
            
            # Convert back to original scale (1-5)
            prediction_original = prediction + 1
            
            # Get interpretation
            level_meanings = {
                1: 'Excellent - Strong nectar flow, high foraging activity',
                2: 'Good - Consistent foraging, stable colony growth',
                3: 'Moderate - Maintenance phase, consumption equals collection',
                4: 'Poor - Colony consuming stored honey, stress indicators',
                5: 'Critical - Significant stress, potential collapse risk'
            }
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'predicted_level': int(prediction_original),
                'interpretation': level_meanings.get(prediction_original, 'Unknown'),
                'confidence': float(max(probabilities)),
                'all_probabilities': {
                    f'Level_{i+1}': float(prob) for i, prob in enumerate(probabilities)
                },
                'risk_assessment': self._assess_risk(prediction_original, max(probabilities))
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error in prediction: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def predict_batch(self, data_df):
        """Make predictions for multiple observations"""
        results = []
        print(f"🔮 Making predictions for {len(data_df)} observations...")
        for idx, row in data_df.iterrows():
            # Convert Series to DataFrame for predict_single
            row_df = row.to_frame().T
            result = self.predict_single(row_df)
            result['observation_id'] = idx
            results.append(result)
        return results
    
    def _assess_risk(self, predicted_level, confidence):
        """Assess risk level based on prediction and confidence"""
        if predicted_level >= 4:  # Poor or Critical
            if confidence > 0.8:
                return "HIGH RISK - Immediate intervention recommended"
            else:
                return "MODERATE RISK - Monitor closely"
        elif predicted_level == 3:  # Moderate
            return "LOW RISK - Regular monitoring sufficient"
        else:  # Good or Excellent
            return "OPTIMAL - Colony performing well"
    
    def get_model_info(self):
        """Get information about the loaded model"""
        return {
            'model_name': self.metadata.get('model_name', 'Unknown'),
            'training_date': self.metadata.get('training_date', 'Unknown'),
            'feature_count': len(self.feature_cols),
            'performance_levels': self.metadata.get('performance_levels', {}),
            'model_type': self.metadata.get('model_type', 'hive_performance_prediction')
        }

def create_sample_prediction():
    """Create a sample prediction for testing"""
    # Sample data
    sample_data = {
        'collection_timestamp': '2024-12-01 14:30:00',
        'hive_id': 'HIVE_001',
        'weather_temperature': 28.5,
        'weather_humidity': 65.0,
        'weather_wind_speed': 12.0,
        'weather_light_intensity': 45000.0,
        'weather_rainfall': 0.0,
        'sensor_temperature': 35.2,
        'sensor_humidity': 55.0,
        'sensor_sound': 75.0,
        'sensor_weight': 45.2
    }
    
    # Initialize predictor
    predictor = HivePerformancePredictor()
    
    # Make prediction
    result = predictor.predict_single(sample_data)
    
    print("🔮 SAMPLE PREDICTION RESULT:")
    print("=" * 50)
    print(f"Hive ID: {sample_data['hive_id']}")
    print(f"Timestamp: {sample_data['collection_timestamp']}")
    print(f"Predicted Level: {result.get('predicted_level', 'Error')}")
    print(f"Interpretation: {result.get('interpretation', 'Error')}")
    print(f"Confidence: {result.get('confidence', 0):.1%}")
    print(f"Risk Assessment: {result.get('risk_assessment', 'Unknown')}")
    
    return result

if __name__ == "__main__":
    # Example usage
    try:
        # Create sample prediction
        sample_result = create_sample_prediction()
        
        # Test model info
        predictor = HivePerformancePredictor()
        model_info = predictor.get_model_info()
        print(f"\n📊 MODEL INFO:")
        print(f"Model: {model_info['model_name']}")
        print(f"Features: {model_info['feature_count']}")
        print(f"Type: {model_info['model_type']}")
        
    except Exception as e:
        print(f"❌ Error in prediction service: {str(e)}")
        print("Make sure the model files exist in the models/ directory")