import unittest
import pygame_menu
from base import Game, SCREEN_WIDTH, SCREEN_HEIGHT


class TestBase(unittest.TestCase):
    """Инициализация класса для тестирования"""

    def setUp(self):
        """Инициализция нужных классов из base.py для последующей проверки"""
        self.game = Game()

    def test_1_gameSize(self):
        """Проверка на то, совпадают ли размеры окна с имеющимися константами, заданными в base.py"""
        self.assertEqual(self.game.screen.get_size(), (SCREEN_WIDTH, SCREEN_HEIGHT))

    def test_2_menu(self):
        """Проверка на то, корректно ли заданы параметры menu"""
        self.assertEqual(vars(self.game.menu.menu)["_window_size"], (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.assertEqual(vars(vars(vars(self.game.menu.menu)["_theme"])[
                         "background_color"])["_filepath"], "intro.png")
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

    def test_3_menu_obj(self):
        """Проверка на то, корректно ли работают виджеты в menu"""
        self.assertEqual(len((vars(self.game.menu.menu)["_widget_columns"])[0]), 5)
