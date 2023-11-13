import pygame
import sys
import Levels

#### ====================================================== INITIALIZATION ===================================================== ####

DIMENSION_X = 20
DIMENSION_Y = 12

SCREEN_SIZE_X = 1000
SCREEN_SIZE_Y = SCREEN_SIZE_X * .6
TILE_SIZE = SCREEN_SIZE_X / DIMENSION_X
TILES = [[0 for i in range(DIMENSION_X)] for j in range(DIMENSION_Y)]

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
fences_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
tile_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
house_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
house_menu_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))

#### ====================================================== IMAGES/SPRITES ===================================================== ####


def get_image(y, x, tileset):
    image = pygame.Surface((16, 16)).convert_alpha()
    image.blit(tileset, (0, 0), ((x * 16), (y * 16), 16, 16))
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    image.set_colorkey((0, 0, 0))
    return image


SPRITES = []

grass_tileset = pygame.image.load("Tile_Sets/Grass.png").convert_alpha()
grass_sprites = []
grass_sprites.append(get_image(4, 2, grass_tileset))
for i in range(2):
    for j in range(6):
        grass_sprites.append(get_image(i, j, grass_tileset))
SPRITES.append(grass_sprites)

water_tileset = pygame.image.load("Tile_Sets/Water.png").convert_alpha()
water_sprites = []
for i in range(1):
    for j in range(4):
        water_sprites.append(get_image(i, j, water_tileset))
SPRITES.append(water_sprites)

dirt_path_tileset = pygame.image.load(
    "Tile_Sets/Tilled Dirt.png").convert_alpha()
dirt_path_sprites = []
for i in range(2):
    for j in range(3):
        dirt_path_sprites.append(get_image(i, j, dirt_path_tileset))
SPRITES.append(dirt_path_sprites)

water_grass_tileset = pygame.image.load("Tile_Sets/Grass.png").convert_alpha()
water_grass_sprites = []
for i in range(2, 7):
    for j in range(4):
        water_grass_sprites.append(
            get_image(i, j, water_grass_tileset))
for i in range(4, 6):
    for j in range(4, 6):
        water_grass_sprites.append(
            get_image(i, j, water_grass_tileset))

for i in range(7, 8):
    for j in range(4):
        water_grass_sprites.append(
            get_image(i, j, water_grass_tileset))
for i in range(2, 8):
    for j in range(6, 10):
        water_grass_sprites.append(
            get_image(i, j, water_grass_tileset))
SPRITES.append(water_grass_sprites)

FENCES = [[0 for i in range(DIMENSION_X + 1)] for j in range(DIMENSION_Y + 1)]

fences_tileset = pygame.image.load("Tile_Sets/Fences.png").convert_alpha()
fences_sprites = []
for i in range(4):
    for j in range(4):
        fences_sprites.append(get_image(i, j, fences_tileset))
SPRITES.append(fences_sprites)


house_tileset = pygame.image.load("Tile_Sets/Wooden House.png").convert_alpha()
house_sprites = []
for i in range(5):
    for j in range(7):
        house_sprites.append(get_image(i, j, house_tileset))
SPRITES.append(house_sprites)

for i in range(len(house_sprites)):
    x = 0
    y = 0
    if i < 20:
        x = i
        y = 0
    elif i < 40:
        x = i - 20
        y = 50
    else:
        x = i - 40
        y = 100

    house_menu_screen.blit(house_sprites[i], (x * 50, y))
    font = pygame.font.Font('m5x7.ttf', 16)
    text = font.render(str(i), True, (255, 30, 100))
    textRect = text.get_rect()
    textRect.center = (x * 50 + 25, y + 25)
    house_menu_screen.blit(text, textRect)


#### ==================================================== LEVEL/BACKGROUND =================================================== ####


class Tile:
    def __init__(self, i, j):
        self.x = j
        self.y = i
        self.image = 0
        self.image_set = -1
        self.image_number = 0
        self.rect = pygame.Rect(
            TILE_SIZE * j, TILE_SIZE * i, TILE_SIZE, TILE_SIZE)
        # pygame.draw.rect(screen, (183, 173, 163), self.rect, 0)

    def update(self, image_set, image_number_change, background_set=9):
        self.background_set = background_set
        if (image_set >= len(SPRITES)):
            return
        if (self.background_set != 9):
            self.image_number = 0
            self.update(background_set, 0)
            self.image_set = image_set
        if self.image_set == image_set:
            self.image_number += image_number_change
            if (self.image_number == len(SPRITES[image_set])):
                self.image_number = 0

        else:
            self.image_number = 0
            self.image_set = image_set
        self.image = SPRITES[self.image_set][self.image_number]
        tile_screen.blit(self.image, (TILE_SIZE * self.x, TILE_SIZE * self.y))
        self.background_set = background_set
        pygame.display.flip()


