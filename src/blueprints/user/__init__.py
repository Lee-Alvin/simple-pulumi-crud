from flask import Blueprint, request
from dynamo_util import create_user, get_user, update_user, delete_user, index_query

blueprint = Blueprint('api', __name__, url_prefix='/simple-crud-api')

@blueprint.route('/user', methods=['POST', 'GET', 'DELETE', 'PUT'])
def user():
    match request.method:
        case 'GET':
            return get_user(request.json)
        case 'POST':
            return create_user(request.json)
        case 'DELETE':
            return delete_user(request.json)
        case 'PUT':
            return update_user(request.json)

@blueprint.route('/user/index', methods=['GET'])
def index():
    return index_query(request.json)