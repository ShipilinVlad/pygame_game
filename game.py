import pygame
import os
import sys

pygame.init()
size = 760, 765
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Йопики у ворот')
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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


class Level:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.cell_size = 50

    def set_view(self, cell_size):
        self.cell_size = cell_size

    def render(self, screen):
        pass

    def get_cell(self, mouse_pos):
        pass

    def on_click(self, cell_cords):
        pass

    def get_click(self, mouse_pos):
        pass


class Player(pygame.sprite.Sprite):
    # Для нормальной картинки
    image = load_image('player_image1.jpg', -1)
    # Надо изменить размеры картинки на размеры клетки
    image = pygame.transform.scale(image, (64, 64))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


def main():
    pygame.init()
    size = 760, 765
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Йопики у ворот')
    clock = pygame.time.Clock()
    fps = 60
    running = True
    all_sprites = pygame.sprite.Group()
    Player(all_sprites)
    directions = {'left': False, 'right': False, 'up': False, 'down': False}
    counter = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    all_sprites.update(50, 0)
                elif event.key == pygame.K_LEFT:
                    all_sprites.update(-50, 0)
                elif event.key == pygame.K_UP:
                    all_sprites.update(0, -50)
                elif event.key == pygame.K_DOWN:
                    all_sprites.update(0, 50)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
