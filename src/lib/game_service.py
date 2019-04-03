from game_manager import GameManager
from game_state import GameState

"""This module represents the drop-token game service. All methods are 1:1 matches with api routes. Ideally documentation for the endpoints is done there."""

game_manager = GameManager()

def get_all_in_progress_games():
    output = {}
    output['games'] = get_all_games(game_state=GameState.IN_PROGRESS)
    return output


def create_new_game(players, columns, rows):
    output = {}
    new_game = game_manager.new_game(players, columns, rows)
    output['gameId'] = new_game.get_game_id()
    return output


def get_game_state(game_id):
    output = {}
    game = game_manager.get_game(game_id)
    output['players'] = game.get_players()
    game_state = game.get_game_state()
    output['state'] = game_state.name
    if game_state == GameState.DONE:
        output['winner'] = game.get_winner()
    return output


def get_game_moves(game_id, start=None, end=None):
    output = {}
    game = game_manager.get_game(game_id)
    output['moves'] = [_move_output(m) for m in game.get_all_moves_taken(start, end)]
    return output


def make_move(game_id, player, column):
    output = {}
    move = game_manager.get_game(game_id).play_token(player, column)
    output['move'] = '{}/moves/{}'.format(game_id, move.get_move_number())
    return output
    

def get_move(game_id, move_number):
    output = {}
    output['move'] = _move_output(game_manager.get_game(game_id).get_move(move_number))
    return output


def player_quits(game_id, player):
    game_manager.get_game(game_id).remove_player(player)
    return {}


def _move_output(move):
    output = {}
    output['type'] = move.get_type().name.upper()
    output['player'] = move.get_player()
    token = move.get_token()
    if token is not None:
        output['column'] = token.get_column()
    return output

