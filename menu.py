"""
Базовый модуль для заставок в игре.

Предоставляет базовый класс с настройкой параметров темы, заднего фона и шрифтов.

:copyright: (c) 2021 by Larin Andrey and Chekhonina Ekaterina
:license: MIT, see COPYING for more details.
"""
import pygame_menu
import gettext

gettext.install("click", ".", names=("ngettext",))


class MyMenu:
    """
    Настройка темы для всех меню в игре.

    :param bgColor: цвет фона
    :param font: шрифт текста
    :param intro_image: изображение для заднего фона
    :param textColor: цвет текста
    :param width: ширина окна приложения
    :param height: высота окна приложения
    """

    def __init__(self, bgColor, font, intro_image, textColor, width, height):
        """Создание темы с конфертацией изображения под формат и всеми настройками."""
        self.myImage = pygame_menu.baseimage.BaseImage(image_path=intro_image,
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
    """
    Создание приветственного меню со считыванием имени, выбором игрока, уровня сложности и инструкцией.

    :param bgColor: цвет фона
    :param font: шрифт текста
    :param intro_image: изображение для заднего фона
    :param textColor: цвет текста
    :param width: ширина окна приложения
    :param height: высота окна приложения
    """

    def __init__(self, game, bgColor, font, intro_image, textColor, width, height):
        """Создание приветственного меню со всеми необходимыми кнопками."""
        MyMenu.__init__(self, bgColor, font, intro_image, textColor, width, height)
        self.gameScreen = game.screen
        self.MyInstruction = Instruction(bgColor, font, intro_image, textColor, width, height)
        self.menu = pygame_menu.Menu(_('WELCOME!'), width, height, theme=self.myTheme)
        self.current_name = ''
        self.menu.add.text_input(_('Your name:'), onchange=self.get_name, onreturn=self.get_name)
        self.menu.add.selector(_('Difficulty:'), [(_('Low'), 1), (_('Medium'), 2), (_('High'), 3)], onchange=self.set_difficulty)
        self.menu.add.selector(_('Сharacter:'), [(_('Name_1'), 1), (_('Name_2'), 2), (_('Name_3'), 3)], onchange=self.set_character)
        self.menu.add.button(_('Play'), lambda: self.start_the_game(game))
        self.menu.add.button(_('Instruction'), self.instruction)
        self.menu.add.button(_('Exit'), pygame_menu.events.EXIT)

    def get_name(self, name):
        """
        Захват имени игрока.

        :param name: введённое имя игрока
        """
        self.current_name = name

    def instruction(self):
        """Вызов окна-инструкции с его созданием, если нужно."""
        self.MyInstruction.InstructionMenu.mainloop(self.gameScreen)
        self.MyInstruction.InstructionMenu.enable()

    def set_character(self, value, character):
        """
        Установка выбранного персонажа.

        :param value: выбранный персонаж
        """
        pass

    def set_difficulty(self, value, difficulty):
        """
        Установка сложности игры.

        :param value: выбранный уровень сложности
        """
        pass

    def start_the_game(self, game, **kwargs):
        """
        Запуск игры через выключение привественного окна.

        :param game: сама игра для передачи имени игрока
        """
        game.playerName = self.current_name
        self.menu.disable()
        self.menu.full_reset()


class Instruction(MyMenu):
    """
    Создание меню инструкции, которое может возвращаться на окно привествия.

    :param bgColor: цвет фона
    :param font: шрифт текста
    :param intro_image: изображение для заднего фона
    :param textColor: цвет текста
    :param width: ширина окна приложения
    :param height: высота окна приложения
    """

    def __init__(self, bgColor, font, intro_image, textColor, width, height):
        """Создание меню инструкции с текстом инструкции."""
        MyMenu.__init__(self, bgColor, font, intro_image, textColor, width, height)
        self.InstructionMenu = pygame_menu.Menu(_('Instruction'), width, height, theme=self.myTheme)
        instruction_intro = [_('Your goal is to find your way out of the dungeon!'),
                             _('Control:'),
                             _('W - up'),
                             _('S - down'),
                             _('D - right'),
                             _('A - left'),
                             _('Collect coins to get more points'),
                             _('Darkness is deadly to you'),
                             _('Traps can hurt you'),
                             _('GOOG LUCK!'),
                             ]
        for inst in instruction_intro:
            self.InstructionMenu.add.label(inst, align=pygame_menu.locals.ALIGN_CENTER, font_size=25)
        self.InstructionMenu.add.vertical_margin(30)
        self.InstructionMenu.add.button(_('Back'), self.back_to_menu)

    def back_to_menu(self):
        """Обработка кнопки возвращении к привественному меню."""
        self.InstructionMenu.disable()


class DieScreen(MyMenu):
    """
    Создание меню при смерти персонажа.

    :param bgColor: цвет фона
    :param font: шрифт текста
    :param intro_image: изображение для заднего фона
    :param textColor: цвет текста
    :param width: ширина окна приложения
    :param height: высота окна приложения
    """

    def __init__(self, bgColor, font, intro_image, textColor, width, height, die_image, coins, playerName):
        """Создание экрана смерти со всеми необходимыми кнопками."""
        MyMenu.__init__(self, bgColor, font, intro_image, textColor, width, height)
        self.DieMenu = pygame_menu.Menu(_('GAME OVER!'), width, height, theme=self.myTheme)
        self.image_die = pygame_menu.baseimage.BaseImage(image_path=die_image,
                                                         drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        self.DieMenu.add.image(self.image_die, scale_smooth=True, align=pygame_menu.locals.ALIGN_CENTER)
        die_text = _(f'''{playerName}, you died!\nYou collected {coins} coins''')
        self.DieMenu.add.label(die_text, align=pygame_menu.locals.ALIGN_CENTER, font_size=30)
        self.DieMenu.add.button(_('Exit'), self.exit)

    def exit(self):
        """Завершение работы приложения при нажатии на кнопку выхода."""
        self.DieMenu.disable()
        self.DieMenu.full_reset()


class WinScreen(MyMenu):
    """
    Создание меню при победе персонажа.

    :param bgColor: цвет фона
    :param font: шрифт текста
    :param intro_image: изображение для заднего фона
    :param textColor: цвет текста
    :param width: ширина окна приложения
    :param height: высота окна приложения
    """

    def __init__(self, bgColor, font, intro_image, textColor, width, height, win_image, coins, playerName):
        """Создание экрана победы со всеми необходимыми кнопками."""
        MyMenu.__init__(self, bgColor, font, intro_image, textColor, width, height)
        self.WinMenu = pygame_menu.Menu(_('CONGRATULATION!'), width, height, theme=self.myTheme)
        self.image_win = pygame_menu.baseimage.BaseImage(image_path=win_image,
                                                         drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
        self.WinMenu.add.image(self.image_win, scale_smooth=True, align=pygame_menu.locals.ALIGN_CENTER)
        win_text = _(f'''{playerName}, you win!\nYou collected {coins} coins''')
        self.WinMenu.add.label(win_text, align=pygame_menu.locals.ALIGN_CENTER, font_size=30)
        self.WinMenu.add.button(_('Exit'), self.exit)

    def exit(self):
        """Завершение работы приложения при нажатии на кнопку выхода."""
        self.WinMenu.disable()
        self.WinMenu.full_reset()
