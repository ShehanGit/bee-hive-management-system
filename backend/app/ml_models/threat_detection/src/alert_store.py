from pathlib import Path
import json
from datetime import datetime
import os

from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# ========== JSON FALLBACK ==========
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = PACKAGE_ROOT / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True, parents=True)
ALERTS_FILE = OUTPUTS_DIR / "alerts.json"

_alerts = []  # in-memory alerts

# # ========== MYSQL SETUP ==========
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "mysql+pymysql://beehive_user:BeePass123@127.0.0.1:3306/beehive_db"
# )
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/hive_db"
)

Base = declarative_base()
SessionLocal = None
engine = None

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    class ThreatAlert(Base):
        __tablename__ = "threat_alerts"
        id = Column(Integer, primary_key=True, autoincrement=True)
        timestamp = Column(DateTime, default=datetime.utcnow)
        threat_type = Column(String(64), nullable=False)
        probability = Column(Float, nullable=False)
        recommendations = Column(Text, nullable=True)
        used_features_json = Column(Text, nullable=True)

    # create table if not exists
    Base.metadata.create_all(bind=engine)
    db_available = True
except Exception as e:
    print(f"[alert_store] ⚠ Falling back to JSON storage: {e}")
    db_available = False


# ========== JSON FUNCTIONS ==========
def load_alerts():
    """Load alerts from DB if available, else JSON file."""
    global _alerts
    if db_available:
        try:
            session = SessionLocal()
            rows = session.query(ThreatAlert).order_by(ThreatAlert.timestamp.desc()).limit(500).all()
            _alerts = [
                {
                    "timestamp": row.timestamp.isoformat(),
                    "threat_type": row.threat_type,
                    "probability": row.probability,
                    "recommendations": json.loads(row.recommendations) if row.recommendations else None,
                    "used_features": json.loads(row.used_features_json) if row.used_features_json else None,
                }
                for row in rows
            ]
            session.close()
            return _alerts
        except SQLAlchemyError as e:
            print(f"[alert_store] DB load failed, fallback to JSON: {e}")

    # Fallback to JSON
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
    """Persist in-memory alerts to JSON (only fallback)."""
    try:
        with open(ALERTS_FILE, "w", encoding="utf-8") as f:
            json.dump(_alerts, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[alert_store] Failed to save alerts to JSON: {e}")


def add_alert(threat_type, probability, used_features, recommendations=None):
    """
    Add an alert to DB if available, else JSON.
    recommendations: dict from recommendation_service.get_recommendations()
    """
    timestamp = datetime.utcnow()

    # Try saving to DB
    if db_available:
        try:
            session = SessionLocal()
            new_alert = ThreatAlert(
                timestamp=timestamp,
                threat_type=threat_type,
                probability=probability,
                recommendations=json.dumps(recommendations) if recommendations else None,
                used_features_json=json.dumps(used_features) if used_features else None,
            )
            session.add(new_alert)
            session.commit()
            session.refresh(new_alert)
            session.close()

            alert_dict = {
                "timestamp": timestamp.isoformat(),
                "threat_type": threat_type,
                "probability": probability,
                "recommendations": recommendations,
                "used_features": used_features,
            }
            _alerts.insert(0, alert_dict)
            if len(_alerts) > 500:
                del _alerts[500:]
            return alert_dict
        except SQLAlchemyError as e:
            print(f"[alert_store] DB insert failed, fallback to JSON: {e}")

    # JSON fallback
    alert = {
        "timestamp": timestamp.isoformat(),
        "threat_type": threat_type,
        "probability": probability,
        "used_features": used_features,
        "recommendations": recommendations,
    }
    _alerts.insert(0, alert)
    if len(_alerts) > 500:
        del _alerts[500:]
    save_alerts()
    return alert


# Load alerts on import
load_alerts()
