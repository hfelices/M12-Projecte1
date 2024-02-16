import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
class Config:

    #GENERAL CONFIG
    SECRET_KEY = environ.get("SECRET_KEY")
    ALLOWED_EXTENSIONS = environ.get("ALLOWED_EXTENSIONS")
    UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER")
    DEBUG = environ.get('DEBUG', True)
    #MAIL CONFIG

    MAIL_SENDER_NAME = environ.get('MAIL_SENDER_NAME')
    MAIL_SENDER_ADDR = environ.get('MAIL_SENDER_ADDR')
    MAIL_SENDER_PASSWORD = environ.get('MAIL_SENDER_PASSWORD')
    MAIL_SMTP_SERVER = environ.get('MAIL_SMTP_SERVER')
    MAIL_SMTP_PORT = int(environ.get('MAIL_SMTP_PORT'))

    # DATABASE
    DATABASE = environ.get("DATABASE")
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    if (SQLALCHEMY_DATABASE_URI is None or SQLALCHEMY_DATABASE_URI == ""):
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(os.path.dirname(__file__))  + "/" + DATABASE
    SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")

    # LOGGING
    # environ.get('LOG_LEVEL', 'DEBUG').upper()
    LOG_LEVEL = 'DEBUG'
            
        