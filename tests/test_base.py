import unittest

from base import Game, SCREEN_WIDTH, SCREEN_HEIGHT


class TestBase(unittest.TestCase):
    
    def setUp(self):
        self.game = Game()

    def test_1_gameSize(self):      
        self.assertEqual(self.game.screen.get_size(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    