from flask_marshmallow import Marshmallow
from models import Admin, Company, Location, Sensor, SensorData

ma = Marshmallow()

class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin

class CompanySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Company

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location

class SensorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sensor

class SensorDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SensorData
