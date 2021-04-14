"""
Семестровый проект по спецкурсу «Совместная разработка приложений на Python3».

Roguelike 2D-игра
"""
import pygame
import sys
from base import Player, Wall, Door, Exit, Floor, Dark, Coin, Trap, Enemy, Game

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
CURRENT_ROOM = map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'


def main():
    """Инициализация переменной типа Игра."""
    g = Game()
    g.intro_screen()
    g.new(CURRENT_ROOM)
    """ Основной цикл игры."""
    while g.running:
        g.main()
        if g.player.win:
            g.win_screen()
        else:
            g.game_over()


if __name__ == "__main__":
    main()


""" Выход из программы с очисткой памяти."""
pygame.quit()
sys.exit()
