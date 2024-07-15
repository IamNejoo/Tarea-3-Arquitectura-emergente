from flask import Blueprint, request, jsonify
from models import db, Location, Company
from schemas import LocationSchema

location_bp = Blueprint('location', __name__)
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

def validate_company_api_key(api_key):
    if not api_key:
        return jsonify({'error': 'API key is missing'}), 401

    company = Company.query.filter_by(company_api_key=api_key).first()
    if not company:
        return jsonify({'error': 'Invalid API key'}), 401

    return company

@location_bp.route('/api/v1/locations', methods=['POST'])
def create_location():
    data = request.json
    print('Request data:', data)  # Añadir este log para depuración
    api_key = data.get('company_api_key')
    company = validate_company_api_key(api_key)
    if isinstance(company, tuple):  # Si la validación falla, se devuelve el error
        return company

    company_id = company.id
    location_name = data['location_name']
    location_country = data['location_country']
    location_city = data['location_city']
    location_meta = data.get('location_meta', '')
    new_location = Location(company_id=company_id, location_name=location_name, location_country=location_country,
                            location_city=location_city, location_meta=location_meta)
    db.session.add(new_location)
    db.session.commit()
    return location_schema.jsonify(new_location), 201

@location_bp.route('/api/v1/locations', methods=['GET'])
def get_locations():
    all_locations = Location.query.all()
    result = locations_schema.dump(all_locations)
    return jsonify(result)

@location_bp.route('/api/v1/locations/<int:id>', methods=['GET'])
def get_location(id):
    location = Location.query.get_or_404(id)
    return location_schema.jsonify(location)

@location_bp.route('/api/v1/locations/<int:id>', methods=['PUT'])
def update_location(id):
    location = Location.query.get_or_404(id)
    location.location_name = request.json['location_name']
    location.location_country = request.json['location_country']
    location.location_city = request.json['location_city']
    location.location_meta = request.json.get('location_meta', location.location_meta)

    db.session.commit()
    return location_schema.jsonify(location)

@location_bp.route('/api/v1/locations/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    return '', 204
