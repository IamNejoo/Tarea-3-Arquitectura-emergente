from flask import Blueprint, request, jsonify
from models import db, SensorData, Sensor
from schemas import SensorDataSchema
from datetime import datetime

sensor_data_bp = Blueprint('sensor_data', __name__)
sensor_data_schema = SensorDataSchema()
sensor_datas_schema = SensorDataSchema(many=True)

@sensor_data_bp.route('/api/v1/sensor_data', methods=['POST'])
def create_sensor_data():
    sensor_api_key = request.json['api_key']
    sensor = Sensor.query.filter_by(sensor_api_key=sensor_api_key).first()

    if not sensor:
        return jsonify({'error': 'Invalid sensor API key'}), 400

    json_data = request.json['json_data']
    timestamp = datetime.utcnow()

    new_sensor_data = SensorData(sensor_id=sensor.id, json_data=json_data, timestamp=timestamp)
    db.session.add(new_sensor_data)
    db.session.commit()

    return sensor_data_schema.jsonify(new_sensor_data), 201

@sensor_data_bp.route('/api/v1/sensor_data', methods=['GET'])
def get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    from_epoch = int(request.args.get('from'))
    to_epoch = int(request.args.get('to'))
    sensor_ids = request.args.getlist('sensor_id')

    from_datetime = datetime.fromtimestamp(from_epoch)
    to_datetime = datetime.fromtimestamp(to_epoch)

    sensor_data = SensorData.query.filter(
        SensorData.sensor_id.in_(sensor_ids),
        SensorData.timestamp >= from_datetime,
        SensorData.timestamp <= to_datetime
    ).all()

    result = sensor_datas_schema.dump(sensor_data)
    return jsonify(result)
