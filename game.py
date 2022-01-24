import pygame
import os
import sys

pygame.init()
size = 760, 765
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Йопики у ворот')


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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

tile_width = tile_height = 64
tile_images = {
    'road': pygame.transform.scale(load_image('road.png'), (tile_width, tile_height)),
    'grass': pygame.transform.scale(load_image('grass.png'), (tile_width, tile_height)),
    'place': pygame.transform.scale(load_image('place.png'), (tile_width, tile_height)),
    'air_tower': pygame.transform.scale(load_image('air_tower_image.png', -1), (tile_width, tile_height)),
    'ground_tower': pygame.transform.scale(load_image('ground_tower_image.png', -1), (tile_width, tile_height))
}

player_image = pygame.transform.scale(load_image('player_image.png', -1), (tile_width, tile_height))
air_enemy = pygame.transform.scale(load_image('air_enemy_image.png', -1), (tile_width, tile_height))
ground_enemy = pygame.transform.scale(load_image('ground_enemy_image.png', -1), (tile_width, tile_height))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    # Для нормальной картинки
    image = player_image

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '-':
                Tile('road', x, y)
            elif level[y][x] == 'h':
                Tile('grass', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'g':
                Tile('ground_tower', x, y)
            elif level[y][x] == 'a':
                Tile('air_tower', x, y)
            elif level[y][x] == 'p':
                Tile('place', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
