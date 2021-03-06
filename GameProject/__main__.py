"""
Семестровый проект по спецкурсу «Совместная разработка приложений на Python3».

Roguelike 2D-игра
"""
import os
import pygame
import sys
import traceback
import shutil
testdir = os.path.dirname(__file__)
srcdir = '../GameProject'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
from base import Game
sys.path.remove(os.path.abspath(os.path.join(testdir, srcdir)))

# Объявление карты игры
map_list = []

# Объявление позиции начальной комнаты
CURRENT_MAP_POSITION = [2, 1]
CURRENT_ROOM = []

# Объявление глобальной переменной для подсчета монет
all_collected_coins = 0
myPath = os.path.abspath(os.path.dirname(sys.argv[0]))
if myPath[-12:] != "/GameProject":
    myPath += "/GameProject"
# Считывание из общей директории карты комнат
with open(myPath + '/RoomsInDungeon/map.in', 'r') as f:
    map = f.read()
    map_list = map.splitlines()

# Объявление начальной комнаты
if __name__ == "__main__":
    cached_dir = ""
    try:
        g = Game()
        g.menu.menu.mainloop(g.screen)
        playerName = g.playerName
        path = os.getcwd()
        cached_dir = shutil.copytree(str(myPath + "/RoomsInDungeon"),
                                     str(myPath + "/CachedRoomsInDungeon"))
        PATH_TO_ROOMS = myPath + "/CachedRoomsInDungeon/"
        CURRENT_ROOM = PATH_TO_ROOMS + \
            map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
        g.new(CURRENT_ROOM)
        # Основной цикл игры.
        while g.running:
            g.main()
            # Считывание новой комнаты при переходе через двери.
            if g.player.go_down:
                # Если персонаж вошел в нижнюю дверь, поменяй комнату на нижнюю.
                CURRENT_MAP_POSITION[1] += 1
                g.delete_coins_and_enemies_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "up_door")
                continue
            elif g.player.go_left:
                # Если персонаж вошел в левую дверь, поменяй комнату на левую.
                CURRENT_MAP_POSITION[0] -= 1
                g.delete_coins_and_enemies_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "right_door")
                continue
            elif g.player.go_right:
                # Если персонаж вошел в правую дверь, поменяй комнату на правую.
                CURRENT_MAP_POSITION[0] += 1
                g.delete_coins_and_enemies_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "left_door")
                continue
            elif g.player.go_up:
                # Если персонаж вошел в верхнюю дверь, поменяй комнату на верхнюю.
                CURRENT_MAP_POSITION[1] -= 1
                g.delete_coins_and_enemies_in_room_file(CURRENT_ROOM)
                CURRENT_ROOM = PATH_TO_ROOMS + \
                    map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'
                all_collected_coins += g.collected_coins
                g = Game()
                g.new(CURRENT_ROOM, "down_door")
                continue
            # Проверка какой экран конца игры выводить.
            if g.player.win:
                all_collected_coins += g.collected_coins
                g.win_screen(all_collected_coins, playerName)
            else:
                all_collected_coins += g.collected_coins
                g.game_over(all_collected_coins, playerName)
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for i in traceback.format_exception(exc_type, exc_value,
                                            exc_traceback):
            print(i, end="")
    finally:
        # Выход из программы с очисткой памяти.
        pygame.quit()
        try:
            shutil.rmtree(cached_dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        sys.exit()