for i in range(DIMENSION_Y):  # initialize TILES
    for j in range(DIMENSION_X):
        tile = Tile(i, j)
        TILES[int(i)][int(j)] = tile
        pygame.display.flip()


def BuildLevel(level):  # Build level based on level_name variable
    for i in range(DIMENSION_Y):
        for j in range(DIMENSION_X):
            TILES[i][j].image_set = -1
            image_set = level[i][j][0]
            background_set = level[i][j][1]
            image_number = level[i][j][2:]
            TILES[i][j].update(int(image_set), int(
                image_number), int(background_set))
            TILES[i][j].update(int(image_set), int(
                image_number), int(background_set))
    pygame.display.flip()


BuildLevel(Levels.LEVEL_1)
background = screen.copy()


def PrintLevel(level_name):
    for i in range(DIMENSION_Y):
        for j in range(DIMENSION_X):
            curr_tile = TILES[i][j]
            Levels.LEVEL_1[i][j] = str(
                curr_tile.image_set) + str(curr_tile.background_set) + str(curr_tile.image_number)
    print(Levels.LEVEL_1)
    pygame.image.save(screen.copy(), "LEVEL_" + str(level_name) + ".png")


def ConnectGrass():
    for i in range(DIMENSION_Y):
        for j in range(DIMENSION_X):
            curr_tile = TILES[i][j]
            if curr_tile.image_set == 0 or curr_tile.image_set == 3:
                border_tiles = []
                border_set = -1
                if i > 0:
                    if TILES[i - 1][j].image_set == 1 or TILES[i - 1][j].image_set == 2:
                        border_set = TILES[i - 1][j].image_set
                        border_tiles.append(0)
                if j < DIMENSION_X - 1:
                    if TILES[i][j + 1].image_set == 1 or TILES[i][j + 1].image_set == 2:
                        border_set = TILES[i][j + 1].image_set
                        border_tiles.append(1)
                if i < DIMENSION_Y - 1:
                    if TILES[i + 1][j].image_set == 1 or TILES[i + 1][j].image_set == 2:
                        border_set = TILES[i + 1][j].image_set
                        border_tiles.append(2)
                if j > 0:
                    if TILES[i][j - 1].image_set == 1 or TILES[i][j - 1].image_set == 2:
                        border_set = TILES[i][j - 1].image_set
                        border_tiles.append(3)

                if len(border_tiles) == 0:
                    continue
                if len(border_tiles) == 1:
                    if border_tiles[0] == 0:
                        curr_tile.update(3, 6, border_set)
                    if border_tiles[0] == 1:
                        curr_tile.update(3, 11, border_set)
                    if border_tiles[0] == 2:
                        curr_tile.update(3, 14, border_set)
                    if border_tiles[0] == 3:
                        curr_tile.update(3, 9, border_set)

                if len(border_tiles) == 2:
                    if border_tiles == [0, 1]:
                        curr_tile.update(3, 7, border_set)
                    if border_tiles == [0, 2]:
                        curr_tile.update(3, 17, border_set)
                    if border_tiles == [0, 3]:
                        curr_tile.update(3, 5, border_set)

                    if border_tiles == [1, 2]:
                        curr_tile.update(3, 15, border_set)
                    if border_tiles == [1, 3]:
                        curr_tile.update(3, 9, border_set)

                    if border_tiles == [2, 3]:
                        curr_tile.update(3, 13, border_set)

                if len(border_tiles) == 3:
                    if border_tiles == [0, 1, 2]:
                        curr_tile.update(3, 19, border_set)
                    if border_tiles == [0, 1, 3]:
                        curr_tile.update(3, 0, border_set)
                    if border_tiles == [0, 2, 3]:
                        curr_tile.update(3, 16, border_set)
                    if border_tiles == [1, 2, 3]:
                        curr_tile.update(3, 12, border_set)

                if len(border_tiles) == 4:
                    curr_tile.update(3, 3, border_set)

    for i in range(DIMENSION_Y):
        for j in range(DIMENSION_X):
            curr_tile = TILES[i][j]
            border_set = -1
            corners = []
            if curr_tile.image_set == 0 or curr_tile.image_set == 3:
                if (i > 0 and j > 0):
                    if TILES[i-1][j].image_set == 3 and TILES[i][j-1].image_set == 3 and TILES[i-1][j-1].image_set != 3 and TILES[i-1][j-1].image_set != 0:
                        border_set = TILES[i-1][j-1].image_set
                        corners.append(1)
                if (i > 0 and j < DIMENSION_X - 1):
                    if TILES[i-1][j].image_set == 3 and TILES[i][j+1].image_set == 3 and TILES[i-1][j+1].image_set != 3 and TILES[i-1][j+1].image_set != 0:
                        border_set = TILES[i-1][j+1].image_set
                        corners.append(2)
                if (i < DIMENSION_Y - 1 and j < DIMENSION_X - 1):
                    if TILES[i+1][j].image_set == 3 and TILES[i][j+1].image_set == 3 and TILES[i+1][j+1].image_set != 3 and TILES[i+1][j+1].image_set != 0:
                        border_set = TILES[i+1][j+1].image_set
                        corners.append(3)
                if (i < DIMENSION_Y - 1 and j > 0):
                    if TILES[i+1][j].image_set == 3 and TILES[i][j-1].image_set == 3 and TILES[i+1][j-1].image_set != 3 and TILES[i+1][j-1].image_set != 0:
                        border_set = TILES[i+1][j-1].image_set
                        corners.append(4)

            if len(corners) == 0:
                continue
            if len(corners) == 1:
                if corners[0] == 1:
                    if curr_tile.image_number == 11 and curr_tile.image_set == 3:
                        curr_tile.update(3, 39, border_set)
                    elif curr_tile.image_number == 14 and curr_tile.image_set == 3:
                        curr_tile.update(3, 40, border_set)
                    else:
                        curr_tile.update(3, 23, border_set)
                if corners[0] == 2:
                    if curr_tile.image_number == 9 and curr_tile.image_set == 3:
                        curr_tile.update(3, 16, border_set)
                    elif curr_tile.image_number == 14 and curr_tile.image_set == 3:
                        curr_tile.update(3, 43, border_set)
                    else:
                        curr_tile.update(3, 22, border_set)
                if corners[0] == 3:
                    if curr_tile.image_number == 6 and curr_tile.image_set == 3:
                        curr_tile.update(3, 37, border_set)
                    elif curr_tile.image_number == 9 and curr_tile.image_set == 3:
                        curr_tile.update(3, 42, border_set)
                    else:
                        curr_tile.update(3, 20, border_set)
                if corners[0] == 4:
                    if curr_tile.image_number == 6 and curr_tile.image_set == 3:
                        curr_tile.update(3, 38, border_set)
                    elif curr_tile.image_number == 11 and curr_tile.image_set == 3:
                        curr_tile.update(3, 42, border_set)
                        curr_tile.image = pygame.transform.flip(
                            curr_tile.image, 1, 0)
                    else:
                        curr_tile.update(3, 21, border_set)

            if len(corners) == 2:
                if corners == [1, 2]:
                    curr_tile.update(3, 45, border_set)
                if corners == [1, 3]:
                    curr_tile.update(3, 27, border_set)
                if corners == [1, 4]:
                    curr_tile.update(3, 44, border_set)

                if corners == [2, 3]:
                    curr_tile.update(3, 49, border_set)
                if corners == [2, 4]:
                    curr_tile.update(3, 26, border_set)

                if corners == [3, 4]:
                    curr_tile.update(3, 48, border_set)

            if len(corners) == 3:
                if corners == [1, 2, 3]:
                    curr_tile.update(3, 29, border_set)
                if corners == [1, 2, 4]:
                    curr_tile.update(3, 28, border_set)
                if corners == [1, 3, 4]:
                    curr_tile.update(3, 32, border_set)
                if corners == [2, 3, 4]:
                    curr_tile.update(3, 33, border_set)

            if len(corners) == 4:
                curr_tile.update(3, 25, border_set)

