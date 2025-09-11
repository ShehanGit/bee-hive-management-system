# app/controllers/potential_location_controller.py

from flask import Blueprint, request, jsonify
from app.services.potential_location_service import (
    get_all_potential_locations, get_potential_location_by_id,
    create_potential_location, update_potential_location, delete_potential_location
)
from math import radians, cos, sin, asin, sqrt  # For Haversine

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

# Similar routes for GET by ID, PUT, DELETE (follow pattern from hive_controller.py)

@potential_loc_blueprint.route('/potential-locations/generate-grid', methods=['GET'])
def generate_grid():
    """Manually generate and insert a sample grid of cells."""
    # Fixed resource locations (expand as needed; min distance to nearest)
    water_sources = [(6.9271, 79.8612)]  # Example lat/lng
    flowering_areas = [(6.9, 79.85)]
    feeding_stations = [(6.95, 79.87)]

    # Grid: 5x5 around Colombo, step 0.01 deg (~1km)
    lats = [6.90 + i * 0.01 for i in range(5)]
    lngs = [79.85 + j * 0.01 for j in range(5)]

    # Sample averages (replace with real data or API fetches in production)
    avg_temp = 28.0
    avg_humidity = 75.0
    avg_sunlight = 7.5  # hours/day
    avg_wind = 4.0  # km/h

    inserted_count = 0
    for lat in lats:
        for lng in lngs:
            dist_water = min(haversine_distance(lat, lng, ws[0], ws[1]) for ws in water_sources)
            dist_flower = min(haversine_distance(lat, lng, fa[0], fa[1]) for fa in flowering_areas)
            dist_feed = min(haversine_distance(lat, lng, fs[0], fs[1]) for fs in feeding_stations)

            data = {
                'lat': lat,
                'lng': lng,
                'temperature': avg_temp,
                'humidity': avg_humidity,
                'sunlight_exposure': avg_sunlight,
                'wind_speed': avg_wind,
                'dist_to_water_source': dist_water,
                'dist_to_flowering_area': dist_flower,
                'dist_to_feeding_station': dist_feed
            }
            create_potential_location(data)
            inserted_count += 1

    return jsonify({"message": f"Inserted {inserted_count} grid cells manually"}), 200