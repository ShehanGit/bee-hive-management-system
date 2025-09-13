# 


# app/services/hive_service.py

from app import db
from app.models.hive import Hive

def get_all_hives():
    """Fetch all hives from the database."""
    return Hive.query.all()

def get_hive_by_id(hive_id):
    """Fetch a single hive by its ID."""
    return Hive.query.get(hive_id)

def create_hive(name, location_lat, location_lng):
    """Create a new hive and save it to the database."""
    new_hive = Hive(name=name, location_lat=location_lat, location_lng=location_lng)
    db.session.add(new_hive)
    db.session.commit()
    return new_hive

def update_hive(hive_id, name=None, location_lat=None, location_lng=None):
    """Update an existing hive's details."""
    hive = get_hive_by_id(hive_id)
    if not hive:
        return None
    
    if name:
        hive.name = name
    if location_lat:
        hive.location_lat = location_lat
    if location_lng:
        hive.location_lng = location_lng
    
    db.session.commit()
    return hive

def delete_hive(hive_id):
    """Delete a hive from the database."""
    hive = get_hive_by_id(hive_id)
    if not hive:
        return None
    
    db.session.delete(hive)
    db.session.commit()
    return hive
