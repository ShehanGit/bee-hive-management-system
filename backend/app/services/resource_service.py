# app/services/resource_service.py

from app import db
from app.models.resource import Resource

def get_all_resources():
    """Fetch all resource records."""
    return Resource.query.all()

def get_resource_by_id(res_id):
    """Fetch a single resource by ID."""
    return Resource.query.get(res_id)

def create_resource(data):
    """Create a new resource record."""
    res = Resource(
        type=data['type'],
        lat=data['lat'],
        lng=data['lng']
    )
    db.session.add(res)
    db.session.commit()
    return res

def update_resource(res_id, data):
    """Update an existing resource record."""
    res = get_resource_by_id(res_id)
    if not res:
        return None
    for key, value in data.items():
        setattr(res, key, value)
    db.session.commit()
    return res

def delete_resource(res_id):
    """Delete a resource record."""
    res = get_resource_by_id(res_id)
    if not res:
        return None
    db.session.delete(res)
    db.session.commit()
    return res