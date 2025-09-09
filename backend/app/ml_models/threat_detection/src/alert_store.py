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
            with open(ALERTS_FILE, "r") as f:
                _alerts = json.load(f)
        except Exception:
            _alerts = []
    else:
        _alerts = []
    return _alerts

def save_alerts():
    with open(ALERTS_FILE, "w") as f:
        json.dump(_alerts, f, indent=2, default=str)

def add_alert(threat_type, probability, used_features):
    timestamp = datetime.utcnow().isoformat()
    alert = {
        "timestamp": timestamp,
        "threat_type": threat_type,
        "probability": probability,
        "used_features": used_features
    }
    _alerts.insert(0, alert)
    del _alerts[200:]
    save_alerts()
    return alert

# load on import
load_alerts()
