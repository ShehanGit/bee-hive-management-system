from pathlib import Path
import pandas as pd
import numpy as np

# threat_detection/
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PACKAGE_ROOT / "data"

# 👇 Use the synthetic dataset by default
DEFAULT_CSV = DATA_DIR / "bee_threat_dataset_synthetic.csv"

# Final feature list used for BOTH training and prediction
FEATURES_BASE = [
    "weather_temp_c",
    "weather_humidity_pct",
    "hive_sound_db",
    "hive_sound_peak_freq",
    "vibration_hz",
    "vibration_var",
    "hour",
    "dayofweek",
    "is_evening",
    "temp_humidity",
    "sound_roll3",
    "vib_roll3",
    "sound_var3",
    "vib_var3",
    "db_to_vib_ratio",
    "peak_to_vib_ratio",
]

def _add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["hour"] = df["timestamp"].dt.hour.fillna(0).astype(int)
        df["dayofweek"] = df["timestamp"].dt.dayofweek.fillna(0).astype(int)
    else:
        df["hour"] = 12
        df["dayofweek"] = 0
    df["is_evening"] = df["hour"].between(19, 22).astype(int)
    return df

def _add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:
    # If you ever add hive_id, this will compute per-hive windows automatically
    if "hive_id" in df.columns and "timestamp" in df.columns:
        df = df.sort_values(["hive_id", "timestamp"]).reset_index(drop=True)
        grp = df.groupby("hive_id")
        df["sound_roll3"] = grp["hive_sound_db"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)
        df["vib_roll3"] = grp["vibration_hz"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True)
        df["sound_var3"] = grp["hive_sound_db"].rolling(3, min_periods=1).var().reset_index(level=0, drop=True).fillna(0)
        df["vib_var3"] = grp["vibration_hz"].rolling(3, min_periods=1).var().reset_index(level=0, drop=True).fillna(0)
    else:
        # Fallbacks if no grouping keys exist (synthetic dataset case)
        df["sound_roll3"] = df["hive_sound_db"]
        df["vib_roll3"] = df["vibration_hz"]
        df["sound_var3"] = 0.0
        df["vib_var3"] = 0.0
    return df

def _add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
    df["temp_humidity"] = df["weather_temp_c"] * df["weather_humidity_pct"]
    # Ratios (avoid divide-by-zero)
    df["db_to_vib_ratio"] = df["hive_sound_db"] / np.clip(df["vibration_hz"], 1e-3, None)
    df["peak_to_vib_ratio"] = df["hive_sound_peak_freq"] / np.clip(df["vibration_hz"], 1e-3, None)
    return df

def load_and_prepare(csv_path: str | Path = None):
    csv_path = Path(csv_path) if csv_path is not None else DEFAULT_CSV
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found at {csv_path}")

    df = pd.read_csv(csv_path, low_memory=False)
    df.columns = [c.strip() for c in df.columns]

    # Ensure numeric types (synthetic dataset includes these extra columns)
    numeric_cols = [
        "weather_temp_c", "weather_humidity_pct", "hive_sound_db",
        "hive_sound_peak_freq", "vibration_hz", "vibration_var"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = _add_time_features(df)
    df = _add_rolling_features(df)
    df = _add_interaction_features(df)

    df = df.dropna(subset=["weather_temp_c","weather_humidity_pct","hive_sound_db",
                           "hive_sound_peak_freq","vibration_hz","vibration_var"])

    if "threat_type" not in df.columns:
        raise ValueError("Column 'threat_type' not found in dataset")

    X = df[FEATURES_BASE].copy()
    y = df["threat_type"].astype(str).copy()
    return df, X, y, FEATURES_BASE
