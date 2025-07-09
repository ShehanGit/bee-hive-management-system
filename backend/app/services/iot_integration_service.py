import requests
from app.services.sensor_service import create_sensor_data

# Update this to match your IoT device IP (or hostname)
IOT_DEVICE_URL = "http://192.168.45.63"


def fetch_and_save_iot_data(hive_id):
    """
    Fetch sensor data from the IoT device and save to the database.
    Returns True if all data is saved successfully, otherwise False.
    """
    try:
        # --- Temperature ---
        temperature_resp = requests.get(f"{IOT_DEVICE_URL}/temperature")
        temperature_resp.raise_for_status()
        temperature = temperature_resp.json().get("temperature")
        if temperature is not None:
            create_sensor_data(hive_id, "temperature", temperature)

        # --- Humidity ---
        humidity_resp = requests.get(f"{IOT_DEVICE_URL}/humidity")
        humidity_resp.raise_for_status()
        humidity = humidity_resp.json().get("humidity")
        if humidity is not None:
            create_sensor_data(hive_id, "humidity", humidity)

        # --- Light Sensor ---
        light_resp = requests.get(f"{IOT_DEVICE_URL}/light")
        light_resp.raise_for_status()
        light = light_resp.json().get("light")
        if light is not None:
            create_sensor_data(hive_id, "light", light)

        # --- GPS ---
        gps_resp = requests.get(f"{IOT_DEVICE_URL}/gps")
        gps_resp.raise_for_status()
        gps_data = gps_resp.json()
        # Save GPS data as two separate sensor records
        latitude = gps_data.get("latitude")
        longitude = gps_data.get("longitude")
        if latitude is not None:
            create_sensor_data(hive_id, "gps_lat", latitude)
        if longitude is not None:
            create_sensor_data(hive_id, "gps_lng", longitude)

        return True
    except Exception as e:
        print(f"Error fetching IoT data: {e}")
        return False
