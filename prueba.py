import requests
import json
import time
import random

# URL base de la API
BASE_URL = 'https://murmuring-gorge-54693-5163040c3e89.herokuapp.com/api/v1'

# Función para crear una compañía
def create_company(company_name):
    url = f'{BASE_URL}/companies'
    payload = {
        'company_name': company_name
    }
    response = requests.post(url, json=payload)
    return response

# Función para crear una ubicación
def create_location(company_api_key, location_name, location_country, location_city, location_meta):
    url = f'{BASE_URL}/locations'
    payload = {
        'company_api_key': company_api_key,
        'location_name': location_name,
        'location_country': location_country,
        'location_city': location_city,
        'location_meta': location_meta
    }
    print('Payload enviado:', payload)
    response = requests.post(url, json=payload)
    return response

# Función para crear un sensor
def create_sensor(company_api_key, location_id, sensor_name, sensor_category, sensor_meta):
    url = f'{BASE_URL}/sensors'
    payload = {
        'company_api_key': company_api_key,
        'location_id': location_id,
        'sensor_name': sensor_name,
        'sensor_category': sensor_category,
        'sensor_meta': sensor_meta
    }
    print('Payload enviado:', payload)
    response = requests.post(url, json=payload)
    return response

# Función para insertar datos del sensor
def insert_sensor_data(sensor_api_key, json_data):
    url = f'{BASE_URL}/sensor_data'
    payload = {
        'api_key': sensor_api_key,
        'json_data': json_data
    }
    print('Payload enviado:', payload)
    response = requests.post(url, json=payload)
    return response

# Función para generar datos aleatorios para el sensor
def generate_sensor_data():
    temperature = round(random.uniform(15.0, 30.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)
    return [{'temperature': temperature, 'humidity': humidity}]

# Flujo principal
def main():
    timestamp = int(time.time())
    unique_suffix = f'_{timestamp}'

    # Crear una compañía
    company_name = f'Test Company{unique_suffix}'
    company_response = create_company(company_name)
    if company_response.status_code != 201:
        print('Error al crear la compañía:', company_response.json())
        return
    
    company_data = company_response.json()
    company_api_key = company_data.get('company_api_key')
    if not company_api_key:
        print('Error: company_api_key no está en la respuesta:', company_data)
        return

    print('Compañía creada:', company_data)

    # Crear una ubicación
    location_name = f'Test Location{unique_suffix}'
    location_response = create_location(company_api_key, location_name, 'Country', 'City', 'Meta data')
    if location_response.status_code != 201:
        print('Error al crear la ubicación:', location_response.json())
        return
    
    location_data = location_response.json()
    location_id = location_data.get('id')
    if not location_id:
        print('Error: id de ubicación no está en la respuesta:', location_data)
        return

    print('Ubicación creada:', location_data)

    # Crear un sensor
    sensor_name = f'Test Sensor{unique_suffix}'
    sensor_response = create_sensor(company_api_key, location_id, sensor_name, 'Category', 'Meta data')
    if sensor_response.status_code != 201:
        print('Error al crear el sensor:', sensor_response.json())
        return
    
    sensor_data = sensor_response.json()
    sensor_api_key = sensor_data.get('sensor_api_key')
    if not sensor_api_key:
        print('Error: sensor_api_key no está en la respuesta:', sensor_data)
        return

    print('Sensor creado:', sensor_data)

    # Enviar datos al sensor cada 1 a 30 segundos
    try:
        while True:
            sensor_data_payload = generate_sensor_data()
            sensor_data_response = insert_sensor_data(sensor_api_key, sensor_data_payload)
            if sensor_data_response.status_code != 201:
                print('Error al insertar datos del sensor:', sensor_data_response.json())
                continue
            print('Datos del sensor insertados:', sensor_data_response.json())

            # Esperar entre 1 y 30 segundos antes de enviar el próximo dato
            interval = random.randint(1, 30)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Proceso detenido manualmente.")

if __name__ == '__main__':
    main()
