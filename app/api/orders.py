from . import api_bp
from .errors import not_found, bad_request, forbidden_access
from .. import db_manager as db
from .helper_json import json_request, json_response 
from flask import current_app, request
from ..models import Order, User, ConfirmedOrder, Product
from .helper_auth import basic_auth, token_auth
from sqlalchemy import select
# Post new confirmed order
@api_bp.route('/orders/<int:id>/confirmed', methods=['POST'])
@token_auth.login_required
def accept_order(id):
   
    order = Order.get(id)
    if order:
        product = Product.get(order.product_id)

        confirmed_order = ConfirmedOrder.get(id)
        if basic_auth.current_user().id == product.seller_id  :
            if confirmed_order :
                confirmed_order = ConfirmedOrder.create(order_id=id)
                data = ConfirmedOrder.to_dict(confirmed_order)
                return json_response(data)
            else:
                return bad_request("Order already confirmed")
        else:
                return forbidden_access("You are not the owner of this product")
    else:
        return not_found("Item not found")
       

# Delete confirmed order
@api_bp.route('/orders/<int:id>/confirmed', methods=['DELETE'])
@token_auth.login_required
def delete_confirmed_order(id):

    order = Order.get(id)
    confirmed_order = ConfirmedOrder.get(id)
    if confirmed_order:

        product = Product.get(order.product_id)
        if basic_auth.current_user().id == product.seller_id :

            confirmed_order.delete()
            return json_response(order.to_dict())
        else:

            return forbidden_access("You are not the owner of this product")
    else:

        return not_found("Order not found")

@api_bp.route('/orders', methods=['POST'])
@token_auth.login_required #esto solo funciona en apis?
def create_order():

    data = json_request(['product_id', 'offer'])
    order = Order.get_all_filtered_by(product_id=data['product_id'],buyer_id=basic_auth.current_user().id)
    
    if not order:
        try:

            data['buyer_id'] = basic_auth.current_user().id
        except Exception as e:

            current_app.logger.debug(e)
            return bad_request(str(e))
        else:

            order = Order.create(**data)
            current_app.logger.debug("CREATED order: {}".format(order.to_dict()))
            return json_response(order.to_dict(), 201)
    else:

        return bad_request("Order already exists")

    
@api_bp.route('/orders/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_item(id):
    order = Order.get(id)
    
    if order:

        confirmed_order = ConfirmedOrder.get(id)
        if order.buyer_id == basic_auth.current_user().id:

            if confirmed_order:

                return bad_request("Order already confirmed")
            else:

                try:

                    data = json_request(['product_id','offer'], False)
                    data['buyer_id'] = order.buyer_id
                except Exception as e:

                    current_app.logger.debug(e)
                    return bad_request(str(e))
                else:

                    order.update(**data)
                    current_app.logger.debug("UPDATED order: {}".format(order.to_dict()))
                    return json_response(order.to_dict())
        else:

            return forbidden_access("You are not the buyer in this offer")
    else:

        current_app.logger.debug("Order {} not found".format(id))
        return not_found("Item not found")
    
@api_bp.route('/orders/<int:id>', methods=['DELETE'])
@token_auth.login_required 
def delete_item(id):

    order = Order.get(id)
    if order:

        confirmed_order = ConfirmedOrder.get(id)
        if order.buyer_id == basic_auth.current_user().id:

            if confirmed_order:

                return bad_request("Order already confirmed")
            else:

                order.delete()
                current_app.logger.debug("DELETED item: {}".format(id))
                return json_response(order.to_dict())
        else:

            return forbidden_access("You are not the owner of this product")
    else:

        current_app.logger.debug("Item {} not found".format(id))
        return not_found("Item not found")
