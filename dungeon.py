"""
Семестровый проект по спецкурсу «Совместная разработка приложений на Python3».

Roguelike 2D-игра
"""
import pygame
import sys
import traceback
from base import Player, Wall, Door, Exit, Floor, Dark, Coin, Trap, Enemy, Game
import unittest
import os
import shutil

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
    Объявление глобальной переменной для подсчета монет
"""
all_collected_coins = 0

"""
    Считывание из общей директории карты комнат
"""

with open('map.in', 'r') as f:
    map = f.read()
    map_list = map.splitlines()
"""
    Объявление начальной комнаты
"""


if __name__ == "__main__":
    cached_dir = ""
    try:
        g = Game()
        g.menu.menu.mainloop(g.screen)
        path = os.getcwd()
        cached_dir = shutil.copytree(str(path + "/rooms_in_dungeon"),
                                     str(path + "/cached_rooms_in_dungeon"))
        PATH_TO_ROOMS = "cached_rooms_in_dungeon/"
        CURRENT_ROOM = PATH_TO_ROOMS + \
            map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
        g.new(CURRENT_ROOM)
        """Основной цикл игры."""
        while g.running:
            g.main()
            """Считывание новой комнаты при переходе через двери."""
            if g.player.go_down:
                """Если персонаж вошел в нижнюю дверь, поменяй комнату на нижнюю."""
                CURRENT_MAP_POSITION[1] += 1
                g.delete_coins_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "up_door")
                continue
            elif g.player.go_left:
                """Если персонаж вошел в левую дверь, поменяй комнату на левую."""
                CURRENT_MAP_POSITION[0] -= 1
                g.delete_coins_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "right_door")
                continue
            elif g.player.go_right:
                """Если персонаж вошел в правую дверь, поменяй комнату на правую."""
                CURRENT_MAP_POSITION[0] += 1
                g.delete_coins_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "left_door")
                continue
            elif g.player.go_up:
                """Если персонаж вошел в верхнюю дверь, поменяй комнату на верхнюю."""
                CURRENT_MAP_POSITION[1] -= 1
                g.delete_coins_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "down_door")
                continue
            """Проверка какой экран конца игры выводить."""
            if g.player.win:
                all_collected_coins += g.collected_coins
                g.win_screen()
                print("победа, собрано монет:", all_collected_coins)
            else:
                all_collected_coins += g.collected_coins
                g.game_over()
                print("поражение, собрано монет:", all_collected_coins)
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for i in traceback.format_exception(exc_type, exc_value,
                                            exc_traceback):
            print(i, end="")
    finally:
        """ Выход из программы с очисткой памяти."""
        pygame.quit()
        try:
            shutil.rmtree(cached_dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        sys.exit()
