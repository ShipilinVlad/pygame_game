import pygame
import os
import sys


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
places_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_width = tile_height = 64
size = tile_width * 8, tile_height * 8
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Йопики у ворот')
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


class Place(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(places_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def place_tower(self, tower_type, pos_x, pos_y):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dx, dy):
        if 0 <= self.rect.x + dx <= size[0] - tile_width:
            self.rect.x += dx
        if 0 <= self.rect.y + dy <= size[1] - tile_height:
            self.rect.y += dy


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(min(8, len(level))):
        for x in range(min(8, len(level[y]))):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '-':
                Tile('road', x, y)
            elif level[y][x] == 'g':
                Tile('grass', x, y)
                Tile('ground_tower', x, y)
            elif level[y][x] == 'a':
                Tile('grass', x, y)
                Tile('air_tower', x, y)
            elif level[y][x] == 'p':
                Tile('place', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def main():

    clock = pygame.time.Clock()
    fps = 60
    running = True
    player, level_x, level_y = generate_level(load_level('lvl1.txt'))
    player = Player(0, 0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player_group.update(64, 0)
                elif event.key == pygame.K_LEFT:
                    player_group.update(-64, 0)
                elif event.key == pygame.K_UP:
                    player_group.update(0, -64)
                elif event.key == pygame.K_DOWN:
                    player_group.update(0, 64)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
