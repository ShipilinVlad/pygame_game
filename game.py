import os
import sys
import pygame
import random


class Monster:
    def __init__(self, x, y, m_type, par, board_width, n, board, all_sprites):
        self.board = board
        self.x, self.y, self.m_type, self.n = x, y, m_type, n
        self.width, self.nx, self.ny = board_width, 1, 0
        self.par_x, self.par_y = par, par
        self.coord = [0, 0]
        self.left, self.top = 0, 0
        self.y = board_width / 2
        self.rotate = False
        if self.m_type == 'flying':
            monster_image = load_image("cataract.png")
        else:
            monster_image = load_image("skelly.png")
        self.monster = pygame.sprite.Sprite(all_sprites)
        self.monster.image = monster_image
        self.monster.rect = self.monster.image.get_rect()

    def move(self):
        if self.left + self.coord[0] * self.width <= self.x <= self.left + (self.coord[0] + 1) * self.width and \
                self.top + self.coord[1] * self.width <= self.y <= self.top + (self.coord[1] + 1) * self.width:
            self.x += self.par_x * self.nx
            self.y += self.par_y * self.ny

            if self.rotate and self.x % self.width > self.width // 2 and self.nx == 1:
                self.ny = self.nx
                self.nx = 0
                self.rotate = False
            elif self.rotate and self.y % self.width > self.width // 2 and self.ny == 1:
                self.nx = -self.ny
                self.ny = 0
                self.rotate = False
            elif self.rotate and self.x % self.width < self.width // 2 and self.nx == -1:
                self.ny = self.nx
                self.nx = 0
                self.rotate = False
            elif self.rotate and self.y % self.width < self.width // 2 and self.ny == -1:
                self.nx = -self.ny
                self.ny = 0
                self.rotate = False
        else:
            board.monster_move(self.coord[0], self.coord[1], self.nx, self.ny, self.monster)
            self.coord[0] += self.nx
            self.coord[1] += self.ny
            if self.coord[0] == self.n - 1 and self.nx == 1 or self.coord[1] == self.n - 1 and self.ny == 1 or\
                    self.coord[0] == 0 and self.nx == -1 or self.coord[1] == 0 and self.ny == -1:
                self.rotate = True


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
                pygame.draw.rect(screen, pygame.Color('white'), coords, 1)


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        print(cell_coords)
        if cell_coords:
            cell_coords = cell_coords[1], cell_coords[0]
            road = pygame.sprite.Sprite(all_sprites)
            road.image = load_image("beta.png")
            road.rect = road.image.get_rect()
            self.board[cell_coords[0]][cell_coords[1]] = road


    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if mouse_x < self.left or mouse_y < self.top or mouse_x > self.left + self.cell_size * self.width\
                or mouse_y > self.top + self.cell_size * self.height:
            return None
        return ((mouse_x - self.left) // self.cell_size, (mouse_y - self.top) // self.cell_size)

    def monster_move(self, x, y, move_x, move_y, monster):
        self.board[y][x] = 0
        self.board[y + move_y][x + move_x] = monster

    def monster_spawn(self, x, y, monster):
        self.board[x][y] = monster

    def fill(self, name):
        for i in range(self.width):
            for j in range(self.height):
                road = pygame.sprite.Sprite(all_sprites)
                road.image = load_image(name)
                road.rect = road.image.get_rect()
                self.board[i][j] = road


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


if __name__ == '__main__':
    pygame.init()
    n = 8
    pygame.display.set_caption("Я слежу за тобой")
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    board = Board(n, n)
    board_state = Board(n, n)
    board_width = 64
    left_top = 0
    board.set_view(left_top, left_top, board_width)
    board_state.set_view(left_top, left_top, board_width)
    all_sprites = pygame.sprite.Group()
    monsters = []
    clock = pygame.time.Clock()
    v, fps = 1, 60
    par = v * board_width / fps
    running = True
    start = False
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start = True
                    monster_type = random.choice(['ground', 'flying'])
                    obj_monster = Monster(left_top, left_top, monster_type, par, board_width, n, board, all_sprites)
                    monsters.append(obj_monster)
                    board.monster_spawn(0, 0, obj_monster.monster)
                else:
                    print(1)
                    board_state.get_click(event.pos)
        if start:
            for i in range(len(monsters)):
                monsters[i].move()
        screen.fill((0, 0, 0))
        board_state.render(screen)
        board.render(screen)
        clock.tick(fps)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
