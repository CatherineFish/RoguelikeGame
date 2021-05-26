import pygame
import pygame_menu
import gettext
import unittest

gettext.install("click", ".", names=("ngettext",))


class MyMenu:
    def __init__(self, bgColor, font, into_image, textColor, width, height):
        self.myImage = pygame_menu.baseimage.BaseImage(image_path=into_image,
                                                       drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        self.myTheme = pygame_menu.Theme(background_color=self.myImage,
                                         title_background_color=(76, 36, 25),
                                         title_font_shadow=True,
                                         widget_padding=25,
                                         widget_font="Arial",
                                         focus_background_color=(217, 140, 63),
                                         selection_color=(217, 178, 63),
                                         title_font_color=(217, 178, 63),
                                         widget_font_color=(217, 178, 63),
                                         title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE)


class Intro(MyMenu):

    def __init__(self, bgColor, font, into_image, textColor, width, height):
        MyMenu.__init__(self, bgColor, font, into_image, textColor, width, height)
        self.menu = pygame_menu.Menu(_('WELCOME!'), width, height, theme=self.myTheme)
        self.menu.add.text_input(_('Your name:'))
        self.menu.add.selector(_('Difficulty:'), [(_('Low'), 1), (_('Medium'), 2), (_('High'), 3)], onchange=self.set_difficulty)
        self.menu.add.selector(_('Сharacter:'), [(_('Name_1'), 1), (_('Name_2'), 2), (_('Name_3'), 3)], onchange=self.set_character)

        self.menu.add.button(_('Play'), self.start_the_game)

        self.menu.add.button(_('Instruction'), self.start_the_game)
        self.menu.add.button(_('Exit'), pygame_menu.events.EXIT)

    def set_character(self, value, character):
        pass

    def set_difficulty(self, value, difficulty):
        pass

    def start_the_game(self):
        self.menu.disable()
        self.menu.full_reset()
