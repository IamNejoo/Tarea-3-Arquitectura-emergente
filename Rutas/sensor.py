from flask import Blueprint, request, jsonify
from models import db, Sensor
from schemas import SensorSchema
import uuid

sensor_bp = Blueprint('sensor', __name__)
sensor_schema = SensorSchema()
sensors_schema = SensorSchema(many=True)

@sensor_bp.route('/api/v1/sensors', methods=['POST'])
def create_sensor():
    location_id = request.json['location_id']
    sensor_name = request.json['sensor_name']
    sensor_category = request.json['sensor_category']
    sensor_meta = request.json.get('sensor_meta', '')
    sensor_api_key = str(uuid.uuid4())
    new_sensor = Sensor(location_id=location_id, sensor_name=sensor_name, sensor_category=sensor_category,
                        sensor_meta=sensor_meta, sensor_api_key=sensor_api_key)
    db.session.add(new_sensor)
    db.session.commit()
    return sensor_schema.jsonify(new_sensor)

@sensor_bp.route('/api/v1/sensors', methods=['GET'])
def get_sensors():
    all_sensors = Sensor.query.all()
    result = sensors_schema.dump(all_sensors)
    return jsonify(result)
