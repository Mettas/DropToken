from drop_token_game import DropTokenGame
from exception import GameNotFoundException


class GameManager:
    """Class to manager creation/delete/retrieval of games"""

    next_game_id = 1
    game_id_prefix = "gameid"


    @classmethod
    def generate_next_game_id(cls):
        """Makes a new unique game id per call."""
        game_id = cls.game_id_prefix + str(cls.next_game_id)
        cls.next_game_id += 1
        return game_id


    def __init__(self):
        self.games = {}
    

    def new_game(self, players, columns, rows):
        """Create a new DropTokenGame

        Arguments
        players -- list of players to join, must not contain duplicates
        columns -- width of the board
        rows -- height of the board
        """
        new_game = DropTokenGame(columns, rows, players, GameManager.generate_next_game_id())
        self.games[new_game.get_game_id()] = new_game
        return new_game


    def get_game(self, game_id):
        if game_id not in self.games:
            raise GameNotFoundException("Game '{}' not found.".format(game_id))
        return self.games[game_id]


    def get_all_games(self, game_state=None):
        if game_state is not None:
            return [g.get_game_id() for g in self.games.values() if g.get_game_state() is game_state]
        return self.games.values()
