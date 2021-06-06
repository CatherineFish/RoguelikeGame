"""
Базовый модуль Roguelike 2D-игры.

Описывает набор базовых классов

:copyright: (c) 2021 by Larin Andrey and Chekhonina Ekaterina
:license: MIT, see COPYING for more details.
"""

import pygame
import gettext
import random
import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '../GameProject'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import __init__ as menu
sys.path.remove(os.path.abspath(os.path.join(testdir, srcdir)))


gettext.install("game", os.path.dirname(__file__), names=("ngettext",))
dir_path_tileset = os.path.abspath(os.path.dirname(sys.argv[0])) + "/Tileset/"

# Объявление глобальных переменны.

# Объявление уровня дебага, для отладки ошибок,
# по умолчанию установлен в 0
# (без вывода сообщений об ошибках)

ERROR_TIME = 0
ERROR_LEVEL = 0

# Объявление глобальных цветов
PINK = (221, 160, 221)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (29, 32, 76)
GREY = (127, 127, 127)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Объявление глобального размера игрового окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608

# Объявление глобального размера игровой ячейки (игрового "пикселя")
TILESIZE = 32

# Объявление глобального размера персонажа игры
PLAYER_TILESIZE = 30

# Объявление глобальной кадровой частоты
FPS = 60

# Объявление глобальных уровней прорисовки спрайтов
# спрайт игрока выше спрайта пола
PLAYER_LAYER = 2
FLOOR_LAYER = 1

# Объявление глобальных уровней прорисовки спрайтов
PLAYER_SPEED = 3

# Объявление глобальных переменных
# для отслеживания спрайтов с анимациями
animation_count = 0


