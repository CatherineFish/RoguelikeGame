"""
Базовый модуль Roguelike 2D-игры.

Описывает набор базовых классов

:copyright: (c) 2021 by Larin Andrey and Chekhonina Ekaterina
:license: MIT, see COPYING for more details.
"""

import pygame
import sys
import menu
import pygame_menu
import gettext
import unittest

gettext.install("click", ".", names=("ngettext",))


"""Объявление глобальных переменны."""
"""
    Объявление уровня дебага, для отладки ошибок,
    по умолчанию установлен в 0
    (без вывода сообщений об ошибках)
"""
ERROR_TIME = 0
ERROR_LEVEL = 0
"""
    Объявление глобальных цветов
"""
PINK = (221, 160, 221)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (29, 32, 76)
"""
    Объявление глобального размера игрового окна
"""
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608
"""
    Объявление глобального размера игровой ячейки (игрового "пикселя")
"""
TILESIZE = 32
"""
    Объявление глобального размера персонажа игры
"""
PLAYER_TILESIZE = 30
"""
    Объявление глобальной кадровой частоты
"""
FPS = 60
"""
    Объявление глобальных уровней прорисовки спрайтов
    спрайт игрока выше спрайта пола
"""
PLAYER_LAYER = 2
FLOOR_LAYER = 1
"""
    Объявление глобальных уровней прорисовки спрайтов
"""
PLAYER_SPEED = 3
"""
    Объявление глобальных переменных
    для отслеживания спрайтов с анимациями
"""
animation_count = 0
animation_count_slime = 0
animation_count_trap = 0


class Player(pygame.sprite.Sprite):
    """Базовый класс, задающий персонажа."""

    def __init__(self, game, x, y):
        """Создание класса Персонажа с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        """Инициализация координат персонажа."""
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        """Инициализация размера персонажа."""
        self.width = TILESIZE
        self.height = TILESIZE

        """Инициализация скорости персонажа."""
        self.x_change = 0
        self.y_change = 0
        """Куда смотрит персонаж в данных момент."""
        self.facing = 'down'

        """Инициализация списков со спрайтами других классов."""
        self.walls = None
        self.coins = None
        self.traps = None
        self.darks = None
        self.doors = None
        self.exits = None

        """Инициализация флагов пермещений между комнатами."""
        self.go_up = False
        self.go_down = False
        self.go_right = False
        self.go_left = False

        """Жив ли персонаж?"""
        self.alive = True
        """Выиграл ли персонаж?"""
        self.win = False

        """Инициализация картинки для персонаж."""
        down1 = pygame.transform.scale(pygame.image.load(
            'down1.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()
        self.game.png_names.add("down1.png")
        self.image = down1

        """Инциализация rect для заданной картинки."""
        self.rect = self.image.get_rect()
        self.rect = pygame.rect.Rect((0, 0), (self.width - 12, self.height - 2))

        """Инциализация colliderect для описания коллизий."""
        self.collideRect = pygame.rect.Rect((0, 0), (self.width - 28, 8))
        self.rect.x = self.x
        self.rect.y = self.y

        """Сolliderect будет совпадать с нашей rect картинкой по середине нижней грани (ногам)."""
        self.collideRect.midbottom = self.rect.midbottom

    def update(self):
        """Объявления основных механик и их изменение во времени."""
        """будем изменять глобальную переменную количества собранных монет"""

        self.movement()

        """Движение по оси x и проверка коллизий со стенами."""
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

        """Движение по оси y и проверка коллизий со стенами."""
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

        """Проверка коллизий с дверьми."""
        rect_list = []
        for sprite in self.doors:
            rect_list.append(sprite.rect)
        doors_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        for door_find in doors_hit_list:
            """
            Определение перехода в следующую комнату:
            go_down – переход в комнату ниже текущей
            go_left – переход в комнату левее текущей
            go_right – переход в комнату правее текущей
            go_up – переход в комнату выше текущей
            """
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

        """Проверка коллизий с монетами."""
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

        """Проверка коллизий с монетами."""
        rect_list = []
        for sprite in self.darks:
            rect_list.append(sprite.rect)
        dark_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        if len(dark_hit_list) > 0:
            self.alive = False

        """Проверка коллизий с выходом."""
        rect_list = []
        for sprite in self.exits:
            rect_list.append(sprite.rect)
        exit_hit_list = pygame.Rect.collidelistall(self.collideRect, rect_list)
        """Выставление флага победы на True"""
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


class Wall(pygame.sprite.Sprite):
    """
    Описание класса.

    Персонаж не может пройти сквозь стену
    """

    def __init__(self, game, x, y):
        """Создание класса Стена с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        """инициализация координат стены."""
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        """инициализация размера стены."""
        self.width = TILESIZE
        self.height = TILESIZE

        """инициализация картинки для стены."""
        self.image = pygame.transform.scale2x(pygame.image.load('white_wall.png').convert())
        self.game.png_names.add('white_wall.png')

        """Инциализация rect для заданной картинки."""
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Door(pygame.sprite.Sprite):
    """
    Описание класса.

    Персонаж переходит в другую комнату, соприкасаясь с дверью
    """

    def __init__(self, game, x, y):
        """Создание класса Дверь с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        """инициализация координат двери."""
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        """инициализация размера двери."""
        self.width = TILESIZE
        self.height = TILESIZE

        """инициализация картинки для двери."""
        self.image = pygame.transform.scale2x(pygame.image.load('white_door.png').convert())
        self.game.png_names.add('white_door.png')

        """Инциализация rect для заданной картинки."""
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Exit(pygame.sprite.Sprite):
    """
    Описание класса.

    Персонаж выигрывает, соприкасаясь с выходом
    """

    def __init__(self, game, x, y):
        """Создание класса Выход."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        """инициализация координат выхода."""
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        """инициализация размера выхода."""
        self.width = TILESIZE
        self.height = TILESIZE

        """инициализация картинки для выхода."""
        self.image = pygame.transform.scale2x(pygame.image.load('white_exit.png').convert())
        self.game.png_names.add('white_exit.png')

        """Инциализация rect для заданной картинки."""
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Floor(pygame.sprite.Sprite):
    """
    Описание класса.

    Персонаж может ходить по полу
    """

    def __init__(self, game, x, y):
        """Создание класса Пол с начальными настройками."""
        self.game = game
        self._layer = FLOOR_LAYER
        super().__init__()

        """инициализация координат пола."""
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        """инициализация размера пола."""
        self.width = TILESIZE
        self.height = TILESIZE

        """инициализация картинки для пола."""
        self.image = pygame.transform.scale2x(pygame.image.load('white_floor.png').convert())
        self.game.png_names.add('white_floor.png')

        """Инциализация rect для заданной картинки."""
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Dark(pygame.sprite.Sprite):
    """
    Описание класса.

    При попадании персонажа в темноту персонаж погибает
    """

    def __init__(self, game, x, y):
        """Создание класса Темнота с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        """инициализация координат темноты."""
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        """инициализация размера темноты."""
        self.width = TILESIZE
        self.height = TILESIZE

        """инициализация картинки для темноты."""
        self.image = pygame.transform.scale2x(pygame.image.load('dark.png').convert())
        self.game.png_names.add('dark.png')

        """Инциализация rect для заданной картинки."""
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Coin(pygame.sprite.Sprite):
    """
    Описание класса.

    При соприкосновении персонажа с монетой она подбирается
    """

    def __init__(self, game, x, y):
        """Создание класса Монета с начальными настройками."""
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        """инициализация координат монеты."""
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        """инициализация размера монеты."""
        self.width = TILESIZE
        self.height = TILESIZE

        """инициализация картинки длsя монеты."""
        self.image = pygame.image.load('loot_gold.png').convert_alpha()
        self.game.png_names.add('loot_gold.png')

        """Инциализация rect для заданной картинки."""
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Trap(pygame.sprite.Sprite):
    """
    Описание класса.

    При попадании персонажа в ловушку персонаж погибает
    """

    def __init__(self, game, x, y):
        """Создание класса Ловушк."""
        pass

    def update(self):
        """Объявления основных механик и их изменение во времени."""
        pass


