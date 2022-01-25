import os
import sys
import pygame
import random


class Monster:
    def __init__(self, x, y, m_type, par, board_width, n, board, board_state, lvl):
        # Для первого уровня!!!
        self.x, self.y, self.nx, self.ny = x, board_width / 2, 1, 0
        self.board = board
        self.board_state = board_state
        self.m_type, self.n = m_type, n
        self.width = board_width
        self.par_x, self.par_y = par, par
        self.coord = [0, 0]
        self.left, self.top = 0, 0
        self.rotate = False
        if self.m_type == 'flying':
            monster_image = load_image("eye.png")
        else:
            monster_image = load_image("skel.png")
        self.monster = pygame.sprite.Sprite(moving_sprites)
        self.monster.image = monster_image
        self.monster.rect = self.monster.image.get_rect()
        self.board.board[0][0] = self.monster
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
                elif self.lvl[self.coord[1] + self.nx * ((self.ny - self.nx) ** 2)]\
                    [self.coord[0] + self.ny * (-(self.nx - self.ny) ** 2)] not in ('r', 'c'):
                    self.rotate = 'left'
                else:
                    self.rotate = 'right'
                print(self.rotate)

class Tower:
        def __init__(self, x, y, t_type, board_moving):
            self.x, self.y = x, y
            self.t_type = t_type
            self.board_moving = board_moving
            if self.t_type == 'flying':
                tower_image = load_image("archer.png")
            else:
                tower_image = load_image("wizard.png")
            self.tower = pygame.sprite.Sprite(moving_sprites)
            self.tower.image = tower_image
            self.tower.rect = self.tower.image.get_rect()
            self.board_moving.board[y][x] = self.tower

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 16

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.board[i][j]
                coords = (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size)
                if cell:
                    cell.rect.x, cell.rect.y = coords[0], coords[1]
                pygame.draw.rect(screen, pygame.Color('black'), coords, 2)


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        print(cell_coords)
        if cell_coords:
            cell_coords = cell_coords[1], cell_coords[0]
            road = pygame.sprite.Sprite(state_sprites)
            road.image = load_image("beta.png")
            road.rect = road.image.get_rect()
            self.board[cell_coords[0]][cell_coords[1]] = road


    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if mouse_x < self.left or mouse_y < self.top or mouse_x > self.left + self.cell_size * self.width\
                or mouse_y > self.top + self.cell_size * self.height:
            return None
        return ((mouse_x - self.left) // self.cell_size, (mouse_y - self.top) // self.cell_size)

    def move(self, x, y, move_x, move_y, sprite):
        self.board[y][x] = 0
        self.board[y + move_y][x + move_x] = sprite

    def fill(self, name):
        text_lvl = load_level(name)
        for i in range(self.width):
            for j in range(self.height):
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

    def check_tower(self, x, y, lvl, moving_board):
        if lvl[y][x] == '0' and moving_board.board[y][x] == 0:
            return True
        return False

    def check_monster_kill(self, x, y, lvl):
        if lvl[y][x] == 'c':
            return True

class Player:
    def __init__(self, x, y, n, board_player):
        self.player = pygame.sprite.Sprite(hero_sprite)
        self.player.image = load_image("hero.png")
        self.player.rect = self.player.image.get_rect()
        self.coords = [x, y]
        self.board_player = board_player
        self.board_player.board[x][y] = self.player
        self.n = n

    def update(self, dx, dy):
        if 0 <= self.coords[0] + dx < self.n and dx != 0:
            self.board_player.move(self.coords[0], self.coords[1], dx, dy, self.player)
            self.coords[0] += dx
        elif 0 <= self.coords[1] + dy < self.n and dy != 0:
            self.board_player.move(self.coords[0], self.coords[1], dx, dy, self.player)
            self.coords[1] += dy


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    lvl = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    lvl = [list(line) for line in lvl]
    return lvl


if __name__ == '__main__':
    pygame.init()
    n = 8
    pygame.display.set_caption("Я слежу за тобой")
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    board_width = 64
    left_top = 0
    board_moving = Board(n, n)
    board_state = Board(n, n)
    board_player = Board(n, n)
    board_background = Board(n, n)
    board_moving.set_view(left_top, left_top, board_width)
    board_state.set_view(left_top, left_top, board_width)
    board_player.set_view(left_top, left_top, board_width)
    board_background.set_view(left_top, left_top, board_width)
    back_sprites = pygame.sprite.Group()
    moving_sprites = pygame.sprite.Group()
    state_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Group()
    board_background.fill('lvl1_back.txt')
    board_state.fill('lvl1.txt')
    monsters = []
    towers = []
    clock = pygame.time.Clock()
    monsters_v = 1
    fps = 60
    par_monsters = monsters_v * board_width / fps
    player = Player(7, 7, n, board_player)
    lvl = load_level('lvl1.txt')
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
                    if board_state.check_tower(player.coords[0], player.coords[1], lvl, board_moving):
                        towers.append(Tower(player.coords[0], player.coords[1], 'ground', board_moving))
                elif event.key == pygame.K_2:
                    if board_state.check_tower(player.coords[0], player.coords[1], lvl, board_moving):
                        towers.append(Tower(player.coords[0], player.coords[1], 'flying', board_moving))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start = True
                    monster_type = random.choice(['ground', 'flying'])
                    obj_monster = Monster(left_top, left_top, monster_type, par_monsters, board_width, n,
                                          board_moving, board_state, lvl)
                    monsters.append(obj_monster)
                elif event.button == 2:
                    board_state.get_click(event.pos)
        if start:
            for i in range(len(monsters)):
                monsters[i].move()
                if board_moving.check_monster_kill(monsters[i].coord[0], monsters[i].coord[1], lvl):
                    monsters[i].monster.kill()
                    monsters.remove(monsters[i])
        screen.fill((0, 0, 0))
        board_background.render(screen)
        board_state.render(screen)
        board_moving.render(screen)
        board_player.render(screen)
        clock.tick(fps)
        back_sprites.draw(screen)
        state_sprites.draw(screen)
        moving_sprites.draw(screen)
        hero_sprite.draw(screen)
        pygame.display.flip()
    pygame.quit()
