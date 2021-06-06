"""
Тесты.

Набор элементарных тестов.
"""

import sys
import os
import unittest
from unittest.mock import MagicMock
testdir = os.path.dirname(__file__)
srcdir = '../GameProject'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from base import Game, PLAYER_LAYER, TILESIZE, FLOOR_LAYER, SCREEN_WIDTH, SCREEN_HEIGHT, Player, Wall, Door, Exit, Floor, Dark, Coin, Trap, Enemy
sys.path.remove(os.path.abspath(os.path.join(testdir, srcdir)))


class TestBase(unittest.TestCase):
    """Инициализация класса для тестирования."""

    mypath = os.path.abspath(os.path.dirname(sys.argv[0])) + '/GameProject/RoomsInDungeon/'

    def setUp(self):
        """Инициализция нужных классов из base.py для последующей проверки."""
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

    def test_01_room_objects(self):
        """Проверка на то, нет ли в файлах комнат *.in неопознанных объектов."""
        # print(os.getcwd())
        rooms_list = [f for f in os.listdir(
            self.mypath) if os.path.isfile(os.path.join(self.mypath, f))]
        for room in rooms_list:
            if (self.mypath + str(room)) == self.mypath + "map.in":
                continue
            self.game.new(self.mypath + str(room))
            try:
                self.game.read_room_file(self.mypath + str(room))
            except ValueError:
                self.assertTrue(False)

    def test_02_gameSize(self):
        """Проверка на то, совпадают ли размеры окна с имеющимися константами, заданными в base.py."""
        self.assertEqual(self.game.screen.get_size(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def test_03_menu(self):
        """Проверка на то, корректно ли заданы параметры menu."""
        self.assertEqual(vars(self.game.menu.menu)["_window_size"], (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.assertEqual(vars(vars(vars(self.game.menu.menu)["_theme"])[
                         "background_color"])["_filepath"], self.mypath[:-16] + "/Screens/intro.png")
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

    def test_04_menu_obj(self):
        """Проверка на то, корректно ли работают виджеты в menu."""
        self.assertEqual(len((vars(self.game.menu.menu)["_widget_columns"])[0]), 5)

    def test_05_png_names(self):
        """Проверка на то, все ли файлы *.png используемые для прорисовки скриптов выбранных классов имеются в репозитории."""
        # print(os.getcwd())
        for name in self.game.png_names:
            self.assertTrue(os.path.exists(name))

    def test_06_player_class(self):
        """Проверка правильной инициализации класса Player."""
        self.assertEqual(self.game, self.player.game)
        self.assertEqual(PLAYER_LAYER, self.player._layer)
        self.assertEqual(self.player.width, TILESIZE)
        self.assertEqual(self.player.height, TILESIZE)
        self.assertEqual(self.player.x_change, 0)
        self.assertEqual(self.player.y_change, 0)
        self.assertEqual(self.player.facing, 'down')
        self.assertEqual(self.player.alive, True)
        self.assertEqual(self.player.win, False)
        self.assertEqual(self.player.collision_immune, False)
        self.assertEqual(self.player.collision_time, 0)
        self.assertEqual(self.player.attacking, False)
        self.assertEqual(self.player.attacking_time, 0)
        self.assertEqual(len(self.player.image_down), 8)
        self.assertEqual(len(self.player.image_up), 8)
        self.assertEqual(len(self.player.image_right), 8)
        self.assertEqual(len(self.player.image_left), 8)
        self.assertEqual(len(self.player.attackloop), 4)

    def test_07_wall_class(self):
        """Проверка правильной инициализации класса Wall."""
        self.assertEqual(self.game, self.wall.game)
        self.assertEqual(PLAYER_LAYER, self.wall._layer)
        self.assertEqual(self.wall.width, TILESIZE)
        self.assertEqual(self.wall.height, TILESIZE)

    def test_08_door_class(self):
        """Проверка правильной инициализации класса Door."""
        self.assertEqual(self.game, self.door.game)
        self.assertEqual(PLAYER_LAYER, self.door._layer)
        self.assertEqual(self.door.width, TILESIZE)
        self.assertEqual(self.door.height, TILESIZE)

    def test_09_exit_class(self):
        """Проверка правильной инициализации класса Exit."""
        self.assertEqual(self.game, self.exit.game)
        self.assertEqual(PLAYER_LAYER, self.exit._layer)
        self.assertEqual(self.exit.width, TILESIZE)
        self.assertEqual(self.exit.height, TILESIZE)

    def test_10_floor_class(self):
        """Проверка правильной инициализации класса Floor."""
        self.assertEqual(self.game, self.floor.game)
        self.assertEqual(FLOOR_LAYER, self.floor._layer)
        self.assertEqual(self.floor.width, TILESIZE)
        self.assertEqual(self.floor.height, TILESIZE)

    def test_11_dark_class(self):
        """Проверка правильной инициализации класса Dark."""
        self.assertEqual(self.game, self.dark.game)
        self.assertNotEqual(FLOOR_LAYER, self.dark._layer)
        self.assertEqual(self.dark.width, TILESIZE)
        self.assertEqual(self.dark.height, TILESIZE)

    def test_12_coin_class(self):
        """Проверка правильной инициализации класса Coin."""
        self.assertEqual(self.game, self.coin.game)
        self.assertEqual(PLAYER_LAYER, self.coin._layer)
        self.assertEqual(self.coin.width, TILESIZE)
        self.assertEqual(self.coin.height, TILESIZE)

    def test_13_trap_class(self):
        """Проверка правильной инициализации класса Trap."""
        self.assertEqual(self.game, self.trap.game)
        self.assertNotEqual(FLOOR_LAYER, self.trap._layer)
        self.assertEqual(self.trap.width, TILESIZE)
        self.assertEqual(self.trap.height, TILESIZE)

    def test_14_enemy_class(self):
        """Проверка правильной инициализации класса Enemy."""
        self.assertEqual(self.game, self.enemy.game)
        self.assertEqual(PLAYER_LAYER, self.enemy._layer)
        self.assertEqual(self.enemy.width, TILESIZE)
        self.assertEqual(self.enemy.height, TILESIZE)
        self.assertTrue(0 == self.enemy.randdirect or self.enemy.randdirect == 1)
        self.assertTrue((0 == self.enemy.x_direction and self.enemy.y_direction == 1
                         ) or (1 == self.enemy.x_direction and self.enemy.y_direction == 0))
        self.assertEqual(self.enemy.facing, 'down')
        self.assertEqual(self.enemy.lifes, 1)
        self.assertEqual(len(self.enemy.image_slime), 4)

    def test_15_game_methods(self):
        """Проверка методов класса Game – new() и read_room_file()."""
        rooms_list = [f for f in os.listdir(
            self.mypath) if os.path.isfile(os.path.join(self.mypath, f))]
        try:
            self.game.new(self.mypath + str(rooms_list[4]))
            self.game.read_room_file = MagicMock()
            self.game.new(self.mypath + str(rooms_list[4]))
        except Exception:
            self.assertTrue(False)
        else:
            self.game.read_room_file.assert_called_once_with(self.mypath + str(rooms_list[4]))
            self.assertIsNotNone(self.game.wall_list)
            self.assertIsNotNone(self.game.player)
            self.assertIsNotNone(self.game.doors_list)
            self.assertIsNotNone(self.game.floors_list)