#### ====================================================== PLAYER ===================================================== ####


f = False
h_pressed = False
house_menu_shown = False
curr_house_sprite = 0
while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            image_set = event.key - 49
            if event.key >= 49 and event.key < 59:
                pos = pygame.mouse.get_pos()
                x = int(pos[0] / TILE_SIZE)
                y = int(pos[1] / TILE_SIZE)
                if (image_set != 3):
                    TILES[y][x].update(image_set, 1)
                if (image_set != 3):
                    TILES[y][x].update(image_set, 0)
                pygame.display.flip()
            if event.key == pygame.K_p:  # print level
                level_name = input("Input Level Name: ")
                PrintLevel(level_name)

            if (f == False):
                background = screen.copy()
            if event.key == pygame.K_f:
                f = True
                print(event.key)
                pos = pygame.mouse.get_pos()
                x = int(pos[0] / TILE_SIZE)
                y = int(pos[1] / TILE_SIZE)
                fences_neighbors = [FENCES[y-1][x], FENCES[y]
                                    [x+1], FENCES[y+1][x], FENCES[y][x-1]]
                if fences_neighbors == [0, 0, 0, 0]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[12], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [1, 0, 0, 0]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[0], (x * TILE_SIZE, (y - 1) * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[8], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [0, 1, 0, 0]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[15], ((x + 1) * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[13], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [0, 0, 1, 0]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[8], (x * TILE_SIZE, (y + 1) * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[0], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [0, 0, 0, 1]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[13], ((x - 1) * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[15], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [1, 0, 1, 0]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[0], (x * TILE_SIZE, (y - 1) * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[8], (x * TILE_SIZE, (y + 1) * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[8], (x * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[0], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [0, 1, 0, 1]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[15], ((x + 1) * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[13], ((x - 1) * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[13], (x * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[15], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [1, 1, 0, 0]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[0], (x * TILE_SIZE, (y - 1) * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[15], ((x + 1) * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[8], (x * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[13], (x * TILE_SIZE, y * TILE_SIZE))

                if fences_neighbors == [0, 1, 1, 0]:
                    FENCES[y][x] = 1
                    fences_screen.blit(
                        fences_sprites[8], (x * TILE_SIZE, (y + 1) * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[15], ((x + 1) * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[13], (x * TILE_SIZE, y * TILE_SIZE))
                    fences_screen.blit(
                        fences_sprites[0], (x * TILE_SIZE, y * TILE_SIZE))

            if event.key == pygame.K_h:
                pos = pygame.mouse.get_pos()
                x = int(pos[0] / TILE_SIZE)
                y = int(pos[1] / TILE_SIZE)
                if house_menu_shown:
                    house_menu_shown = False
                else:
                    house_menu_shown = True

            if event.key == pygame.K_g:
                if house_menu_screen:
                    pos = pygame.mouse.get_pos()
                    x = int(pos[0] / TILE_SIZE)
                    y = int(pos[1] / TILE_SIZE)
                    i = x + y * 20
                    if i < len(house_sprites):
                        curr_house_sprite = i

            if event.key == pygame.K_b:
                if house_menu_screen:
                    pos = pygame.mouse.get_pos()
                    x = int(pos[0] / TILE_SIZE)
                    y = int(pos[1] / TILE_SIZE)
                    house_screen.blit(house_sprites[curr_house_sprite], (x * TILE_SIZE, y * TILE_SIZE))
                    TILES[y][x].update(5, 0)
            
            if event.key == pygame.K_v:
                if house_menu_screen:
                    house_screen.fill((0, 0, 0))

            if event.key == pygame.K_l:  # increment level forward
                Levels.LEVEL_NUMBER += 1
                if (Levels.LEVEL_NUMBER < len(Levels.LEVELS)):
                    BuildLevel(Levels.LEVELS[Levels.LEVEL_NUMBER])
                else:
                    Levels.LEVEL_NUMBER -= 1
            if event.key == pygame.K_k:  # increment level backward
                Levels.LEVEL_NUMBER -= 1
                if (Levels.LEVEL_NUMBER >= 0):
                    BuildLevel(Levels.LEVELS[Levels.LEVEL_NUMBER])
                else:
                    Levels.LEVEL_NUMBER += 1
            if event.key == pygame.K_c:
                ConnectGrass()
    tile_screen.set_colorkey((0, 0, 0))
    screen.blit(tile_screen, (0, 0))
    fences_screen.set_colorkey((0, 0, 0))
    screen.blit(fences_screen, (0, 0))
    house_screen.set_colorkey((0, 0, 0))
    screen.blit(house_screen, (0, 0))
    if house_menu_shown:
        house_menu_screen.set_colorkey((0, 0, 0))
        screen.blit(house_menu_screen, (0, 0))
    pygame.display.update()
