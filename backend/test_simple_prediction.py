"""Simple test - load model and predict with minimal data"""
import sys
import os
import time
import numpy as np
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

print("Loading model...")
import joblib
model_path = 'app/ml_models/performance_prediction/models/performance_model.pkl'
scaler_path = 'app/ml_models/performance_prediction/models/scaler.pkl'
meta_path = 'app/ml_models/performance_prediction/models/performance_model_meta.json'

# Load metadata
with open(meta_path, 'r') as f:
    metadata = json.load(f)

# Load model
start = time.time()
model = joblib.load(model_path)
print(f"Model loaded in {time.time() - start:.2f}s")
print(f"Model type: {type(model)}")
print(f"n_jobs: {getattr(model, 'n_jobs', 'N/A')}")

# Load scaler
scaler = joblib.load(scaler_path)

# Create dummy features (39 features as expected by model)
features = metadata['feature_columns']
print(f"Expected {len(features)} features")

# Create a simple test input with all zeros (1 row, 39 features)
X = np.zeros((1, len(features)))

# Scale it
X_scaled = scaler.transform(X)

# Try prediction with n_jobs=1
print("\nSetting n_jobs=1...")
model.set_params(n_jobs=1)
print(f"n_jobs after setting: {model.n_jobs}")

print("\nMaking prediction...")
start = time.time()
prediction = model.predict(X_scaled)[0]
probabilities = model.predict_proba(X_scaled)[0]
elapsed = time.time() - start

print(f"✅ Prediction completed in {elapsed:.2f}s")
print(f"Predicted level: {prediction + 1}")
print(f"Probabilities: {probabilities}")

