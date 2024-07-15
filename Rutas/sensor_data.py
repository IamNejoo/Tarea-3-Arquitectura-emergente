from flask import Blueprint, request, jsonify
from models import db, SensorData, Sensor, Company
from schemas import SensorDataSchema
from datetime import datetime

sensor_data_bp = Blueprint('sensor_data', __name__)
sensor_data_schema = SensorDataSchema()
sensor_datas_schema = SensorDataSchema(many=True)

def validate_sensor_api_key(api_key):
    sensor = Sensor.query.filter_by(sensor_api_key=api_key).first()
    if not sensor:
        return None
    return sensor

@sensor_data_bp.route('/api/v1/sensor_data', methods=['POST'])
def create_sensor_data():
    sensor_api_key = request.json.get('api_key')
    if not sensor_api_key:
        return jsonify({'error': 'API key is missing'}), 401

    sensor = validate_sensor_api_key(sensor_api_key)
    if not sensor:
        return jsonify({'error': 'Invalid API key'}), 401

    json_data = request.json['json_data']
    timestamp_str = request.json.get('timestamp')
    
    if timestamp_str:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    else:
        timestamp = datetime.utcnow()

    new_sensor_data = SensorData(sensor_id=sensor.id, json_data=json_data, timestamp=timestamp)
    db.session.add(new_sensor_data)
    db.session.commit()

    print(f'Inserted sensor data: {new_sensor_data}')

    return sensor_data_schema.jsonify(new_sensor_data), 201

@sensor_data_bp.route('/api/v1/sensor_data', methods=['GET'])
def get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    from_epoch = int(request.args.get('from'))
    to_epoch = int(request.args.get('to'))
    sensor_ids = request.args.getlist('sensor_id')
    
    # Limpiar y convertir los valores de sensor_id a enteros
    sensor_ids = [int(sensor_id.strip()) for sensor_id in sensor_ids]

    from_datetime = datetime.fromtimestamp(from_epoch)
    to_datetime = datetime.fromtimestamp(to_epoch)

    print(f'from_datetime: {from_datetime}, to_datetime: {to_datetime}, sensor_ids: {sensor_ids}')

    # Recuperar y mostrar todos los datos antes de aplicar el filtro para verificar los datos almacenados
    all_sensor_data = SensorData.query.all()
    print(f'Total sensor data in DB: {len(all_sensor_data)}')
    for data in all_sensor_data:
        print(f'SensorData ID: {data.id}, Timestamp: {data.timestamp}, Sensor ID: {data.sensor_id}, UNIX timestamp: {data.timestamp.timestamp()}')

    sensor_data = SensorData.query.filter(
        SensorData.sensor_id.in_(sensor_ids),
        SensorData.timestamp >= from_datetime,
        SensorData.timestamp <= to_datetime
    ).all()

    print(f'Found {len(sensor_data)} entries.')

    result = sensor_datas_schema.dump(sensor_data)
    return jsonify(result)