class Player(pygame.sprite.Sprite):
    """
    Базовый класс, задающий персонажа.

    :param game: игра, в которой существует Персонаж
    :param x: координата персонажа по оси абсцисс
    :param y: координата персонажа по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Персонажа с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # Инициализация координат персонажа.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # Инициализация размера персонажа.
        self.width = TILESIZE
        self.height = TILESIZE

        # Инициализация скорости персонажа.
        self.x_change = 0
        self.y_change = 0
        # Куда смотрит персонаж в данных момент.
        self.facing = 'down'

        # Инициализация списков со спрайтами других классов.
        self.walls = None
        self.coins = None
        self.traps = None
        self.darks = None
        self.doors = None
        self.exits = None
        self.enemies = None

        # Инициализация флагов пермещений между комнатами.
        self.go_up = False
        self.go_down = False
        self.go_right = False
        self.go_left = False

        # Жив ли персонаж?
        self.alive = True

        # Выиграл ли персонаж?
        self.win = False

        # Флаг и отслеживания времени для неуязвимости.
        self.collision_immune = False
        self.collision_time = 0

        # Флаг для атак.
        self.attacking = False
        self.attacking_time = 0

        # Инициализация изображений для персонажа.
        down1 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down1.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        down2 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down2.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        down3 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down3.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        down4 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down4.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        down5 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down5.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        down6 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down6.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        down7 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down7.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        down8 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'down8.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        self.image_down = [down1, down2, down3, down4, down5, down6, down7, down8]
        up1 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up1.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        up2 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up2.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        up3 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up3.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        up4 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up4.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        up5 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up5.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        up6 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up6.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        up7 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up7.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        up8 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'up8.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        self.image_up = [up1, up2, up3, up4, up5, up6, up7, up8]
        left1 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left1.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        left2 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left2.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        left3 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left3.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        left4 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left4.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        left5 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left5.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        left6 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left6.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        left7 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left7.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        left8 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'left8.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        self.image_left = [left1, left2, left3, left4, left5, left6, left7, left8]
        right1 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right1.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        right2 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right2.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        right3 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right3.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        right4 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right4.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        right5 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right5.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        right6 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right6.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        right7 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right7.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        right8 = pygame.transform.scale(pygame.image.load(
            dir_path_tileset + 'right8.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        self.image_right = [right1, right2, right3, right4, right5, right6, right7, right8]
        for i in range(8):
            self.game.png_names.add(dir_path_tileset + f"down{i+1}.png")
            self.game.png_names.add(dir_path_tileset + f"up{i+1}.png")
            self.game.png_names.add(dir_path_tileset + f"left{i+1}.png")
            self.game.png_names.add(dir_path_tileset + f"right{i+1}.png")

        self.image = down1

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()
        self.rect = pygame.rect.Rect((0, 0), (self.width - 12, self.height - 2))

        # Инциализация colliderect для описания коллизий.
        self.collideRect = pygame.rect.Rect((0, 0), (self.width - 28, 8))
        self.rect.x = self.x
        self.rect.y = self.y

        # Инциализация attackrect для описания атак.
        self.attackimage = pygame.image.load(dir_path_tileset + "slash.png").convert_alpha()
        self.game.png_names.add(dir_path_tileset + 'slash.png')
        sprite0, sprite1, sprite2, sprite3 = pygame.Surface([TILESIZE, TILESIZE]), pygame.Surface(
            [TILESIZE, TILESIZE]), pygame.Surface([TILESIZE, TILESIZE]), pygame.Surface([TILESIZE, TILESIZE])
        sprite0.blit(self.attackimage, (0, 0), (0, 0, TILESIZE, TILESIZE))
        sprite0.set_colorkey(BLACK)
        sprite1.blit(self.attackimage, (0, 0), (32, 0, TILESIZE, TILESIZE))
        sprite1.set_colorkey(BLACK)
        sprite2.blit(self.attackimage, (0, 0), (64, 0, TILESIZE, TILESIZE))
        sprite2.set_colorkey(BLACK)
        sprite3.blit(self.attackimage, (0, 0), (96, 0, TILESIZE, TILESIZE))
        sprite3.set_colorkey(BLACK)
        self.attackloop = [sprite0, sprite1, sprite2, sprite3]
        self.attackrect = self.attackloop[0].get_rect()

        # Сolliderect будет совпадать с нашей rect картинкой по середине нижней грани (ногам).
        self.collideRect.midbottom = self.rect.midbottom

        # attackrect верхней гранью будет совпадать с нашей rect картинкой по середине нижней грани.
        self.attackrect.midtop = self.rect.midbottom

    def update(self):
        """Объявления основных механик и их изменение во времени."""
        # Будем изменять глобальную переменную смены анимаций персонажа.
        global animation_count
        # Считывание движений с клавиатуры.
        self.movement()
        # Изменение переменной анимицации персонажа, а вместе с ней и изображения.
        animation_count += 1
        if animation_count + 1 >= 24:
            animation_count = 0
        if self.x_change != 0 or self.y_change != 0:
            if self.facing == "right":
                self.image = self.image_right[animation_count // 8]
                self.attackrect.midleft = self.rect.midright
            elif self.facing == "left":
                self.image = self.image_left[animation_count // 8]
                self.attackrect.midright = self.rect.midleft
            elif self.facing == "up":
                self.image = self.image_up[animation_count // 8]
                self.attackrect.midbottom = self.rect.midtop
            else:
                self.image = self.image_down[animation_count // 8]
                self.attackrect.midtop = self.rect.midbottom

        # Движение по оси x и проверка коллизий со стенами.
        self.rect.x += self.x_change
        self.collideRect.midbottom = self.rect.midbottom
        rect_list = []
        for sprite in self.walls:
            rect_list.append(sprite.rect)
        block_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        for block in block_hit_list:
            if ERROR_LEVEL == 1:
                print("hitted wall")
            if self.x_change > 0:
                self.collideRect.right = rect_list[block].left
                self.rect.midbottom = self.collideRect.midbottom
            else:
                self.collideRect.left = rect_list[block].right
                self.rect.midbottom = self.collideRect.midbottom
        if self.collideRect.x > SCREEN_WIDTH:
            self.collideRect.x = SCREEN_WIDTH
            self.rect.midbottom = self.collideRect.midbottom
        if self.collideRect.x < 0:
            self.collideRect.x = 0
            self.rect.midbottom = self.collideRect.midbottom

        # Движение по оси y и проверка коллизий со стенами.
        self.rect.y += self.y_change
        self.collideRect.midbottom = self.rect.midbottom
        rect_list = []
        for sprite in self.walls:
            rect_list.append(sprite.rect)
        block_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        for block in block_hit_list:
            if self.y_change > 0:
                self.collideRect.bottom = rect_list[block].top
                self.rect.midbottom = self.collideRect.midbottom
            else:
                self.collideRect.top = rect_list[block].bottom
                self.rect.midbottom = self.collideRect.midbottom
        if self.collideRect.y > SCREEN_HEIGHT:
            self.collideRect.y = SCREEN_HEIGHT
            self.rect.midbottom = self.collideRect.midbottom
        if self.collideRect.y < 0:
            self.collideRect.y = 0
            self.rect.midbottom = self.collideRect.midbottom

        # Сдвиг attackrect во время движения персонажа.
        if self.facing == "right":
            self.attackrect.midleft = self.rect.midright
        elif self.facing == "left":
            self.attackrect.midright = self.rect.midleft
        elif self.facing == "up":
            self.attackrect.midbottom = self.rect.midtop
        else:
            self.attackrect.midtop = self.rect.midbottom

        # Проверка коллизий с дверьми.
        rect_list = []
        for sprite in self.doors:
            rect_list.append(sprite.rect)
        doors_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        for door_find in doors_hit_list:

            # Определение перехода в следующую комнату:
            # go_down – переход в комнату ниже текущей
            # go_left – переход в комнату левее текущей
            # go_right – переход в комнату правее текущей
            # go_up – переход в комнату выше текущей
            if self.facing == 'down':
                self.go_down = True
                self.go_left = False
                self.go_right = False
                self.go_up = False
            elif self.facing == 'left':
                self.go_down = False
                self.go_left = True
                self.go_right = False
                self.go_up = False
            elif self.facing == 'right':
                self.go_down = False
                self.go_left = False
                self.go_right = True
                self.go_up = False
            elif self.facing == 'up':
                self.go_down = False
                self.go_left = False
                self.go_right = False
                self.go_up = True

        # Проверка коллизий с монетами.
        rect_list = []
        sprite_list = []
        for sprite in self.coins:
            rect_list.append(sprite.rect)
            sprite_list.append(sprite)
        coins_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        for coin_find in coins_hit_list:
            self.game.collected_coins += 1
            self.game.collected_coins_list.append(
                [sprite_list[coin_find].x // TILESIZE, sprite_list[coin_find].y // TILESIZE])
            sprite_list[coin_find].kill()

        # Проверка коллизий с ловушками.
        rect_list = []
        sprite_list = []
        for sprite in self.traps:
            rect_list.append(sprite.rect)
            sprite_list.append(sprite)
        traps_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        if not self.collision_immune:
            for trap_find in traps_hit_list:
                if sprite_list[trap_find].image == sprite_list[trap_find].image_traps[0]:
                    menu.lifes -= 1
                    self.collision_immune = True
                    self.collision_time = pygame.time.get_ticks()
                    break

        rect_list = []
        for sprite in self.enemies:
            rect_list.append(sprite.rect)
        enemies_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        #  if ERROR_LEVEL == 1:
        #     print("here was:", type(enemies_hit_list), ' ;', len(enemies_hit_list))
        if not self.collision_immune:
            if len(enemies_hit_list) > 0:
                menu.lifes -= 1
                self.collision_immune = True
                self.collision_time = pygame.time.get_ticks()

        # Проверка на конец жизней.
        if menu.lifes <= 0:
            self.alive = False

        # Проверка на конец времени неуязвимости.
        if pygame.time.get_ticks() - self.collision_time > 3000:    # время в ms.
            self.collision_immune = False

        # Проверка на конец времени атаки.
        if pygame.time.get_ticks() - self.attacking_time > 500:    # время в ms.
            self.attacking = False

        # Проверка коллизий с темнотой.
        rect_list = []
        for sprite in self.darks:
            rect_list.append(sprite.rect)
        dark_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        if len(dark_hit_list) > 0:
            menu.lifes = 0

        # Проверка коллизий с выходом.
        rect_list = []
        for sprite in self.exits:
            rect_list.append(sprite.rect)
        exit_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        # Выставление флага победы на True
        if len(exit_hit_list) > 0:
            self.win = True

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        """
        Функция по обработке нажатия клавиш.

        pygame.K_w (клавиша "W") -- появляется скорость персонажа по y координате. //
        // Она направлена вверх
        pygame.K_a (клавиша "A") -- появляется скорость персонажа по x координате. //
        // Она направлена влево
        pygame.K_s (клавиша "S") -- появляется скорость персонажа по y координате. //
        // Она направлена вниз
        pygame.K_D (клавиша "D") -- появляется скорость персонажа по x координате. //
        // Она направлена вправо
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        if keys[pygame.K_SPACE]:
            if self.attacking is False:
                self.attacking = True
                self.attacking_time = pygame.time.get_ticks()


