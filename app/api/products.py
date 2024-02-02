from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Category , Product, Order
from ..helper_json import json_request, json_response
from flask import  request, current_app



# Get product filtered by title
@api_bp.route('/products', methods=['GET'])
def get_fitered_products():
    filterTitle = request.args.get('title')
    products = Product.query.filter(Product.title.ilike(f"%{filterTitle}%")).all()
    #products = Product.get_all_filtered_by(title=filterTitle)
    
    data = Product.to_dict_collection(products)
    return json_response(data)

# Get product by id
@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.get(id)
    data = Product.to_dict(product)
    return json_response(data)

# Update product
@api_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.get(id)
    data = json_request(['title','description', 'photo', 'price'],False)
    current_app.logger.debug(data)
    product.update(**data)
    return json_response(product.to_dict())


# Get ofers filtered by product id
@api_bp.route('/products/<int:id>/orders', methods=['GET'])
def get_fitered_orders(id):
    orders = Order.get_all_filtered_by(buyer_id=id)
    data = Order.to_dict_collection(orders)
    return json_response(data)
