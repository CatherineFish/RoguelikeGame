"""
Семестровый проект по спецкурсу «Совместная разработка приложений на Python3».

Roguelike 2D-игра
"""
import pygame
import sys
from base import Player, Wall, Door, Exit, Floor, Dark, Coin, Trap, Enemy, Game
import unittest

# import time

"""
    Объявление карты игры
"""
map_list = []
"""
    Объявление позиции начальной комнаты
"""
CURRENT_MAP_POSITION = [2, 1]
CURRENT_ROOM = []


"""
    Считывание из общей директории карты комнат
"""

with open('map.in', 'r') as f:
    map = f.read()
    map_list = map.splitlines()
"""
    Объявление начальной комнаты
"""
PATH_TO_ROOMS = "rooms_in_dungeon/"
CURRENT_ROOM = PATH_TO_ROOMS + map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'


def main(PATH_TO_ROOMS="rooms_in_dungeon/"):
    """Инициализация переменной типа Игра."""
    global CURRENT_ROOM
    g = Game()
    g.menu.menu.mainloop(g.screen)
    g.new(CURRENT_ROOM)
    """Основной цикл игры."""
    while g.running:
        g.main()
        """Считывание новой комнаты при переходе через двери."""
        if g.player.go_down:
            """Если персонаж вошел в нижнюю дверь, поменяй комнату на нижнюю."""
            CURRENT_MAP_POSITION[1] += 1
            CURRENT_ROOM = PATH_TO_ROOMS + \
                map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
            g = Game()
            g.new(CURRENT_ROOM, "up_door")
            continue
        elif g.player.go_left:
            """Если персонаж вошел в левую дверь, поменяй комнату на левую."""
            CURRENT_MAP_POSITION[0] -= 1
            CURRENT_ROOM = PATH_TO_ROOMS + \
                map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
            g = Game()
            g.new(CURRENT_ROOM, "right_door")
            continue
        elif g.player.go_right:
            """Если персонаж вошел в правую дверь, поменяй комнату на правую."""
            CURRENT_MAP_POSITION[0] += 1
            CURRENT_ROOM = PATH_TO_ROOMS + \
                map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
            g = Game()
            g.new(CURRENT_ROOM, "left_door")
            continue
        elif g.player.go_up:
            """Если персонаж вошел в верхнюю дверь, поменяй комнату на верхнюю."""
            CURRENT_MAP_POSITION[1] -= 1
            CURRENT_ROOM = PATH_TO_ROOMS + \
                map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
            g = Game()
            g.new(CURRENT_ROOM, "down_door")
            continue
        """Проверка какой экран конца игры выводить."""
        if g.player.win:
            g.win_screen()
        else:
            g.game_over()


if __name__ == "__main__":
    main(PATH_TO_ROOMS)


""" Выход из программы с очисткой памяти."""
pygame.quit()
sys.exit()
