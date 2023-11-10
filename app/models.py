from . import db_manager as db
from datetime import datetime
from flask_login import UserMixin
def now():
    return datetime.now()

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.Text)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DATETIME, default=now(), nullable=False)
    updated = db.Column(db.DATETIME, default=now(), onupdate=now(), nullable=False)

    category = db.relationship('Category', backref='products')
    seller = db.relationship('User', backref='products')

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    slug = db.Column(db.Text, unique=True, nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default='wanner')
    created = db.Column(db.DATETIME, default=now(), nullable=False)
    updated = db.Column(db.DATETIME, default=now(), onupdate=now(), nullable=False)

    def get_id(self):
        return self.name
