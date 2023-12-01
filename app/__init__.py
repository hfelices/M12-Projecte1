from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf.csrf import CSRFProtect
from .config import Config
from flask_login import LoginManager
from flask_principal import Principal
from .helper_mail import MailManager
from werkzeug.local import LocalProxy
from flask import current_app
from flask_debugtoolbar import DebugToolbarExtension


db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager =  Principal()
mail_manager = MailManager()
logger = LocalProxy(lambda: current_app.logger)
toolbar = DebugToolbarExtension()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
     # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    mail_manager.init_app(app)
    toolbar.init_app(app)
    
    # csrf = CSRFProtect(app)
    # csrf.init_app(app)
    with app.app_context():
        from . import routes_main, routes_auth, routes_admin

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)  
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
          
    app.logger.info("Aplicación iniciada")
    return app