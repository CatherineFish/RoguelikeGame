import unittest
from base import Player, Wall, Door, Exit, Floor, Dark, Coin, Trap, Enemy, Game
import os


class TestBase(unittest.TestCase):
    """Инициализация класса для тестирования"""

    def setUp(self):
        """Инициализция нужных классов из base.py для последующей проверки"""
        self.game = Game()
        self.player = Player(self.game, 0, 0)
        self.wall = Wall(self.game, 0, 0)
        self.door = Door(self.game, 0, 0)
        self.exit = Exit(self.game, 0, 0)
        self.floor = Floor(self.game, 0, 0)

    def test_1_png_names(self):
        """Проверка на то, все ли файлы *.png используемые для прорисовки скриптов имеются в репоизтории"""
        # print(os.getcwd())
        for name in self.game.png_names:
            self.assertTrue(os.path.exists(name))
