import os


DATABASE = 'database.db'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath(os.path.dirname(__file__))  + "/" + DATABASE
SQLALCHEMY_ECHO = True
SECRET_KEY = "1234"


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/uploads'