class Wall(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Стену.

    Персонаж не может проходить через Стену.

    :param game: игра, в которой существует Стена
    :param x: координата Стены по оси абсцисс
    :param y: координата Стены по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Стена с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # инициализация координат стены.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера стены.
        self.width = TILESIZE
        self.height = TILESIZE

        # инициализация картинки для стены.
        self.image = pygame.transform.scale2x(pygame.image.load(
            dir_path_tileset + 'white_wall.png').convert())
        self.game.png_names.add(dir_path_tileset + 'white_wall.png')

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Door(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Дверь.

    При соприкосновении с Дверью Персонаж переходит в другую комнату.

    :param game: игра, в которой существует Дверь
    :param x: координата Двери по оси абсцисс
    :param y: координата Двери по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Дверь с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # инициализация координат двери.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера двери.
        self.width = TILESIZE
        self.height = TILESIZE

        # инициализация картинки для двери.
        self.image = pygame.transform.scale2x(pygame.image.load(
            dir_path_tileset + 'white_door.png').convert())
        self.game.png_names.add(dir_path_tileset + 'white_door.png')

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Exit(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Выход.

    При соприкосновении с Выходом Персонаж выигрывает.

    :param game: игра, в которой существует Выход
    :param x: координата Выхода по оси абсцисс
    :param y: координата Выхода по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Выход."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # инициализация координат выхода.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера выхода.
        self.width = TILESIZE
        self.height = TILESIZE

        # инициализация картинки для выхода.
        self.image = pygame.transform.scale2x(pygame.image.load(
            dir_path_tileset + 'white_exit.png').convert())
        self.game.png_names.add(dir_path_tileset + 'white_exit.png')

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Floor(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Пол.

    Персонаж умеет ходить по Полу.

    :param game: игра, в которой существует Пол
    :param x: координата Пола по оси абсцисс
    :param y: координата Пола по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Пол с начальными настройками."""
        self.game = game
        self._layer = FLOOR_LAYER
        super().__init__()

        # инициализация координат пола.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера пола.
        self.width = TILESIZE
        self.height = TILESIZE

        # инициализация картинки для пола.
        self.image = pygame.transform.scale2x(pygame.image.load(
            dir_path_tileset + 'white_floor.png').convert())
        self.game.png_names.add(dir_path_tileset + 'white_floor.png')

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Dark(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Темноту.

    При попадании на Темноту Персонаж умирает.

    :param game: игра, в которой существует Темнота
    :param x: координата Темноты по оси абсцисс
    :param y: координата Темноты по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Темнота с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # инициализация координат темноты.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера темноты.
        self.width = TILESIZE
        self.height = TILESIZE

        # инициализация картинки для темноты.
        self.image = pygame.transform.scale2x(
            pygame.image.load(dir_path_tileset + 'dark.png').convert())
        self.game.png_names.add(dir_path_tileset + 'dark.png')

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Coin(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Монету.

    При соприкосновении с Монетой Персонаж подбирает её.

    :param game: игра, в которой существует Монета
    :param x: координата Монеты по оси абсцисс
    :param y: координата Монеты по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Монета с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # инициализация координат монеты.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера монеты.
        self.width = TILESIZE
        self.height = TILESIZE

        # инициализация картинки для монеты.
        self.image = pygame.image.load(dir_path_tileset + 'loot_gold.png').convert_alpha()
        self.game.png_names.add(dir_path_tileset + 'loot_gold.png')

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Trap(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Ловушку.

    При соприкосновении с Ловушкой Персонаж теряет одну жизнь.

    :param game: игра, в которой существует Ловушка
    :param x: координата Ловушки по оси абсцисс
    :param y: координата Ловушки по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Ловушка."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # инициализация координат ловушки.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера ловушки.
        self.width = TILESIZE
        self.height = TILESIZE

        # Будем изменять переменную смены анимаций ловушки.
        self.animation_count_trap = 0

        # инициализация изображений для ловушки.
        trap1 = pygame.transform.scale2x(pygame.image.load(
            dir_path_tileset + 'trap1.png')).convert_alpha()
        trap2 = pygame.transform.scale2x(pygame.image.load(
            dir_path_tileset + 'trap2.png')).convert_alpha()
        self.game.png_names.add(dir_path_tileset + 'trap1.png')
        self.game.png_names.add(dir_path_tileset + 'trap2.png')

        # Инциализация rect для заданного изображения.
        self.image = trap1
        self.image_traps = [trap1, trap2]

        # Инциализация rect для заданной картинки.
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """Объявления основных механик и их изменение во времени."""
        # Изменение переменной анимицации ловушки, а вместе с ней и изображения
        self.animation_count_trap += 1
        if self.animation_count_trap + 1 >= 180:
            self.animation_count_trap = 0
        self.image = self.image_traps[self.animation_count_trap // 90]


class Enemy(pygame.sprite.Sprite):
    """
    Базовый класс, задающий Врага.

    При столкновении с Врагом Персонаж теряет жизнь.

    :param game: игра, в которой существует Враг
    :param x: координата Врага по оси абсцисс
    :param y: координата Врага по оси ординат
    """

    def __init__(self, game, x, y):
        """Создание класса Враг."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        # инициализация координат врага.
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        # инициализация размера врага.
        self.width = TILESIZE
        self.height = TILESIZE

        # инициализация хаотичного движения врага.
        self.randdirect = random.randint(0, 1)
        if self.randdirect:
            self.start = self.x - TILESIZE * random.randint(1, 3)
            self.stop = self.x + TILESIZE * random.randint(5, 8)
            self.x_direction = 1
            self.y_direction = 0
        else:
            self.start = self.y - TILESIZE * random.randint(1, 3)
            self.stop = self.y + TILESIZE * random.randint(5, 8)
            self.y_direction = 1
            self.x_direction = 0

        # инициализация классов стен для врага.
        self.walls = None
        self.facing = 'down'

        # инициализация жизней для врага.
        self.lifes = 1

        # Будем изменять переменную смены анимаций персонажа.
        self.animation_count_slime = 0

        # инициализация изображений для врага.
        slime1 = pygame.image.load(dir_path_tileset + 'slime1.png').convert_alpha()
        slime2 = pygame.image.load(dir_path_tileset + 'slime2.png').convert_alpha()
        slime3 = pygame.image.load(dir_path_tileset + 'slime3.png').convert_alpha()
        slime4 = pygame.image.load(dir_path_tileset + 'slime4.png').convert_alpha()
        self.game.png_names.add(dir_path_tileset + 'slime1.png')
        self.game.png_names.add(dir_path_tileset + 'slime2.png')
        self.game.png_names.add(dir_path_tileset + 'slime3.png')
        self.game.png_names.add(dir_path_tileset + 'slime4.png')
        self.image_slime = [slime1, slime2, slime3, slime4]

        # Инциализация rect для заданной картинки.
        self.image = slime1
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        """Объявления основных механик и их изменение во времени."""
        # Инициализация скорости врага и направления движения
        if self.randdirect:
            self.rect.x += self.x_direction * 2
            block_hit_list = pygame.sprite.spritecollide(self, self.game.player.walls, False)
            for block in block_hit_list:
                if self.x_direction > 0:
                    self.rect.right = block.rect.left
                    self.x_direction = -1
                else:
                    self.rect.left = block.rect.right
                    self.x_direction = 1
            dark_hit_list = pygame.sprite.spritecollide(self, self.game.player.darks, False)
            for block in dark_hit_list:
                if self.x_direction > 0:
                    self.rect.right = block.rect.left
                    self.x_direction = -1
                else:
                    self.rect.left = block.rect.right
                    self.x_direction = 1
            trap_hit_list = pygame.sprite.spritecollide(self, self.game.player.traps, False)
            for block in trap_hit_list:
                if self.x_direction > 0:
                    self.rect.right = block.rect.left
                    self.x_direction = -1
                else:
                    self.rect.left = block.rect.right
                    self.x_direction = 1

            if self.rect.x <= self.start:
                self.rect.x = self.start
                self.x_direction = 1
            if self.rect.x >= self.stop:
                self.rect.x = self.stop
                self.x_direction = -1
        else:
            self.rect.y += self.y_direction * 2
            block_hit_list = pygame.sprite.spritecollide(self, self.game.player.walls, False)
            for block in block_hit_list:
                if self.y_direction > 0:
                    self.rect.bottom = block.rect.top
                    self.y_direction = -1
                else:
                    self.rect.top = block.rect.bottom
                    self.y_direction = 1
            dark_hit_list = pygame.sprite.spritecollide(self, self.game.player.darks, False)
            for block in dark_hit_list:
                if self.y_direction > 0:
                    self.rect.bottom = block.rect.top
                    self.y_direction = -1
                else:
                    self.rect.top = block.rect.bottom
                    self.y_direction = 1
            trap_hit_list = pygame.sprite.spritecollide(self, self.game.player.traps, False)
            for block in trap_hit_list:
                if self.y_direction > 0:
                    self.rect.bottom = block.rect.top
                    self.y_direction = -1
                else:
                    self.rect.top = block.rect.bottom
                    self.y_direction = 1

            if self.rect.y <= self.start:
                self.rect.y = self.start
                self.y_direction = 1
            if self.rect.y >= self.stop:
                self.rect.y = self.stop
                self.y_direction = -1

        # Изменение изображения врага.
        self.animation_count_slime += 1
        if self.animation_count_slime + 1 >= 40:
            self.animation_count_slime = 0
        #  print(animation_count_slime)
        self.image = self.image_slime[self.animation_count_slime // 10]

        # Проверка коллизий с атакой персонажа.
        if self.game.player.attacking:
            if pygame.Rect.colliderect(self.rect, self.game.player.attackrect):
                self.lifes -= 1

        if self.lifes <= 0:
            self.game.killed_enemies_list.append(
                [self.x // TILESIZE, self.y // TILESIZE])
            self.kill()


class Game:
    """
    Базовый класс, задающий Игру.

    Реагирует на различные игровые события.
    """

    png_names = set()
    collected_coins = 0

    def __init__(self):
        """Создание класса Игра с настройкой размера окна игры."""
        pygame.init()
        self.collected_coins_list = []
        self.killed_enemies_list = []
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        #  self.font = pygame.font.Font('Arial', 32)
        self.running = True
        self.playerName = ''
        self.menu = menu.Intro(self,
                               BLUE,
                               "Arial",
                               os.path.abspath(os.path.dirname(sys.argv[0])) + "/Screens/intro.png",
                               WHITE,
                               SCREEN_WIDTH,
                               SCREEN_HEIGHT)
        self.png_names.add(os.path.abspath(os.path.dirname(sys.argv[0])) + "/Screens/intro.png")

    def read_room_file(self, room):
        """Функция, считывающая все объекты, хранящиеся в файле комнаты."""
        # открываем файл комнаты с координатам.
        with open(room, 'r') as f:
            data = f.read()
            lines = data.splitlines()
            # для каждой считанной координаты ставим в соответсвие объект игры.
            for j in range(0, 19):
                for i in range(0, 25):
                    if lines[j][i] == "#":
                        # если встретилась стена.
                        self.wall_coords.append([i, j])
                    elif lines[j][i] == "m":
                        # если встретилась монета.
                        self.coins_coord.append([i, j])
                    elif lines[j][i] == "x":
                        # если встретилась дверь.
                        self.doors_coord.append([i, j])
                    elif lines[j][i] == "T":
                        # если встретилась ловушка.
                        self.traps_coord.append([i, j])
                    elif lines[j][i] == " ":
                        # если встретилась темнота.
                        self.darks_coord.append([i, j])
                    elif lines[j][i] == "e":
                        # если встретился враг.
                        self.enemies_coord.append([i, j])
                    elif lines[j][i] == "Q":
                        # если встретился выход.
                        self.exits_coord.append([i, j])
                    elif lines[j][i] == ".":
                        # если встретился пол.
                        self.floors_coord.append([i, j])
                    elif lines[j][i] == "@":
                        # если встретился персонаж.
                        self.player_coord = [i, j]
                    else:
                        raise ValueError(f'Такого объекта в комнате {room} не существует {i}, {j}, {lines[j][i]}.')
            f.close()

    def delete_coins_and_enemies_in_room_file(self, room):
        """Функция, удаляющая уже собранные монеты, хранящиеся в файле комнаты."""
        # открываем файл комнаты с координатами.
        data = None
        with open(room, 'r') as f:
            data = f.read()
            lines = data.splitlines()
            # для каждой собранной монеты и убитого врага заменяем её значение в файле на пол.
            for coin in self.collected_coins_list:
                lines[coin[1]] = lines[coin[1]][:coin[0]] + "." + lines[coin[1]][coin[0] + 1:]
            for enemy in self.killed_enemies_list:
                lines[enemy[1]] = lines[enemy[1]][:enemy[0]] + "." + lines[enemy[1]][enemy[0] + 1:]
            data = "\n".join(lines)
            f.close()
        with open(room, 'w') as f:
            f.write(data)
            f.close()

    def new(self, room, spawn_door="default"):
        """Начало новой игры с созданием всех спрайтов."""
        self.playing = True
        # обьявление массивов для запоминания координат каждого из объектов.
        self.wall_coords = []
        self.doors_coord = []
        self.coins_coord = []
        self.traps_coord = []
        self.darks_coord = []
        self.enemies_coord = []
        self.exits_coord = []
        self.floors_coord = []

        # вызываем функцию, считывающую все объекты, хранящиеся в файле комнаты
        self.read_room_file(room)

        # для каждого массива зададим группу спрайтов,
        # в которой будут хранится объекты определенного класса
        self.all_sprite_list = pygame.sprite.Group()

        # Группа спрайтов класса Стена
        self.wall_list = pygame.sprite.Group()
        for coord in self.wall_coords:
            wall = Wall(self, coord[0], coord[1])
            self.wall_list.add(wall)
            self.all_sprite_list.add(wall)

        # Группа спрайтов класса Дверь
        self.doors_list = pygame.sprite.Group()
        for coord in self.doors_coord:
            door = Door(self, coord[0], coord[1])
            self.doors_list.add(door)
            self.all_sprite_list.add(door)

        # Группа спрайтов класса Пол
        self.floors_list = pygame.sprite.Group()
        for coord in self.floors_coord:
            floor = Floor(self, coord[0], coord[1])
            self.floors_list.add(floor)
            self.all_sprite_list.add(floor)

        # Группа спрайтов класса Выход
        self.exits_list = pygame.sprite.Group()
        for coord in self.exits_coord:
            exit = Exit(self, coord[0], coord[1])
            self.exits_list.add(exit)
            self.all_sprite_list.add(exit)

        # Группа спрайтов класса Монета
        self.coins_list = pygame.sprite.Group()
        for coord in self.coins_coord:
            coin = Coin(self, coord[0], coord[1])
            self.coins_list.add(coin)
            floor = Floor(self, coord[0], coord[1])
            self.all_sprite_list.add(floor)
            self.all_sprite_list.add(coin)

        # Группа спрайтов класса Ловушка
        self.traps_list = pygame.sprite.Group()
        for coord in self.traps_coord:
            trap = Trap(self, coord[0], coord[1])
            floor = Floor(self, coord[0], coord[1])
            self.all_sprite_list.add(floor)
            self.traps_list.add(trap)
            self.all_sprite_list.add(trap)

        # Группа спрайтов класса Враг
        self.enemies_list = pygame.sprite.Group()
        for coord in self.enemies_coord:
            floor = Floor(self, coord[0], coord[1])
            enemy = Enemy(self, coord[0], coord[1])
            self.enemies_list.add(enemy)
            self.all_sprite_list.add(floor)
            self.all_sprite_list.add(enemy)

        # Группа спрайтов класса Темнота
        self.darks_list = pygame.sprite.Group()
        for coord in self.darks_coord:
            dark = Dark(self, coord[0], coord[1])
            self.darks_list.add(dark)
            self.all_sprite_list.add(dark)

        # Спрайт класса Персонаж
        if spawn_door == "left_door":
            left_door_x = self.doors_coord[0][0]
            left_door_y = self.doors_coord[0][1]
            for door in self.doors_coord:
                if door[0] < left_door_x:
                    left_door_x = door[0]
                    left_door_y = door[1]
            self.player = Player(self, left_door_x + 1, left_door_y)
        elif spawn_door == "up_door":
            up_door_x = self.doors_coord[0][0]
            up_door_y = self.doors_coord[0][1]
            for door in self.doors_coord:
                if door[1] < up_door_y:
                    up_door_x = door[0]
                    up_door_y = door[1]
            self.player = Player(self, up_door_x, up_door_y + 1)
        elif spawn_door == "right_door":
            right_door_x = self.doors_coord[0][0]
            right_door_y = self.doors_coord[0][1]
            for door in self.doors_coord:
                if door[0] > right_door_x:
                    right_door_x = door[0]
                    right_door_y = door[1]
            self.player = Player(self, right_door_x - 1, right_door_y)
        elif spawn_door == "down_door":
            down_door_x = self.doors_coord[0][0]
            down_door_y = self.doors_coord[0][1]
            for door in self.doors_coord:
                if door[1] > down_door_y:
                    down_door_x = door[0]
                    down_door_y = door[1]
            self.player = Player(self, down_door_x, down_door_y - 1)
        elif spawn_door == "default":
            self.player = Player(self, self.player_coord[0], self.player_coord[1])
        floor = Floor(self, self.player_coord[0], self.player_coord[1])
        self.all_sprite_list.add(floor)
        self.all_sprite_list.add(self.player)

        # Передача всех спрайтов разных классов в класс Персонаж.
        self.player.walls = self.wall_list
        self.player.exits = self.exits_list
        self.player.doors = self.doors_list
        self.player.coins = self.coins_list
        self.player.traps = self.traps_list
        self.player.darks = self.darks_list
        self.player.enemies = self.enemies_list

    def events(self):
        """Отлавливание событий в Игровом цикле."""
        for event in pygame.event.get():

            # Проверка на завершение (выключение) игры.
            if event.type is pygame.QUIT:
                self.playing = False
                self.running = False

            # Проверка на погиб ли игрок.
            if not self.player.alive:
                self.playing = False
                if ERROR_LEVEL == 1:
                    print("changed playing on False because alive is False")

            # Проверка на переход в новую комнату.
            if self.player.go_down:
                self.playing = False
            if self.player.go_left:
                self.playing = False
            if self.player.go_right:
                self.playing = False
            if self.player.go_up:
                self.playing = False
            if self.player.win:
                self.playing = False

    def update(self):
        """Обновление спрайтов в Игровом цикле."""
        global ERROR_TIME
        ERROR_TIME += 1
        if ERROR_LEVEL == 1:
            print("TIME is ", ERROR_TIME, "and win flag is", self.player.win)
        self.all_sprite_list.update()
        if menu.lifes >= 3 * menu.MAX_LIFE / 4:
            self.player_life_color = GREEN
        elif menu.lifes >= menu.MAX_LIFE / 2:
            self.player_life_color = YELLOW
        else:
            self.player_life_color = RED

    def draw(self):
        """Прорисовка спрайтов и фона окна в Игровом цикле."""
        self.screen.fill(BLACK)
        self.all_sprite_list.draw(self.screen)
        # Проверка на конец времени атаки.
        if self.player.attacking:
            if pygame.time.get_ticks() - self.player.attacking_time <= 125:    # время в ms.
                if self.player.facing == "left":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[0], 90)
                elif self.player.facing == "down":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[0], 180)
                elif self.player.facing == "right":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[0], 270)
                else:
                    rotated_image = self.player.attackloop[0]
                self.screen.blit(rotated_image,
                                 (self.player.attackrect.x, self.player.attackrect.y))
            elif pygame.time.get_ticks() - self.player.attacking_time <= 250:
                if self.player.facing == "left":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[1], 90)
                elif self.player.facing == "down":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[1], 180)
                elif self.player.facing == "right":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[1], 270)
                else:
                    rotated_image = self.player.attackloop[1]
                self.screen.blit(rotated_image,
                                 (self.player.attackrect.x, self.player.attackrect.y))
            elif pygame.time.get_ticks() - self.player.attacking_time <= 375:
                if self.player.facing == "left":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[2], 90)
                elif self.player.facing == "down":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[2], 180)
                elif self.player.facing == "right":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[2], 270)
                else:
                    rotated_image = self.player.attackloop[2]
                self.screen.blit(rotated_image,
                                 (self.player.attackrect.x, self.player.attackrect.y))
            else:
                if self.player.facing == "left":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[3], 90)
                elif self.player.facing == "down":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[3], 180)
                elif self.player.facing == "right":
                    rotated_image = pygame.transform.rotate(self.player.attackloop[3], 270)
                else:
                    rotated_image = self.player.attackloop[3]
                self.screen.blit(rotated_image,
                                 (self.player.attackrect.x, self.player.attackrect.y))
        pygame.draw.rect(self.screen, GREY, (5, 5, 104, 24), 3)
        pygame.draw.rect(self.screen, self.player_life_color,
                         (7, 7, round(menu.lifes * 100 / menu.MAX_LIFE), 20))
        self.clock.tick(FPS)
        # После того как всё нарисовали, отобразим на экране всё сразу.
        pygame.display.flip()

    def main(self):
        """Игровой цикл."""
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self, coins, playerName):
        """Финальный экран в случае поражения."""
        self.DieScreen = menu.DieScreen(BLUE,
                                        "Arial",
                                        os.path.abspath(os.path.dirname(sys.argv[0])) + "/Screens/intro.png",
                                        WHITE,
                                        SCREEN_WIDTH,
                                        SCREEN_HEIGHT,
                                        os.path.abspath(os.path.dirname(sys.argv[0])) + "/Screens/game_over.png",
                                        coins,
                                        playerName)
        self.DieScreen.DieMenu.mainloop(self.screen)

    def intro_screen(self):
        """Начальный экран с приветсвием, правилами и управлением."""
        pass

    def win_screen(self, coins, playerName):
        """Финальный экран в случае победы."""
        self.WinScreen = menu.WinScreen(BLUE,
                                        "Arial",
                                        os.path.abspath(os.path.dirname(sys.argv[0])) + "/Screens/intro.png",
                                        WHITE,
                                        SCREEN_WIDTH,
                                        SCREEN_HEIGHT,
                                        os.path.abspath(os.path.dirname(sys.argv[0])) + "/Screens/win_screen.png",
                                        coins,
                                        playerName)
        self.WinScreen.WinMenu.mainloop(self.screen)
