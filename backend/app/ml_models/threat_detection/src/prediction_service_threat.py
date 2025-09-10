from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from datetime import datetime

from .data_preprocessing_threat import PACKAGE_ROOT, FEATURES_BASE

MODEL_FILE = PACKAGE_ROOT / "models" / "threat_model.pkl"
_bundle_cache = None

def _load_bundle():
    global _bundle_cache
    if _bundle_cache is None:
        _bundle_cache = joblib.load(MODEL_FILE)
    return _bundle_cache

def get_model_meta():
    b = _load_bundle()
    return {
        "classes": list(b["label_encoder"].classes_),
        "features": b["features"]
    }

def _build_feature_row(payload: dict):
    row = {}
    # Core numeric features with safe defaults
    row["weather_temp_c"] = float(payload.get("weather_temp_c", 30.0))
    row["weather_humidity_pct"] = float(payload.get("weather_humidity_pct", 60.0))
    row["hive_sound_db"] = float(payload.get("hive_sound_db", 70.0))
    row["hive_sound_peak_freq"] = float(payload.get("hive_sound_peak_freq", 200.0))
    row["vibration_hz"] = float(payload.get("vibration_hz", 200.0))
    row["vibration_var"] = float(payload.get("vibration_var", 10.0))

    # Time-based features
    ts = payload.get("timestamp")
    if ts:
        try:
            ts = pd.to_datetime(ts)
        except Exception:
            ts = datetime.utcnow()
    else:
        ts = datetime.utcnow()
    row["hour"] = int(ts.hour)
    row["dayofweek"] = int(ts.weekday())
    row["is_evening"] = 1 if 19 <= row["hour"] <= 22 else 0

    # Interactions / rolling proxies
    row["temp_humidity"] = row["weather_temp_c"] * row["weather_humidity_pct"]

    # If you stream history you can pass these; otherwise fallback to current values
    row["sound_roll3"] = float(payload.get("sound_roll3", row["hive_sound_db"]))
    row["vib_roll3"] = float(payload.get("vib_roll3", row["vibration_hz"]))
    row["sound_var3"] = float(payload.get("sound_var3", 0.0))
    row["vib_var3"] = float(payload.get("vib_var3", 0.0))

    row["db_to_vib_ratio"] = row["hive_sound_db"] / max(row["vibration_hz"], 1e-3)
    row["peak_to_vib_ratio"] = row["hive_sound_peak_freq"] / max(row["vibration_hz"], 1e-3)

    df = pd.DataFrame([row])
    return df[FEATURES_BASE]

def predict_threat(payload: dict):
    b = _load_bundle()
    model = b["model"]
    le = b["label_encoder"]
    X = _build_feature_row(payload)
    pred_idx = model.predict(X)[0]
    proba = None
    if hasattr(model, "predict_proba"):
        proba = float(np.max(model.predict_proba(X)))
    label = le.inverse_transform([pred_idx])[0]
    return {
        "threat_type": label,
        "probability": proba,
        "used_features": X.to_dict(orient="records")[0]
    }
