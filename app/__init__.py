from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.database import mongo
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your-secret-key-here'   
    mongo.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app