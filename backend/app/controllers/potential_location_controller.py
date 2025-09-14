# app/controllers/potential_location_controller.py (updated for weather and resources)

from flask import Blueprint, request, jsonify
from app.services.potential_location_service import (
    get_all_potential_locations, get_potential_location_by_id,
    create_potential_location, update_potential_location, delete_potential_location
)
from app.services.resource_service import get_all_resources  # New import
from flask import current_app  # Corrected import
import requests  # For API calls
from math import radians, cos, sin, asin, sqrt

potential_loc_blueprint = Blueprint('potential_loc_blueprint', __name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    """Haversine formula for distance calculation."""
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

@potential_loc_blueprint.route('/potential-locations', methods=['GET'])
def get_potential_locations():
    locs = get_all_potential_locations()
    results = [{
        'id': loc.id,
        'lat': loc.lat,
        'lng': loc.lng,
        'temperature': loc.temperature,
        'humidity': loc.humidity,
        'sunlight_exposure': loc.sunlight_exposure,
        'wind_speed': loc.wind_speed,
        'dist_to_water_source': loc.dist_to_water_source,
        'dist_to_flowering_area': loc.dist_to_flowering_area,
        'dist_to_feeding_station': loc.dist_to_feeding_station,
        'honey_production': loc.honey_production,
        'created_at': loc.created_at
    } for loc in locs]
    return jsonify(results), 200

@potential_loc_blueprint.route('/potential-locations', methods=['POST'])
def add_potential_location():
    data = request.get_json()
    required_fields = ['lat', 'lng', 'temperature', 'humidity', 'sunlight_exposure',
                       'wind_speed', 'dist_to_water_source', 'dist_to_flowering_area', 'dist_to_feeding_station']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    loc = create_potential_location(data)
    return jsonify({"message": "Potential location created", "id": loc.id}), 201

# ... (keep other routes like GET/PUT/DELETE by ID)

@potential_loc_blueprint.route('/potential-locations/generate-grid', methods=['GET'])
def generate_grid():
    """Manually generate and insert a sample grid of cells with real weather data."""
    # Fetch resources from DB
    water_sources = [(r.lat, r.lng) for r in get_all_resources() if r.type == 'water']
    flowering_areas = [(r.lat, r.lng) for r in get_all_resources() if r.type == 'flowering']
    feeding_stations = [(r.lat, r.lng) for r in get_all_resources() if r.type == 'feeding']

    # If no resources, use defaults
    if not water_sources:
        water_sources = [(6.9271, 79.8612)]
    if not flowering_areas:
        flowering_areas = [(6.9, 79.85)]
    if not feeding_stations:
        feeding_stations = [(6.95, 79.87)]

    # Grid: 10x10 around Colombo, step 0.005 deg (~500m)
    step_size = 0.005
    grid_size = 10
    center_lat, center_lng = 6.9271, 79.8612
    lats = [center_lat - (grid_size // 2) * step_size + i * step_size for i in range(grid_size)]
    lngs = [center_lng - (grid_size // 2) * step_size + i * step_size for i in range(grid_size)]

    # Fetch weather data from OpenWeather One Call API (once for center, apply to all)
    api_key = current_app.config.get('OPENWEATHER_API_KEY')
    if not api_key:
        return jsonify({"error": "OpenWeather API key not configured"}), 500

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={center_lat}&lon={center_lng}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data", "details": response.text}), 500

    data = response.json()
    current = data['current']
    daily = data['daily'][0]  # Today's forecast

    temperature = current['temp']
    humidity = current['humidity']
    wind_speed = current['wind_speed']
    clouds = current['clouds']
    sunrise = daily['sunrise']
    sunset = daily['sunset']
    daylight_hours = (sunset - sunrise) / 3600.0
    sunlight_exposure = daylight_hours * (1 - clouds / 100.0)

    inserted_count = 0
    for lat in lats:
        for lng in lngs:
            # Calculate min distances
            dist_water = min(haversine_distance(lat, lng, ws[0], ws[1]) for ws in water_sources)
            dist_flower = min(haversine_distance(lat, lng, fa[0], fa[1]) for fa in flowering_areas)
            dist_feed = min(haversine_distance(lat, lng, fs[0], fs[1]) for fs in feeding_stations)

            data = {
                'lat': round(lat, 6),
                'lng': round(lng, 6),
                'temperature': temperature,
                'humidity': humidity,
                'sunlight_exposure': sunlight_exposure,
                'wind_speed': wind_speed,
                'dist_to_water_source': dist_water,
                'dist_to_flowering_area': dist_flower,
                'dist_to_feeding_station': dist_feed
            }
            create_potential_location(data)
            inserted_count += 1

    return jsonify({"message": f"Inserted {inserted_count} grid cells with real weather data"}), 200


@potential_loc_blueprint.route('/potential-locations/recalculate-distances', methods=['GET'])
def recalculate_distances():
    """Recalculate distances for all potential locations based on current resources."""
    # Fetch resources from DB
    water_sources = [(r.lat, r.lng) for r in get_all_resources() if r.type == 'water']
    flowering_areas = [(r.lat, r.lng) for r in get_all_resources() if r.type == 'flowering']
    feeding_stations = [(r.lat, r.lng) for r in get_all_resources() if r.type == 'feeding']

    # If no resources, use defaults
    if not water_sources:
        water_sources = [(6.9271, 79.8612)]
    if not flowering_areas:
        flowering_areas = [(6.9, 79.85)]
    if not feeding_stations:
        feeding_stations = [(6.95, 79.87)]

    locs = get_all_potential_locations()
    updated_count = 0
    for loc in locs:
        dist_water = min(haversine_distance(loc.lat, loc.lng, ws[0], ws[1]) for ws in water_sources)
        dist_flower = min(haversine_distance(loc.lat, loc.lng, fa[0], fa[1]) for fa in flowering_areas)
        dist_feed = min(haversine_distance(loc.lat, loc.lng, fs[0], fs[1]) for fs in feeding_stations)

        update_data = {
            'dist_to_water_source': dist_water,
            'dist_to_flowering_area': dist_flower,
            'dist_to_feeding_station': dist_feed
        }
        update_potential_location(loc.id, update_data)
        updated_count += 1

    return jsonify({"message": f"Updated distances for {updated_count} locations"}), 200