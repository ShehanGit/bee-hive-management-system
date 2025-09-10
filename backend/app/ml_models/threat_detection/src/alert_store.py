# backend/app/ml_models/threat_detection/src/alert_store.py
from pathlib import Path
import json
from datetime import datetime

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PACKAGE_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)
ALERTS_FILE = OUTPUTS_DIR / "alerts.json"

_alerts = []

def load_alerts():
    global _alerts
    if ALERTS_FILE.exists():
        try:
            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                _alerts = json.load(f)
        except Exception:
            _alerts = []
    else:
        _alerts = []
    return _alerts

def save_alerts():
    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        json.dump(_alerts, f, indent=2, ensure_ascii=False)

def add_alert(threat_type, probability, used_features, recommendations=None):
    """
    Add an alert to in-memory list and persist to outputs/alerts.json
    recommendations: optional dict returned by recommendation_service.get_recommendations()
    """
    timestamp = datetime.utcnow().isoformat()
    alert = {
        "timestamp": timestamp,
        "threat_type": threat_type,
        "probability": probability,
        "used_features": used_features,
        "recommendations": recommendations
    }
    # newest first
    _alerts.insert(0, alert)
    # keep list bounded
    if len(_alerts) > 500:
        del _alerts[500:]
    save_alerts()
    return alert

# Load existing alerts at import time
load_alerts()
