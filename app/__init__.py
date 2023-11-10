from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf.csrf import CSRFProtect
from .config import Config
from flask_login import LoginManager

db_manager = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

     # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    
    # csrf = CSRFProtect(app)
    # csrf.init_app(app)
    with app.app_context():
        from . import routes_main, routes_auth

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)  
        app.register_blueprint(routes_auth.auth_bp)
          
    app.logger.info("Aplicació iniciada")
    return app