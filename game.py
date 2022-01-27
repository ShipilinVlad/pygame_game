import os
import sys
import pygame
import random


class Monster:
    def __init__(self, x, y, m_type, par):
        self.x, self.y, self.nx, self.ny = x, y, 1, 0
        self.x, self.y = 0, cell_width / 2
        self.board_state = board_state
        self.m_type, self.n = m_type, n
        self.width = cell_width
        self.par_x, self.par_y = par, par
        self.coord = [0, 0]
        self.left, self.top = 0, 0
        self.rotate = False
        self.hp = random.choice([3, 4])
        if self.m_type == 'flying':
            monster_image = load_image("eye.png")
        else:
            monster_image = load_image("skell.png")
        self.monster = pygame.sprite.Sprite(moving_sprites)
        self.monster.image = monster_image
        self.monster.rect = self.monster.image.get_rect()
        board_moving.board[0][0] = self.monster
        self.lvl = lvl

    def move(self):
        if self.left + self.coord[0] * self.width <= self.x <= self.left + (self.coord[0] + 1) * self.width and \
                self.top + self.coord[1] * self.width <= self.y <= self.top + (self.coord[1] + 1) * self.width:
            self.x += self.par_x * self.nx
            self.y += self.par_y * self.ny
            if self.rotate and self.x % self.width > self.width // 2 and self.nx == 1:
                self.ny = self.nx - (2 * int(self.rotate == 'left') * self.nx)
                self.nx = 0
                self.rotate = False
            elif self.rotate and self.y % self.width > self.width // 2 and self.ny == 1:
                self.nx = -self.ny - (2 * int(self.rotate == 'left') * -self.ny)
                self.ny = 0
                self.rotate = False
            elif self.rotate and self.x % self.width < self.width // 2 and self.nx == -1:
                self.ny = self.nx - (2 * int(self.rotate == 'left') * self.nx)
                self.nx = 0
                self.rotate = False
            elif self.rotate and self.y % self.width < self.width // 2 and self.ny == -1:
                self.nx = -self.ny - (2 * int(self.rotate == 'left') * -self.ny)
                self.ny = 0
                self.rotate = False
        else:
            board_moving.move(self.coord[0], self.coord[1], self.nx, self.ny, self.monster)
            self.coord[0] += self.nx
            self.coord[1] += self.ny
            if self.coord[0] == self.n - 1 and self.nx == 1 or self.coord[1] == self.n - 1 and self.ny == 1 or\
                    self.coord[0] == 0 and self.nx == -1 or self.coord[1] == 0 and self.ny == -1:
                self.rotate = True
            elif self.lvl[self.coord[1] + self.ny][self.coord[0] + self.nx] not in ('r', 'c'):
                self.rotate = True
            if self.rotate:
                if self.coord[0] == 0 and self.ny == -1 or self.coord[0] == self.n - 1 and self.ny == 1 or\
                        self.coord[1] == 0 and self.nx == 1 or self.coord[1] == self.n - 1 and self.nx == -1:
                    self.rotate = 'right'
                elif self.coord[0] == 0 and self.ny == 1 or self.coord[0] == self.n - 1 and self.ny == -1 or \
                        self.coord[1] == 0 and self.nx == -1 or self.coord[1] == self.n - 1 and self.nx == 1:
                    self.rotate = 'left'
                elif (self.lvl[self.coord[1] + self.nx * ((self.ny - self.nx) ** 2)]
                      [self.coord[0] + self.ny * (-(self.nx - self.ny) ** 2)] not in ('r', 'c')):
                    self.rotate = 'left'
                else:
                    self.rotate = 'right'


