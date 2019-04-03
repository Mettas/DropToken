import unittest
from ..lib.game_manager import GameManager
from ..lib.exception import *

class TestGameManager(unittest.TestCase):

    def setUp(self):
        self.game_manager = GameManager()


    def test_new_game(self):
        game = self.game_manager.new_game(['red', 'blue'], 4, 4)
        self.assertEquals(game, self.game_manager.get_game(game.get_game_id()))


    def test_game_not_found(self):
        game = self.game_manager.new_game(['red', 'blue'], 4, 4)
        with self.assertRaises(GameNotFoundException):
            self.game_manager.get_game(-1)

    
    def test_different_game_ids(self):
        game1 = self.game_manager.new_game(['red', 'blue'], 4, 4)
        game2 = self.game_manager.new_game(['red', 'blue'], 4, 4)
        self.assertNotEquals(game1.get_game_id(), game2.get_game_id())



if __name__ == '__main__':
    unittest.main()
