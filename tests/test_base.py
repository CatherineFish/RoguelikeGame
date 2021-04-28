import unittest

from base import Game, SCREEN_WIDTH, SCREEN_HEIGHT


class TestBase(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()

    def test_1_gameSize(self):      
        self.assertEqual(self.game.screen.get_size(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def test_2_menu(self):
        self.assertEqual(vars(self.game.menu.menu)["_window_size"], (SCREEN_WIDTH, SCREEN_HEIGHT)) 
        self.assertEqual(vars(vars(vars(self.game.menu.menu)["_theme"])["background_color"])["_filepath"], "intro.png") 
        