class Tower:
    def __init__(self, x, y, t_type):
        self.x, self.y = int(x), int(y)
        self.t_type = t_type
        if self.t_type == 'flying':
            tower_image = load_image("archer.png")
        else:
            tower_image = load_image("wizard.png")
        self.tower = pygame.sprite.Sprite(moving_sprites)
        self.tower.image = tower_image
        self.tower.rect = self.tower.image.get_rect()
        board_moving.board[self.y][self.x] = self.tower

    def damage_monsters_near(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= i + self.y < n and 0 <= j + self.x < n:
                    for monster_to_kill in monsters:
                        if monster_to_kill.coord == [j + self.x, i + self.y]:
                            if monster_to_kill.m_type == self.t_type:
                                monster_to_kill.hp -= 1
                                if self.t_type == 'flying':
                                    pygame.mixer.Sound('data/arrow.wav').play()
                                else:
                                    pygame.mixer.Sound('data/wizard.wav').play()
                                return


class Board:
    def __init__(self):
        self.board = [[0] * n for _ in range(n)]
        self.left = 10
        self.top = 10
        self.cell_size = 16

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(n):
            for j in range(n):
                cell = self.board[i][j]
                coord = (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size)
                if cell:
                    cell.rect.x, cell.rect.y = coord[0], coord[1]

    def move(self, x, y, move_x, move_y, sprite):
        self.board[y][x] = 0
        self.board[y + move_y][x + move_x] = sprite

    def fill(self, name):
        text_lvl = load_level(name)
        for i in range(n):
            for j in range(n):
                if text_lvl[i][j] == '0':
                    continue
                elem = pygame.sprite.Sprite(back_sprites)
                if text_lvl[i][j] == '.':
                    elem.image = pygame.transform.scale(load_image("grass.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "r":
                    elem.image = pygame.transform.scale(load_image("beta.png"), (self.cell_size, self.cell_size))
                elif text_lvl[i][j] == "c":
                    elem.image = pygame.transform.scale(load_image("house.png"), (self.cell_size, self.cell_size))
                elem.rect = elem.image.get_rect()
                self.board[i][j] = elem


class Player:
    def __init__(self, x, y):
        self.player = pygame.sprite.Sprite(hero_sprite)
        self.player.image = load_image("hero.png")
        self.player.rect = self.player.image.get_rect()
        self.coord = [x, y]
        self.board_player = board_player
        self.board_player.board[x][y] = self.player
        self.n = n

    def update(self, dx, dy):
        if 0 <= self.coord[0] + dx < self.n and dx:
            self.board_player.move(self.coord[0], self.coord[1], dx, dy, self.player)
            self.coord[0] += dx
        elif 0 <= self.coord[1] + dy < self.n and dy:
            self.board_player.move(self.coord[0], self.coord[1], dx, dy, self.player)
            self.coord[1] += dy


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    level = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    level = [list(line) for line in level]
    return level


def check_tower(x, y):
    return lvl[y][x] == '0' and board_moving.board[y][x] == 0


def check_monster_kill(x, y):
    if lvl[y][x] == 'c':
        pygame.mixer.Sound('data/no_hp.wav').play()
        return True
    return False


if __name__ == '__main__':
    counter = 0
    pygame.init()
    n = 8
    monsters_num = 10
    money = 20
    score = 0
    health = 4
    pygame.display.set_caption("Я слежу за тобой")
    screen = pygame.display.set_mode((700, 700))
    cell_width = 64
    left_top = 0
    board_moving = Board()
    board_state = Board()
    board_player = Board()
    board_background = Board()
    board_moving.set_view(left_top, left_top, cell_width)
    board_state.set_view(left_top, left_top, cell_width)
    board_player.set_view(left_top, left_top, cell_width)
    board_background.set_view(left_top, left_top, cell_width)
    back_sprites = pygame.sprite.Group()
    moving_sprites = pygame.sprite.Group()
    state_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    board_background.fill('lvl1_back.txt')
    board_state.fill('lvl1.txt')
    monsters = []
    towers = []
    clock = pygame.time.Clock()
    # Поменять скорость
    monsters_v = 1
    fps = 60
    par_monsters = monsters_v * cell_width / fps
    player = Player(7, 7)
    pygame.mixer.music.load('data/music.mp3')
    pygame.mixer.music.play()
    lvl = load_level('lvl1.txt')
    sound1 = pygame.mixer.Sound('data/arrow.wav')
    running = True
    start = False
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.update(1, 0)
                elif event.key == pygame.K_LEFT:
                    player.update(-1, 0)
                elif event.key == pygame.K_UP:
                    player.update(0, -1)
                elif event.key == pygame.K_DOWN:
                    player.update(0, 1)
                elif event.key == pygame.K_1:
                    if check_tower(player.coord[0], player.coord[1]) and money >= 10:
                        towers.append(Tower(player.coord[0], player.coord[1], 'ground'))
                        money -= 10
                elif event.key == pygame.K_2:
                    if check_tower(player.coord[0], player.coord[1]) and money >= 10:
                        towers.append(Tower(player.coord[0], player.coord[1], 'flying'))
                        money -= 10
        if monsters_num != 0 and board_moving.board[left_top][left_top] == 0:
            start = True
            monster_type = random.choice(['ground', 'flying'])
            a = [0] * int(1.5 * fps) + [1]
            if random.choice(a):
                obj_monster = Monster(left_top, left_top, monster_type, par_monsters)
                monsters.append(obj_monster)
                monsters_num -= 1
        if start:
            for monster in monsters:
                monster.move()
                if check_monster_kill(monster.coord[0], monster.coord[1]) or monster.hp <= 0:
                    if monster.m_type == 'ground' and monster.hp <= 0:
                        pygame.mixer.Sound('data/skell.wav').play()
                    elif monster.m_type == 'flying' and monster.hp <= 0:
                        pygame.mixer.Sound('data/eye.wav').play()
                    monster.monster.kill()
                    monsters.remove(monster)
                    money += 5
            if counter >= 60:
                for tower in towers:
                    tower.damage_monsters_near()
                counter = 0
        if not len(monsters):
            # Переход на след. уровень или конечный экран с выводом счета
            pass
        screen.fill((0, 0, 0))
        board_background.render()
        board_state.render()
        board_moving.render()
        board_player.render()
        clock.tick(fps)
        back_sprites.draw(screen)
        state_sprites.draw(screen)
        moving_sprites.draw(screen)
        hero_sprite.draw(screen)
        pygame.display.flip()
        counter += 1
    pygame.quit()
