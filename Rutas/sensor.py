from flask import Blueprint, request, jsonify
from models import db, Sensor, Location, Company
from schemas import SensorSchema
import uuid

sensor_bp = Blueprint('sensor', __name__)
sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)

def validate_company_api_key(api_key):
    if not api_key:
        return jsonify({'error': 'API key is missing'}), 401

    company = Company.query.filter_by(company_api_key=api_key).first()
    if not company:
        return jsonify({'error': 'Invalid API key'}), 401

    return company

@sensor_bp.route('/api/v1/sensors', methods=['POST'])
def create_sensor():
    data = request.json
    api_key = data.get('company_api_key')
    company = validate_company_api_key(api_key)
    if isinstance(company, tuple):  # Si la validación falla, se devuelve el error
        return company

    location_id = data['location_id']
    sensor_name = data['sensor_name']
    sensor_category = data['sensor_category']
    sensor_meta = data.get('sensor_meta', '')
    sensor_api_key = str(uuid.uuid4())
    new_sensor = Sensor(location_id=location_id, sensor_name=sensor_name, sensor_category=sensor_category,
                        sensor_meta=sensor_meta, sensor_api_key=sensor_api_key)
    db.session.add(new_sensor)
    db.session.commit()
    return sensor_schema.jsonify(new_sensor), 201

@sensor_bp.route('/api/v1/sensors', methods=['GET'])
def get_sensors():
    all_sensors = Sensor.query.all()
    result = sensors_schema.dump(all_sensors)
    return jsonify(result)

@sensor_bp.route('/api/v1/sensors/<int:id>', methods=['GET'])
def get_sensor(id):
    sensor = Sensor.query.get_or_orkr(id)
    return sensor_schema.jsonify(sensor)

@sensor_bp.route('/api/v1/sensors/<int:id>', methods=['PUT'])
def update_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    sensor.sensor_name = request.json['sensor_name']
    sensor.sensor_category = request.json['sensor_category']
    sensor.sensor_meta = request.json.get('sensor_meta', sensor.sensor_meta)

    db.session.commit()
    return sensor_schema.jsonify(sensor)

@sensor_bp.route('/api/v1/sensors/<int:id>', methods=['DELETE'])
def delete_sensor(id):
    sensor = Sensor.query.get_or_404(id)
    db.session.delete(sensor)
    db.session.commit()
