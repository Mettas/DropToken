from flask import jsonify, Blueprint, request
from ..lib import game_service as service
from ..lib.exception import MalformedRequestException


drop_token_bp = Blueprint('drop_token', __name__, url_prefix='/drop_token')


# Ideally we're using a library to help parse out parameters.
# Also one that makes it easy to document the apis (like Swagger)
# I wanted to keep the dependecies to a minimum to prevent build issues


@drop_token_bp.route('', methods=['GET'])
def get_all_in_progress_games():
    return jsonify(service.get_all_in_progress_games())


@drop_token_bp.route('', methods=['POST'])
def create_new_game():
    data = request.get_json(force=True)

    players = _get_list_param('players', data)
    columns = _get_int_param('columns', data)
    rows = _get_int_param('rows', data)
    return jsonify(service.create_new_game(players, columns, rows))


@drop_token_bp.route('/<game_id>', methods=['GET'])
def get_game_state(game_id):
    return jsonify(service.get_game_state(game_id))


@drop_token_bp.route('/<game_id>/moves', methods=['GET'])
def get_game_moves(game_id):
    data = request.args.to_dict()

    start = _get_int_param('start', data, required=False)
    until = _get_int_param('until', data, required=False)
    return jsonify(service.get_game_moves(game_id, start=start, end=until))


@drop_token_bp.route('/<game_id>/<player>', methods=['POST'])
def make_move(game_id, player):
    data = request.get_json(force=True)

    column = _get_int_param('column', data)
    return jsonify(service.make_move(game_id, player, column))


@drop_token_bp.route('/<game_id>/moves/<int:move_number>', methods=['GET'])
def get_move(game_id, move_number):
    return jsonify(service.get_move(game_id, move_number))


@drop_token_bp.route('/<game_id>/<player>', methods=['DELETE'])
def player_quits(game_id, player):
    return jsonify(service.player_quits(game_id, player))



def _get_int_param(name, data, required=True):
    if name not in data:
        if required:
            raise MalformedRequestException("int '{}' is required.".format(name))
        else:
            return None

    value = data[name]
    try:
        value = int(value)
    except ValueError:
        raise MalformedRequestException("'{}' should be a valid int.".format(name))
    return value

def _get_list_param(name, data, required=True):
    if name not in data:
        if required:
            raise MalformedRequestException("list '{}' is required.".format(name))
        else:
            return None

    if type(data[name]) != list:
        raise MalformedRequestException("'{}' must be a list.".format(name))
    return data[name]


