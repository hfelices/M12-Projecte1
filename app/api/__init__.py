from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import  errors, statuses, categories, users, products, orders, tokens
