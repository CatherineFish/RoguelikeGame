import pygame
import sys
from base import Player, Wall, Door, Exit, Floor, Dark, Coin, Trap, Enemy, Game

# import time

''' Объявление глобальных переменных '''
'''
    Объявление уровня дебага, для отладки ошибок,
    по умолчанию установлен в 0
    (без вывода сообщений об ошибках)
'''
ERROR_TIME = 0
ERROR_LEVEL = 0
'''
    Объявление глобальных цветов
'''
PINK = (221, 160, 221)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (29, 32, 76)
'''
    Объявление глобального размера игрового окна
'''
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608
'''
    Объявление глобального размера игровой ячейки (игрового "пикселя")
'''
TILESIZE = 32
'''
    Объявление глобального размера персонажа игры
'''
PLAYER_TILESIZE = 30
'''
    Объявление глобальной кадровой частоты
'''
FPS = 60
'''
    Объявление глобальных уровней прорисовки спрайтов
    спрайт игрока выше спрайта пола
'''
PLAYER_LAYER = 2
FLOOR_LAYER = 1
'''
    Объявление глобальных уровней прорисовки спрайтов
'''
PLAYER_SPEED = 3
'''
    Объявление глобальных переменных
    для отслеживания спрайтов с анимациями
'''
animation_count = 0
animation_count_slime = 0
animation_count_trap = 0
'''
    Объявление глобальной переменной для подсчета монет
'''
collected_coins = 0
'''
    Объявление карты игры
'''
map_list = []
'''
    Объявление позиции начальной комнаты
'''
CURRENT_MAP_POSITION = [2, 1]
'''
    Считывание из общей директории карты комнат
'''
with open('map.in', 'r') as f:
    map = f.read()
    map_list = map.splitlines()
'''
    Объявление начальной комнаты
'''
CURRENT_ROOM = map_list[CURRENT_MAP_POSITION[1]][CURRENT_MAP_POSITION[0]] + '.in'


def main():
	''' Инициализация переменной типа Игра '''
	g = Game()
	g.intro_screen()
	g.new(CURRENT_ROOM)
	''' Основной цикл игры '''
	while g.running:
	    g.main()
	    if g.player.win:
	        g.win_screen()
	    else:
	        g.game_over()


if __name__ == "__main__":
    main()


''' Выход из программы с очисткой памяти '''
pygame.quit()
sys.exit()
