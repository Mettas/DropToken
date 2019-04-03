import unittest
from ..lib.game_state import GameState
from ..lib.drop_token_game import DropTokenGame
from ..lib.exception import *

class TestDropTokenGame(unittest.TestCase):
    
    def setUp(self):
        self.players = ['red', 'blue']

    def test_play_game_win(self):
        game = DropTokenGame(4, 4, self.players, 1)
        game.play_token(self.players[0], 0)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[1], 2)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[0], 0)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[1], 2)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[0], 1)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[1], 2)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[0], 1)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[1], 2)
        self.assertEquals(GameState.DONE, game.get_game_state())
        self.assertEquals("blue", game.get_winner())


    def test_play_game_draw(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[1], 1)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[0], 1)
        self.assertEquals(GameState.IN_PROGRESS, game.get_game_state())
        game.play_token(self.players[1], 0)
        self.assertEquals(GameState.DONE, game.get_game_state())
        self.assertEquals(None, game.get_winner())


    def test_invalid_move_off_board(self):
        game = DropTokenGame(2, 2, self.players, 1)
        with self.assertRaises(InvalidMoveException):
            game.play_token(self.players[0], 2)

        with self.assertRaises(InvalidMoveException):
            game.play_token(self.players[0], -1)


    def test_invalid_move_full_column(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        game.play_token(self.players[1], 0)
        with self.assertRaises(InvalidMoveException):
            game.play_token(self.players[0], 0)


    def test_wrong_player(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        with self.assertRaises(NotYourTurnException):
            game.play_token(self.players[0], 0)


    def test_wrong_player_first_turn(self):
        game = DropTokenGame(2, 2, self.players, 1)
        with self.assertRaises(NotYourTurnException):
            game.play_token(self.players[1], 0)


    def test_missing_player(self):
        game = DropTokenGame(2, 2, self.players, 1)
        with self.assertRaises(PlayerNotFoundException):
            game.play_token("bob", 0)


    def test_get_move(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        move = game.get_move(0)
        self.assertEquals(self.players[0], move.get_player())
        self.assertEquals(0, move.get_token().get_column())


    def test_get_move_not_found(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        with self.assertRaises(MovesNotFoundException):
            game.get_move(1)


    def test_get_all_moves_taken(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        game.play_token(self.players[1], 0)
        moves = game.get_all_moves_taken()
        self.assertEquals(2, len(moves))
        self.assertEquals(self.players[0], moves[0].get_player())
        self.assertEquals(0, moves[0].get_token().get_column())
        self.assertEquals(self.players[1], moves[1].get_player())
        self.assertEquals(0, moves[1].get_token().get_column())


    def test_get_all_moves_taken_no_moves(self):
        game = DropTokenGame(2, 2, self.players, 1)
        with self.assertRaises(MovesNotFoundException):
            moves = game.get_all_moves_taken()


    def test_get_all_moves_taken_range(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        game.play_token(self.players[1], 0)
        game.play_token(self.players[0], 1)
        game.play_token(self.players[1], 1)
        moves = game.get_all_moves_taken(start=2, end=3)
        self.assertEquals(2, len(moves))
        self.assertEquals(self.players[0], moves[0].get_player())
        self.assertEquals(1, moves[0].get_token().get_column())
        self.assertEquals(self.players[1], moves[1].get_player())
        self.assertEquals(1, moves[1].get_token().get_column())


    def test_get_all_moves_taken_range_not_found(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        game.play_token(self.players[1], 0)
        with self.assertRaises(MovesNotFoundException):
            moves = game.get_all_moves_taken(start=1, end=3)


    def test_get_all_moves_taken_range_not_found_negative(self):
        game = DropTokenGame(2, 2, self.players, 1)
        game.play_token(self.players[0], 0)
        game.play_token(self.players[1], 0)
        game.play_token(self.players[0], 1)
        game.play_token(self.players[1], 1)
        with self.assertRaises(MovesNotFoundException):
            moves = game.get_all_moves_taken(start=-1, end=1)

    

if __name__ == '__main__':
    unittest.main()
