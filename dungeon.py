import pygame
import sys
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


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        ''' Создание класса Персонажа с начальными настройками '''
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        ''' инициализация координат персонажа '''
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        ''' инициализация размера персонажа '''
        self.width = TILESIZE
        self.height = TILESIZE

        ''' инициализация скорости персонажа '''
        self.x_change = 0
        self.y_change = 0
        ''' куда смотрит персонаж в данных момент '''
        self.facing = 'down'

        self.walls = None
        self.coins = None
        self.traps = None
        self.darks = None
        self.doors = None
        self.exits = None

        ''' Жив ли персонаж? '''
        self.alive = True
        ''' Выиграл ли персонаж? '''
        self.win = False

        down1 = pygame.transform.scale(pygame.image.load(
            'down1.png'), (PLAYER_TILESIZE, PLAYER_TILESIZE)).convert_alpha()

        self.image = down1
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        ''' Объявления основных механик и их изменение во времени'''
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
        if self.rect.y < 0:
            self.rect.y = SCREEN_HEIGHT

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        '''
            Функция по обработке нажатия клавиш:
            pygame.K_w (клавиша "W") -- появляется скорость персонажа по y координате. //
            // Она направлена вверх
            pygame.K_a (клавиша "A") -- появляется скорость персонажа по x координате. //
            // Она направлена влево
            pygame.K_s (клавиша "S") -- появляется скорость персонажа по y координате. //
            // Она направлена вниз
            pygame.K_D (клавиша "D") -- появляется скорость персонажа по x координате. //
            // Она направлена вправо
        '''
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
    '''
        Описание класса:
        Персонаж не может пройти сквозь стену
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Стена с начальными настройками '''
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        ''' инициализация координат стены '''
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        ''' инициализация размера стены '''
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.transform.scale2x(pygame.image.load('wall.png').convert())
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Door(pygame.sprite.Sprite):
    '''
        Описание класса:
        Персонаж переходит в другую комнату, соприкасаясь с дверью
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Дверь с начальными настройками '''
        self.game = game
        self._layer = PLAYER_LAYER
        super().__init__()

        ''' инициализация координат двери '''
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        ''' инициализация размера двери '''
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.transform.scale2x(pygame.image.load('door.png').convert())
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Exit(pygame.sprite.Sprite):
    '''
        Описание класса:
        Персонаж выигрывает, соприкасаясь с выходом
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Выход '''
        pass


class Floor(pygame.sprite.Sprite):
    '''
        Описание класса:
        Персонаж может ходить по полу
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Пол с начальными настройками '''
        self.game = game
        self._layer = FLOOR_LAYER
        super().__init__()

        ''' инициализация координат пола '''
        self.x = x * TILESIZE
        self.y = y * TILESIZE

        ''' инициализация размера пола '''
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.transform.scale2x(pygame.image.load('floor.png').convert())
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


class Dark(pygame.sprite.Sprite):
    '''
        Описание класса:
        При попадании персонажа в темноту персонаж погибает
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Темнота '''
        pass


class Coin(pygame.sprite.Sprite):
    '''
        Описание класса:
        При соприкосновении персонажа с монетой она подбирается
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Монета '''
        pass


class Trap(pygame.sprite.Sprite):
    '''
        Описание класса:
        При попадании персонажа в ловушку персонаж погибает
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Ловушки '''
        pass

    def update(self):
        ''' Объявления основных механик и их изменение во времени'''
        pass


class Enemy(pygame.sprite.Sprite):
    '''
        Описание класса:
        При соприкосновении персонажа с врагом персонаж погибает
    '''

    def __init__(self, game, x, y):
        ''' Создание класса Врага '''
        pass

    def update(self):
        ''' Объявления основных механик и их изменение во времени'''
        pass


