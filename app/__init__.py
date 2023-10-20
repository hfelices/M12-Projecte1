from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_manager = SQLAlchemy()
DATABASE = 'database.db'
UPLOAD_FOLDER = './static/uploads'

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__)) 

    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/" + DATABASE
    app.config["SQLALCHEMY_ECHO"] = True

    db_manager.init_app(app)

    with app.app_context():
        from . import routes_main

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)  
          
    app.logger.info("Aplicació iniciada")
    return app