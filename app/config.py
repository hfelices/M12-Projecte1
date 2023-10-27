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


    # DATABASE
    DATABASE = environ.get("DATABASE")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(os.path.dirname(__file__))  + "/" + DATABASE
    SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")
