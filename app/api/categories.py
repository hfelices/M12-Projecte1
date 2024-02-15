from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Category
from .helper_json import json_request, json_response
from flask import  request


@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.get_all()
    data = Category.to_dict_collection(categories)
    return json_response(data)

