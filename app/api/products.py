from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Category , Product
from ..helper_json import json_request, json_response
from flask import  request


@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.get(id)
    data = Product.to_dict(product)
    return json_response(data)

