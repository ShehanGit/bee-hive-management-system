# from apscheduler.schedulers.background import BackgroundScheduler
# from app.services.iot_integration_service import fetch_and_save_iot_data

# def start_scheduler(app):
#     scheduler = BackgroundScheduler(timezone="UTC")
    
#     # Define a wrapper function that pushes the app context
#     def scheduled_job():
#         with app.app_context():
#             fetch_and_save_iot_data(1)  # Replace 1 with appropriate hive_id if needed

#     # Schedule the job to run every 0.5 minute
#     scheduler.add_job(scheduled_job, 'interval', minutes=0.5)
    
#     scheduler.start()
    
#     # Optionally, store the scheduler in app config for reference
#     app.config['SCHEDULER'] = scheduler


# IT21807862 - Malinda

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.iot_integration_service import fetch_and_save_iot_data
from app.services.weather_service import weather_service
from app.services.synchronized_monitoring_service import synchronized_monitoring_service
from app.services.real_time_threat_detection_service import real_time_threat_detection_service
from app.utils.adafruit_client import get_feed_data
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_scheduler(app, socketio):
    scheduler = BackgroundScheduler(timezone="UTC")
    
    def monitor_hive():
        """Function to fetch and emit real-time hive data"""
        try:
            hive_id = 1  # For now, monitoring only one hive
            hive_data = {
                "hive_id": hive_id,
                "timestamp": datetime.now().isoformat(),
                "weight": get_feed_data("weight"),
                "temperature": get_feed_data("temperature"),
                "humidity": get_feed_data("humidity"),
                "heatindex": get_feed_data("heatindex"),
                "sound": get_feed_data("sound"),
                "status": get_feed_data("status")
            }
            
            if any(hive_data.values()):  # Only emit if we got some data
                logger.info(f"Emitting hive data update: {hive_data}")
                socketio.emit("hive_update", hive_data)
            else:
                logger.warning("No hive data received from Adafruit IO")
                
        except Exception as e:
            logger.error(f"Error in monitor_hive: {str(e)}")
    
    def synchronized_collection_job():
        """Function to collect synchronized weather and sensor data"""
        with app.app_context():
            try:
                logger.info("Starting synchronized data collection...")
                result = synchronized_monitoring_service.collect_synchronized_data(1)
                
                if result['success']:
                    logger.info(f"Synchronized data collection completed successfully")
                    logger.info(f"Collected {len(result['sensor_data'])} sensor readings")
                    
                    # Emit real-time update with synchronized data
                    synchronized_update = {
                        "hive_id": result['hive_id'],
                        "timestamp": result['collection_timestamp'],
                        "weather": result['weather_data'],
                        "sensors": result['sensor_data'],
                        "api_usage": result['api_usage']
                    }
                    socketio.emit("synchronized_update", synchronized_update)
                    
                    # Process real-time threat detection
                    threat_result = real_time_threat_detection_service.process_latest_data(1)
                    
                    if threat_result.get('success'):
                        logger.info(f"Threat detection completed: {threat_result['prediction']['threat_type']}")
                        
                        # Emit threat detection update
                        threat_update = {
                            "hive_id": threat_result['hive_id'],
                            "timestamp": threat_result['timestamp'],
                            "prediction": threat_result['prediction'],
                            "threat_trend": threat_result['threat_trend'],
                            "alert_generated": threat_result['alert_generated'],
                            "alert_data": threat_result['alert_data']
                        }
                        socketio.emit("threat_detection_update", threat_update)
                        
                        # If alert was generated, emit alert notification
                        if threat_result['alert_generated'] and threat_result['alert_data']:
                            alert_notification = {
                                "type": "threat_alert",
                                "hive_id": threat_result['hive_id'],
                                "threat_type": threat_result['prediction']['threat_type'],
                                "probability": threat_result['prediction']['probability'],
                                "timestamp": threat_result['timestamp'],
                                "alert_data": threat_result['alert_data']
                            }
                            socketio.emit("threat_alert", alert_notification)
                            logger.warning(f"🚨 THREAT ALERT EMITTED: {threat_result['prediction']['threat_type']}")
                    
                else:
                    logger.warning(f"Synchronized data collection failed: {result['errors']}")
                    
            except Exception as e:
                logger.error(f"Error in synchronized collection job: {str(e)}")


    def scheduled_weather_job():
        """Function to fetch and save weather data (legacy - kept for backward compatibility)"""
        with app.app_context():
            try:
                logger.info("Starting legacy weather data collection...")
                success = weather_service.fetch_and_save_weather()
                if success:
                    logger.info("Legacy weather data collection completed successfully")
                else:
                    logger.warning("Legacy weather data collection failed")
            except Exception as e:
                logger.error(f"Error in legacy weather scheduled job: {str(e)}")

    def scheduled_job():
        """Wrapper function that handles both data saving and real-time updates (legacy)"""
        with app.app_context():
            try:
                # First save the data to database
                fetch_and_save_iot_data(1)
                # Then emit real-time update
                monitor_hive()
            except Exception as e:
                logger.error(f"Error in legacy scheduled job: {str(e)}")

    # NEW: Schedule synchronized collection every 1 minute
    scheduler.add_job(synchronized_collection_job, 'interval', minutes=1)
    
    # LEGACY: Keep old schedulers for backward compatibility (can be removed later)
    # scheduler.add_job(scheduled_job, 'interval', seconds=30)
    # scheduler.add_job(scheduled_weather_job, 'interval', minutes=30)
    
    logger.info("Starting scheduler with 1-minute synchronized collection intervals")

    
    scheduler.start()
    
    # Store the scheduler in app config for reference
    app.config['SCHEDULER'] = scheduler
