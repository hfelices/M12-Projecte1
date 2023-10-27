from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf.csrf import CSRFProtect
from .config import Config

db_manager = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db_manager.init_app(app)
    
    # csrf = CSRFProtect(app)
    # csrf.init_app(app)
    with app.app_context():
        from . import routes_main

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)  
          
    app.logger.info("Aplicació iniciada")
    return app