class Game:
    def __init__(self):
        ''' Создание класса Игра с настройкой размера окна игры '''
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font('Arial', 32)
        self.running = True

    def new(self, room='K.in'):
        ''' Начало новой игры с созданием всех спрайтов '''
        self.playing = True
        ''' обьявление массивов для запоминания координат каждого из объектов '''
        wall_coords = []
        doors_coord = []
        coins_coord = []
        traps_coord = []
        darks_coord = []
        enemies_coord = []
        exits_coord = []
        floors_coord = []
        ''' открываем файл комнаты с координатами '''
        with open(room, 'r') as f:
            data = f.read()
            lines = data.splitlines()
            ''' для каждой считанной координаты ставим в соответсвие объект игры '''
            for j in range(0, 19):
                for i in range(0, 25):
                    if lines[j][i] == "#":
                        ''' если встретилась стена '''
                        wall_coords.append([i, j])
                    elif lines[j][i] == "m":
                        ''' если встретилась монета '''
                        coins_coord.append([i, j])
                    elif lines[j][i] == "x":
                        ''' если встретилась дверь '''
                        doors_coord.append([i, j])
                    elif lines[j][i] == "T":
                        ''' если встретилась ловушка '''
                        traps_coord.append([i, j])
                    elif lines[j][i] == " ":
                        ''' если встретилась темнота '''
                        darks_coord.append([i, j])
                    elif lines[j][i] == "e":
                        ''' если встретился враг '''
                        enemies_coord.append([i, j])
                    elif lines[j][i] == "Q":
                        ''' если встретился выход '''
                        exits_coord.append([i, j])
                    elif lines[j][i] == ".":
                        ''' если встретилась пол '''
                        floors_coord.append([i, j])
                    elif lines[j][i] == "@":
                        ''' если встретилась персонаж '''
                        player_coord = [i, j]

        '''
            для каждого массива зададим группу спрайтов,
            в которй будду хранится объекты определенного класса
        '''
        self.all_sprite_list = pygame.sprite.Group()
        '''
            Группа спрайтов класса Стена
        '''
        self.wall_list = pygame.sprite.Group()
        for coord in wall_coords:
            wall = Wall(self, coord[0], coord[1])
            self.wall_list.add(wall)
            self.all_sprite_list.add(wall)
        '''
            Группа спрайтов класса Дверь
        '''
        self.doors_list = pygame.sprite.Group()
        for coord in doors_coord:
            door = Door(self, coord[0], coord[1])
            self.doors_list.add(door)
            self.all_sprite_list.add(door)
        '''
            Группа спрайтов класса Пол
        '''
        self.floors_list = pygame.sprite.Group()
        for coord in floors_coord:
            floor = Floor(self, coord[0], coord[1])
            self.floors_list.add(floor)
            self.all_sprite_list.add(floor)
        '''
            Спрайт класса Персонаж
        '''
        self.player = Player(self, player_coord[0], player_coord[1])
        floor = Floor(self, player_coord[0], player_coord[1])
        self.all_sprite_list.add(floor)
        self.all_sprite_list.add(self.player)
        self.player.walls = self.wall_list

    def events(self):
        ''' Отлавливание событий в Игровом цикле '''
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        ''' Обновление спрайтов в Игровом цикле '''
        global ERROR_TIME
        ERROR_TIME += 1
        if ERROR_LEVEL == 1:
            print("TIME is ", ERROR_TIME, "and win flag is", self.player.win)
        self.all_sprite_list.update()

    def draw(self):
        ''' Прорисовка спрайтов и фона окна в Игровом цикле '''
        self.screen.fill(BLACK)
        self.all_sprite_list.draw(self.screen)
        self.clock.tick(FPS)
        ''' После того как всё нарисовали, отобразим на экране всё сразу'''
        pygame.display.flip()

    def main(self):
        ''' Игровой цикл '''
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        ''' Финальный экран в случае поражения '''
        pass

    def intro_screen(self):
        ''' Начальный экран с приветсвием, правилами и управлением '''
        pass

    def win_screen(self):
        ''' Финальный экран в случае победы или поражения '''
        pass


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

''' Выход из программы с очисткой памяти '''
pygame.quit()
sys.exit()
