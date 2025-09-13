# app/services/potential_location_service.py

from app import db
from app.models.potential_location import PotentialLocation

def get_all_potential_locations():
    """Fetch all potential location records."""
    return PotentialLocation.query.all()

def get_potential_location_by_id(loc_id):
    """Fetch a single potential location by ID."""
    return PotentialLocation.query.get(loc_id)

def create_potential_location(data):
    """Create a new potential location record."""
    loc = PotentialLocation(
        lat=data['lat'],
        lng=data['lng'],
        temperature=data['temperature'],
        humidity=data['humidity'],
        sunlight_exposure=data['sunlight_exposure'],
        wind_speed=data['wind_speed'],
        dist_to_water_source=data['dist_to_water_source'],
        dist_to_flowering_area=data['dist_to_flowering_area'],
        dist_to_feeding_station=data['dist_to_feeding_station'],
        honey_production=data.get('honey_production')  # Optional
    )
    db.session.add(loc)
    db.session.commit()
    return loc

def update_potential_location(loc_id, data):
    """Update an existing potential location record (e.g., to set honey_production)."""
    loc = get_potential_location_by_id(loc_id)
    if not loc:
        return None
    for key, value in data.items():
        setattr(loc, key, value)
    db.session.commit()
    return loc

def delete_potential_location(loc_id):
    """Delete a potential location record."""
    loc = get_potential_location_by_id(loc_id)
    if not loc:
        return None
    db.session.delete(loc)
    db.session.commit()
    return loc