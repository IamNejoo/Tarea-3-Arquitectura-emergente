from flask import Flask
from config import Config
from models import db, bcrypt
from schemas import ma
from Rutas.company import company_bp
from Rutas.location import location_bp
from Rutas.sensor import sensor_bp
from Rutas.sensor_data import sensor_data_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(company_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(sensor_bp)
    app.register_blueprint(sensor_data_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
