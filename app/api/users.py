from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..helper_json import json_request, json_response
from flask import current_app, request
from ..models import User, BlockedUser, Product

@api_bp.route('/users', methods=['GET'])
def get_user():
    filterName = request.args.get('name')
    result = User.get_filtered_by(name=filterName)
    # result = User.get(filterName)
    if result:
        data = User.to_dict(result)
        return json_response(data)
    else:
        current_app.logger.debug("User {} not found")
        return not_found("User not found")

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user_id(id):
    result = User.get(id)
    if result:
        data = User.to_dict(result)
        return json_response(data)
    else:
        current_app.logger.debug("User {} not found".format(id))
        return not_found("User not found")
    
@api_bp.route('/users/<int:id>/products', methods=['GET'])
def get_products_user(id):
    result = Product.get_all_filtered_by(seller_id=id)
    if result:
        (product) = result
        data = Product.to_dict_collection(product)
        return json_response(data)
    else:
        current_app.logger.debug("User {} not found".format(id))
        return not_found("User not found")
