from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import uuid

db = SQLAlchemy()
bcrypt = Bcrypt()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), unique=True, nullable=False)
    company_api_key = db.Column(db.String(150), unique=True, nullable=False, default=str(uuid.uuid4()))
    locations = db.relationship('Location', backref='company', lazy=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    location_name = db.Column(db.String(150), nullable=False)
    location_country = db.Column(db.String(150), nullable=False)
    location_city = db.Column(db.String(150), nullable=False)
    location_meta = db.Column(db.String(150), nullable=True)
    sensors = db.relationship('Sensor', backref='location', lazy=True)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    sensor_name = db.Column(db.String(150), nullable=False)
    sensor_category = db.Column(db.String(150), nullable=False)
    sensor_meta = db.Column(db.String(150), nullable=True)
    sensor_api_key = db.Column(db.String(150), unique=True, nullable=False, default=str(uuid.uuid4()))
    sensor_data = db.relationship('SensorData', backref='sensor', lazy=True)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    json_data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)