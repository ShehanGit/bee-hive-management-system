import requests
import logging
from app.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use centralized configuration
ADAFRUIT_USERNAME = Config.ADAFRUIT_USERNAME
ADAFRUIT_KEY = Config.ADAFRUIT_KEY
BASE_URL = Config.ADAFRUIT_BASE_URL

HEADERS = {"X-AIO-Key": ADAFRUIT_KEY}

# Define feed names with hyphens
FEED_NAMES = {
    'weight': 'hive-1-weight',
    'temperature': 'hive-1-temperature',
    'humidity': 'hive-1-humidity',
    'heatindex': 'hive-1-heatindex',
    'sound': 'hive-1-sound',
    'status': 'hive-1-status'
}

def get_feed_data(metric):
    """Fetch the latest value from an Adafruit feed"""
    feed_name = FEED_NAMES.get(metric)
    if not feed_name:
        logger.error(f"Unknown metric: {metric}")
        return None
        
    try:
        # Get the feed's latest data
        data_url = f"{BASE_URL}/{feed_name}/data?limit=1"
        data_response = requests.get(data_url, headers=HEADERS)
        
        if data_response.status_code == 404:
            logger.error(f"Feed '{feed_name}' not found. Please check if the feed name is correct.")
            return None
        elif data_response.status_code != 200:
            logger.error(f"Error accessing feed '{feed_name}': {data_response.status_code} - {data_response.text}")
            return None
            
        data = data_response.json()
        if data:
            logger.info(f"Successfully retrieved data for feed '{feed_name}': {data[0]['value']}")
            return data[0]['value']
        else:
            logger.warning(f"No data available for feed '{feed_name}'")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while accessing feed '{feed_name}': {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while accessing feed '{feed_name}': {str(e)}")
        return None
    try:
        # First, get the feed information
        feed_url = f"{BASE_URL}/{feed_name}"
        feed_response = requests.get(feed_url, headers=HEADERS)
        
        if feed_response.status_code == 404:
            logger.error(f"Feed '{feed_name}' not found. Please check if the feed name is correct.")
            return None
        elif feed_response.status_code != 200:
            logger.error(f"Error accessing feed '{feed_name}': {feed_response.status_code} - {feed_response.text}")
            return None
            
        # If feed exists, get its latest data
        data_url = f"{feed_url}/data?limit=1"
        data_response = requests.get(data_url, headers=HEADERS)
        
        if data_response.status_code == 200:
            data = data_response.json()
            if data:
                logger.info(f"Successfully retrieved data for feed '{feed_name}': {data[0]['value']}")
                return data[0]["value"]
            else:
                logger.warning(f"No data available for feed '{feed_name}'")
                return None
        else:
            logger.error(f"Error getting data for feed '{feed_name}': {data_response.status_code} - {data_response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while accessing feed '{feed_name}': {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while accessing feed '{feed_name}': {str(e)}")
        return None
