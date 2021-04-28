import unittest
from base import Game
import os


class TestBase(unittest.TestCase):
    """Инициализация класса для тестирования"""
    mypath = './rooms_in_dungeon/'

    def setUp(self):
        """Инициализция нужных классов из base.py для последующей проверки"""
        self.game = Game()

    def test_1_room_objects(self):
        """Проверка на то, нет ли в файлах комнат *.in неопознанных объектов"""
        # print(os.getcwd())
        rooms_list = [f for f in os.listdir(
            self.mypath) if os.path.isfile(os.path.join(self.mypath, f))]
        for room in rooms_list:
            self.game.new(self.mypath + str(room))
            try:
                self.game.read_room_file(self.mypath + str(room))
            except ValueError:
                self.assertTrue(False)
