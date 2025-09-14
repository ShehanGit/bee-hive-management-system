from apscheduler.schedulers.background import BackgroundScheduler
from app.services.iot_integration_service import fetch_and_save_iot_data
from app.services.dummy_live_data_service import fetch_and_save_dummy_data
import logging

def start_scheduler(app):
    scheduler = BackgroundScheduler(timezone="UTC")

    def scheduled_job():
        with app.app_context():
            try:
                # Try fetching from IoT (Hive DB table)
                rows = fetch_and_save_iot_data(1)  # Replace 1 with actual hive_id if needed
                if not rows:  # If no rows found → fallback
                    logging.warning("[scheduler] No IoT data found. Using dummy data...")
                    fetch_and_save_dummy_data()
            except Exception as e:
                logging.error(f"[scheduler] IoT fetch failed → fallback to dummy. Error: {e}")
                fetch_and_save_dummy_data()

    # Schedule job every 30 seconds
    scheduler.add_job(scheduled_job, 'interval', seconds=30)

    scheduler.start()
    app.config['SCHEDULER'] = scheduler
