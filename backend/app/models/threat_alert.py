from datetime import datetime
from app import db

class ThreatAlert(db.Model):
    __tablename__ = "threat_alerts"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    threat_type = db.Column(db.String(64), index=True, nullable=False)
    probability = db.Column(db.Float, nullable=False)
    recommendation = db.Column(db.Text, nullable=True)
    used_features_json = db.Column(db.Text, nullable=True)

    def to_dict(self):
        import json
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "threat_type": self.threat_type,
            "probability": self.probability,
            "recommendation": self.recommendation,
            "used_features": json.loads(self.used_features_json or "{}")
        }