class Enemy(pygame.sprite.Sprite):
    """
    Описание класса.

    При соприкосновении персонажа с врагом персонаж погибает
    """

    def __init__(self, game, x, y):
        """Создание класса Враг."""
        pass

    def update(self):
        """Объявления основных механик и их изменение во времени."""
        pass


class Game:
    """Основная игра, реагирующая на различные игровые события."""
    png_names = set()
    collected_coins = 0

    def __init__(self):
        """Создание класса Игра с настройкой размера окна игры."""
        pygame.init()
        self.collected_coins_list = []
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True
        self.menu = menu.MyMenu(BLUE,
                                "Arial",
                                "intro.png",
                                WHITE,
                                SCREEN_WIDTH,
                                SCREEN_HEIGHT)
        self.png_names.add("intro.png")

    def read_room_file(self, room):
        """Функция, считывающая все объекты, хранящиеся в файле комнаты"""
        """открываем файл комнаты с координатам."""
        with open(room, 'r') as f:
            data = f.read()
            lines = data.splitlines()
            """для каждой считанной координаты ставим в соответсвие объект игры."""
            for j in range(0, 19):
                for i in range(0, 25):
                    if lines[j][i] == "#":
                        """если встретилась стена."""
                        self.wall_coords.append([i, j])
                    elif lines[j][i] == "m":
                        """если встретилась монета."""
                        self.coins_coord.append([i, j])
                    elif lines[j][i] == "x":
                        """если встретилась дверь."""
                        self.doors_coord.append([i, j])
                    elif lines[j][i] == "T":
                        """если встретилась ловушк."""
                        self.traps_coord.append([i, j])
                    elif lines[j][i] == " ":
                        """если встретилась темнота."""
                        self.darks_coord.append([i, j])
                    elif lines[j][i] == "e":
                        """если встретился враг."""
                        self.enemies_coord.append([i, j])
                    elif lines[j][i] == "Q":
                        """если встретился выход."""
                        self.exits_coord.append([i, j])
                    elif lines[j][i] == ".":
                        """если встретился пол."""
                        self.floors_coord.append([i, j])
                    elif lines[j][i] == "@":
                        """если встретился персонаж."""
                        self.player_coord = [i, j]
                    else:
                        raise ValueError(f'Такого объекта в комнате {room} не существует.')
            f.close()

    def delete_coins_in_room_file(self, room):
        """Функция, удаляющая уже собранные монеты, хранящиеся в файле комнаты"""
        """открываем файл комнаты с координатами."""
        data = None
        with open(room, 'r') as f:
            data = f.read()
            lines = data.splitlines()
            """для каждой собранной монет заменяем её значение в файле на пол."""
            for coin in self.collected_coins_list:
                lines[coin[1]] = lines[coin[1]][:coin[0]] + "." + lines[coin[1]][coin[0] + 1:]
            data = "\n".join(lines)
            f.close()
        with open(room, 'w') as f:
            f.write(data)
            f.close()

    def new(self, room, spawn_door="default"):
        """Начало новой игры с созданием всех спрайтов."""
        self.playing = True
        """обьявление массивов для запоминания координат каждого из объектов."""
        self.wall_coords = []
        self.doors_coord = []
        self.coins_coord = []
        self.traps_coord = []
        self.darks_coord = []
        self.enemies_coord = []
        self.exits_coord = []
        self.floors_coord = []

        """вызываем функцию, считывающую все объекты, хранящиеся в файле комнаты"""
        self.read_room_file(room)

        """
            для каждого массива зададим группу спрайтов,
            в которой будут хранится объекты определенного класса
        """
        self.all_sprite_list = pygame.sprite.Group()
        """
            Группа спрайтов класса Стена
        """
        self.wall_list = pygame.sprite.Group()
        for coord in self.wall_coords:
            wall = Wall(self, coord[0], coord[1])
            self.wall_list.add(wall)
            self.all_sprite_list.add(wall)
        """
            Группа спрайтов класса Дверь
        """
        self.doors_list = pygame.sprite.Group()
        for coord in self.doors_coord:
            door = Door(self, coord[0], coord[1])
            self.doors_list.add(door)
            self.all_sprite_list.add(door)
        """
            Группа спрайтов класса Пол
        """
        self.floors_list = pygame.sprite.Group()
        for coord in self.floors_coord:
            floor = Floor(self, coord[0], coord[1])
            self.floors_list.add(floor)
            self.all_sprite_list.add(floor)
        """
            Группа спрайтов класса Выход
        """
        self.exits_list = pygame.sprite.Group()
        for coord in self.exits_coord:
            exit = Exit(self, coord[0], coord[1])
            self.exits_list.add(exit)
            self.all_sprite_list.add(exit)
        """
            Группа спрайтов класса Монета
        """
        self.coins_list = pygame.sprite.Group()
        for coord in self.coins_coord:
            coin = Coin(self, coord[0], coord[1])
            self.coins_list.add(coin)
            floor = Floor(self, coord[0], coord[1])
            self.all_sprite_list.add(floor)
            self.all_sprite_list.add(coin)
        """
            Группа спрайтов класса Темнота
        """
        self.darks_list = pygame.sprite.Group()
        for coord in self.darks_coord:
            dark = Dark(self, coord[0], coord[1])
            self.darks_list.add(dark)
            self.all_sprite_list.add(dark)
        """
            Спрайт класса Персонаж
        """
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

        """Передача всех спрайтов разных классов в класс Персонаж."""
        self.player.walls = self.wall_list
        self.player.exits = self.exits_list
        self.player.doors = self.doors_list
        self.player.coins = self.coins_list
        self.player.darks = self.darks_list

    def events(self):
        """Отлавливание событий в Игровом цикле."""
        for event in pygame.event.get():
            """
                Проверка на завершение (выключение) игры.
            """
            if event.type is pygame.QUIT:
                self.playing = False
                self.running = False
            """
                Проверка на погиб ли игрок.
            """
            if not self.player.alive:
                self.playing = False
                if ERROR_LEVEL == 1:
                    print("changed playing on False because alive is False")
            """
                Проверка на переход в новую комнату.
            """
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

    def draw(self):
        """Прорисовка спрайтов и фона окна в Игровом цикле."""
        self.screen.fill(BLACK)
        self.all_sprite_list.draw(self.screen)
        # print(self.png_names)
        self.clock.tick(FPS)
        """После того как всё нарисовали, отобразим на экране всё сразу."""
        pygame.display.flip()

    def main(self):
        """Игровой цик."""
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        """Финальный экран в случае поражения."""
        pass

    def intro_screen(self):
        """Начальный экран с приветсвием, правилами и управлением."""
        pass

    def win_screen(self):
        """Финальный экран в случае победы."""
        pass
