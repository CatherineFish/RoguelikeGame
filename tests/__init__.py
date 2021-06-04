import sys, os
testdir = os.path.dirname(__file__)
srcdir = '../GameProject'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from base import Game, SCREEN_WIDTH, SCREEN_HEIGHT, Player, Wall, Door, Exit, Floor, Dark, Coin, Trap, Enemy
import os


class TestBase(unittest.TestCase):
    """Инициализация класса для тестирования"""
    mypath = 'GameProject/RoomsInDungeon/'

    def setUp(self):
        """Инициализция нужных классов из base.py для последующей проверки"""
        self.game = Game()
        self.player = Player(self.game, 0, 0)
        self.wall = Wall(self.game, 0, 0)
        self.door = Door(self.game, 0, 0)
        self.exit = Exit(self.game, 0, 0)
        self.floor = Floor(self.game, 0, 0)
        self.dark = Dark(self.game, 0, 0)
        self.trap = Trap(self.game, 0, 0)
        self.enemy = Enemy(self.game, 0, 0)
        self.coin = Coin(self.game, 0, 0)

    def test_1_room_objects(self):
        """Проверка на то, нет ли в файлах комнат *.in неопознанных объектов"""
        # print(os.getcwd())
        rooms_list = [f for f in os.listdir(
            self.mypath) if os.path.isfile(os.path.join(self.mypath, f))]
        for room in rooms_list:
            if (self.mypath + str(room)) == 'GameProject/RoomsInDungeon/map.in':
                continue
            self.game.new(self.mypath + str(room))
            try:
                self.game.read_room_file(self.mypath + str(room))
            except ValueError:
                self.assertTrue(False)

    def test_2_gameSize(self):
        """Проверка на то, совпадают ли размеры окна с имеющимися константами, заданными в base.py"""
        self.assertEqual(self.game.screen.get_size(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def test_3_menu(self):
        """Проверка на то, корректно ли заданы параметры menu"""
        self.assertEqual(vars(self.game.menu.menu)["_window_size"], (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.assertEqual(vars(vars(vars(self.game.menu.menu)["_theme"])[
                         "background_color"])["_filepath"], "GameProject/Screens/intro.png")
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])[
                         "title_background_color"], (76, 36, 25, 255))
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])["widget_padding"], 25)
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])["widget_font"], "Arial")
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])["title_font_shadow"], True)
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])[
                         "focus_background_color"], (217, 140, 63, 255))
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])[
                         "selection_color"], (217, 178, 63, 255))
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])[
                         "title_font_color"], (217, 178, 63, 255))
        self.assertEqual(vars(vars(self.game.menu.menu)["_theme"])[
                         "widget_font_color"], (217, 178, 63, 255))

    def test_4_menu_obj(self):
        """Проверка на то, корректно ли работают виджеты в menu"""
        self.assertEqual(len((vars(self.game.menu.menu)["_widget_columns"])[0]), 5)

    def test_1_png_names(self):
        """Проверка на то, все ли файлы *.png используемые для прорисовки скриптов выбранных классов имеются в репозитории"""
        # print(os.getcwd())
        for name in self.game.png_names:
            self.assertTrue(os.path.exists(name))
