import pygame


class Monster:
    def __init__(self, x, y, m_type, par, board_width, n, board):
        self.board = board
        self.x, self.y, self.m_type, self.n = x, y, m_type, n
        self.width, self.nx, self.ny = board_width, 1, 0
        self.par_x, self.par_y = par, par
        self.coord = [0, 0]
        self.left, self.top = 10, 10

    def move(self):
        if self.left + self.coord[0] * self.width <= self.x <= self.left + (self.coord[0] + 1) * self.width and \
                self.top + self.coord[1] * self.width <= self.y <= self.top + (self.coord[1] + 1) * self.width:
            self.x += self.par_x * self.nx
            self.y += self.par_y * self.ny
        else:
            board.monster_move(self.coord[0], self.coord[1], self.nx, self.ny)
            self.coord[0] += self.nx
            self.coord[1] += self.ny
            if self.coord[0] == self.n - 1 and self.nx == 1:
                self.ny = self.nx
                self.nx = 0
            elif self.coord[1] == self.n - 1 and self.ny == 1:
                self.nx = -self.ny
                self.ny = 0
            elif self.coord[0] == 0 and self.nx == -1:
                self.ny = self.nx
                self.nx = 0
            elif self.coord[1] == 0 and self.ny == -1:
                self.nx = -self.ny
                self.ny = 0




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
                    pygame.draw.rect(screen, pygame.Color('blue'), coords)
                pygame.draw.rect(screen, pygame.Color('white'), coords, 1)


    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        print(cell_coords)
        if cell_coords:
            cell_coords = cell_coords[1], cell_coords[0]
            if self.board[cell_coords[0]][cell_coords[1]] == 0:
                self.board[cell_coords[0]][cell_coords[1]] = 1


    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        if mouse_x < self.left or mouse_y < self.top or mouse_x > self.left + self.cell_size * self.width\
                or mouse_y > self.top + self.cell_size * self.height:
            return None
        return ((mouse_x - self.left) // self.cell_size, (mouse_y - self.top) // self.cell_size)

    def check(self):
        if self.board[0][0] == 0:
            return True
        else:
            return False

    def monster_move(self, x, y, move_x, move_y):
        self.board[y][x] = 0
        self.board[y + move_y][x + move_x] = 1

    def monster_spawn(self, x, y):
        self.board[x][y] = 1



if __name__ == '__main__':
    pygame.init()
    n = 8
    pygame.display.set_caption("Я слежу за тобой")
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    board = Board(n, n)
    board_width = 64
    board.set_view(10, 10, board_width)
    monsters = []
    clock = pygame.time.Clock()
    v, fps = 0.5, 60
    par = v * board_width / fps
    running = True
    start = False
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = True
                monsters.append(Monster(10, 10, 'ground', par, board_width, n, board))
                board.monster_spawn(0, 0)
        if start:
            for i in range(len(monsters)):
                monsters[i].move()
        screen.fill((0, 0, 0))
        board.render(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
