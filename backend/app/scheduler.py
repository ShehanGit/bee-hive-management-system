from apscheduler.schedulers.background import BackgroundScheduler
from app.services.iot_integration_service import fetch_and_save_iot_data

def start_scheduler(app):
    scheduler = BackgroundScheduler(timezone="UTC")
    
    # Define a wrapper function that pushes the app context
    def scheduled_job():
        with app.app_context():
            fetch_and_save_iot_data(1)  # Replace 1 with appropriate hive_id if needed

    # Schedule the job to run every 0.5 minute
    # scheduler.add_job(scheduled_job, 'interval', minutes=0.5)
    
    scheduler.start()
    
    # Optionally, store the scheduler in app config for reference
    app.config['SCHEDULER'] = scheduler
