from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Category , Product, Order, ConfirmedOrder
from ..helper_json import json_request, json_response
from flask import  request, current_app


# Post new confirmed order
@api_bp.route('/orders/<int:id>/confirmed', methods=['POST'])
def accept_order(id):
   
    order = Order.get(id)
    if order:
        confirmed_order = ConfirmedOrder.create(order_id=id)
        data = ConfirmedOrder.to_dict(confirmed_order)
        return json_response(data)
    else:
        return not_found("Item not found")
       

# Delete confirmed order
@api_bp.route('/orders/<int:id>/confirmed', methods=['DELETE'])
def delete_confirmed_order(id):
    order = ConfirmedOrder.get(id)
    if order:
        order.delete()
        return json_response(order.to_dict())
    else:
        return not_found("Order not found")