from . import api_bp
from .errors import not_found, bad_request
from .. import db_manager as db
from ..models import Status
from .helper_json import json_request, json_response
from flask import current_app, request

# List
@api_bp.route('/statuses', methods=['GET'])
def get_statuses():
    statuses = Status.get_all()
    data = Status.to_dict_collection(statuses)
    return json_response(data)
