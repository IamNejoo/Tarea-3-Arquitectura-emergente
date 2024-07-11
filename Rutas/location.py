from flask import Blueprint, request, jsonify
from models import db, Location
from schemas import LocationSchema

location_bp = Blueprint('location', __name__)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

@location_bp.route('/api/v1/locations', methods=['POST'])
def create_location():
    company_id = request.json['company_id']
    location_name = request.json['location_name']
    location_country = request.json['location_country']
    location_city = request.json['location_city']
    location_meta = request.json.get('location_meta', '')
    new_location = Location(company_id=company_id, location_name=location_name, location_country=location_country,
                            location_city=location_city, location_meta=location_meta)
    db.session.add(new_location)
    db.session.commit()
    return location_schema.jsonify(new_location)

@location_bp.route('/api/v1/locations', methods=['GET'])
def get_locations():
    all_locations = Location.query.all()
    result = locations_schema.dump(all_locations)
    return jsonify(result)
