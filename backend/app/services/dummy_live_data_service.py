import random
from datetime import datetime
import requests
from app.models.threat_alert import ThreatAlert
from app.extensions import db
from app.ml_models.threat_detection.src import alert_store

# Generate dummy sensor data
def generate_dummy_data():
    return {
        "weather_temp_c": round(random.uniform(25, 35), 2),
        "weather_humidity_pct": round(random.uniform(60, 90), 2),
        "hive_sound_db": round(random.uniform(50, 90), 2),
        "hive_sound_peak_freq": round(random.uniform(200, 500), 2),
        "vibration_hz": round(random.uniform(10, 100), 2),
        "vibration_var": round(random.uniform(0.1, 5.0), 2),
    }

def fetch_and_save_dummy_data():
    try:
        # Generate fake input
        data = generate_dummy_data()

        # Call the existing Flask predict endpoint (same as frontend does)
        res = requests.post("http://127.0.0.1:5000/api/threat/predict", json=data)
        if res.status_code != 200:
            print("[dummy] Prediction request failed:", res.text)
            return

        prediction = res.json()
        threat_type = prediction.get("threat_type", "Unknown")
        probability = prediction.get("probability", 0.0)

        # Create DB alert
        alert = ThreatAlert(
            timestamp=datetime.utcnow(),
            threat_type=threat_type,
            probability=probability,
            used_features_json=str(data),
            recommendations=str(prediction.get("recommendations", {}))
        )
        db.session.add(alert)
        db.session.commit()

        # Also store in JSON fallback
        alert_store.add_alert(threat_type, probability, data, prediction.get("recommendations", {}))

        print(f"[dummy] ✅ Added dummy alert: {threat_type} ({probability*100:.1f}%)")

    except Exception as e:
        print("[dummy] ❌ Error generating dummy data:", e)
