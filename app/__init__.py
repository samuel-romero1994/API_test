from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    api = Api(app, version='1.0', title='API de Items',
              description='Una simple API RESTful para gestionar items')
    
    from .routes import initialize_routes
    initialize_routes(api)
    
    with app.app_context():
        db.create_all()
    
    return app
