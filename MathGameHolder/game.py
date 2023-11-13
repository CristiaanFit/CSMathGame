import pygame
import sys
import data
sys.path.insert(0, './data')
import Levels
import problems
import random
import math


#### ====================================================== INITIALIZATION ===================================================== ####

DIMENSION_X = 20
DIMENSION_Y = 12

SCREEN_SIZE_X = 1000
SCREEN_SIZE_Y = SCREEN_SIZE_X * .6
TILE_SIZE = SCREEN_SIZE_X / DIMENSION_X
TILES = [[0 for i in range(DIMENSION_X)] for j in range(DIMENSION_Y)]

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
collision_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
house_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
player_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
clock = pygame.time.Clock()


#### ==================================================== LEVEL/BACKGROUND =================================================== ####

level_number = 0
levels = []
levels.append(pygame.image.load("data/Level/LEVEL_Spawn.png"))
levels.append(pygame.image.load("data/Level/LEVEL_Combat.png"))
levels.append(pygame.image.load("data/Level/LEVEL_House.png"))

ds1  = pygame.image.load("data/Level/DesertScreen1.png")
ds1 = pygame.transform.scale(ds1, (1000, 600))
levels.append(ds1)
levels.append(pygame.image.load("data/Level/DesertScreen2.png"))

solid_tiles = []

house_screen.blit(pygame.image.load("data/Level/House.png"), (0, 0))



class Tile:
    def __init__(self, i, j):
        self.x = j
        self.y = i
        level = Levels.LEVELS[Levels.LEVEL_NUMBER]
        if (level[i][j][0] == "1" or level[i][j][0] == "5"):
            self.rect = pygame.Rect(
                TILE_SIZE * j, TILE_SIZE * i, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(collision_screen, (255, 0, 0), self.rect)
            solid_tiles.append(self)


for i in range(DIMENSION_Y):
    for j in range(DIMENSION_X):
        tile = Tile(i, j)


def ChangeLevel(level_num):
    global solid_tiles
    solid_tiles = []
    global level_number
    level_number = level_num
    global screen
    screen.blit(levels[level_num], (0, 0))
    Levels.LEVEL_NUMBER = level_num
    collision_screen.fill((0, 0, 0))
    if level_num != 1:
        for i in range(DIMENSION_Y):
            for j in range(DIMENSION_X):
                tile = Tile(i, j)

#### ======================================================== PLAYER ======================================================== ####


def get_character_image(y, x, tileset):
    image = pygame.Surface((16, 17)).convert_alpha()
    if y == 1:
        image.blit(tileset, (0, 1), ((x * 16), (y * 16 + 6), 16, 16))
    if y == 2:
        image.blit(tileset, (0, 0), ((x * 16), (y * 16 + 13), 16, 17))
    if y == 3:
        image.blit(tileset, (0, 1), ((x * 16), (y * 16 + 21), 16, 16))
    image = pygame.transform.scale(image, (TILE_SIZE - 10, TILE_SIZE - 10 + 3))
    image.set_colorkey((0, 0, 0))
    return image


player_tileset = pygame.image.load("data/robot.png").convert_alpha()
player_sprites = []
for i in range(8):
    temp = []
    for j in range(1, 4):
        temp.append(get_character_image(j, i, player_tileset))
    player_sprites.append(temp)


class Player:
    def __init__(self):
        self.x = 500
        self.y = 300
        self.width = 28
        self.height = 25
        self.image = player_sprites[4][1]

        self.speed = .2
        self.direction = 0
        self.frame = 1
        self.last_update = 0
        self.animation_cooldown = 200
        self.forward = True

        self.health = 3
        self.last_damaged = 0
        self.colliding_with_enemy = False

        self.problems_completed = 0
        self.problems_needed = 10
        self.ending_combat_loss = False
        self.ending_combat_win = False
        self.ending_combat_time = 0

        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False

        self.player_rect = pygame.Rect(
            self.x + 5, self.y + 4, self.width, self.height)

    def update(self, dt):
        self.current_time = pygame.time.get_ticks()
        if (in_combat and self.current_time - self.last_damaged < 3000 and self.health != 0):
            self.immunity_indicator()

        collider_tiles = []
        for i in range(len(solid_tiles)):
            if (pygame.Rect.colliderect(player.player_rect, solid_tiles[i].rect)):
                collider_tiles.append(solid_tiles[i])

        directions = []

        if level_number == 1:
            if (self.w_pressed == True):
                directions.append(0)
                if self.y > 210:
                    self.y = self.y - self.speed * dt
            if (self.a_pressed == True):
                directions.append(6)
                if self.x > 254:
                    self.x = self.x - self.speed * dt
            if (self.s_pressed == True):
                directions.append(4)
                if self.y < 550:
                    self.y = self.y + self.speed * dt
            if (self.d_pressed == True):
                directions.append(2)
                if self.x < 710:
                    self.x = self.x + self.speed * dt

        else:
            if (self.w_pressed == True):
                directions.append(0)
                if (self.y > 0):
                    self.y = self.y - self.speed * dt
            if (self.a_pressed == True):
                directions.append(6)
                if (self.x > 0):
                    self.x = self.x - self.speed * dt
            if (self.s_pressed == True):
                directions.append(4)
                if (self.y < SCREEN_SIZE_Y - TILE_SIZE):
                    self.y = self.y + self.speed * dt
            if (self.d_pressed == True):
                directions.append(2)
                if (self.x < SCREEN_SIZE_X - TILE_SIZE):
                    self.x = self.x + self.speed * dt

            for tile in collider_tiles:

                if ((player.y - tile.y * TILE_SIZE) > 20):
                    self.y = self.y + self.speed * dt
                if ((player.x - tile.x * TILE_SIZE) > 20):
                    self.x = self.x + self.speed * dt
                if ((player.y - tile.y * TILE_SIZE) < -10):
                    self.y = self.y - self.speed * dt
                if ((player.x - tile.x * TILE_SIZE) < -10):
                    self.x = self.x - self.speed * dt

        if len(directions) == 0:  # change direction
            self.frame = 1
        else:
            if len(directions) == 1:
                self.direction = directions[0]
            if len(directions) == 2:
                if directions[0] == 0 and directions[1] == 6:
                    self.direction = 7
                else:
                    self.direction = (directions[0] + directions[1]) // 2
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                if self.forward:
                    self.frame += 1
                if self.forward == False:
                    self.frame -= 1
                self.last_update = current_time
                if self.frame >= len(player_sprites[self.direction]):
                    self.forward == False
                    self.frame -= 2
                if self.frame < 0:
                    self.forward == False
                    self.frame += 2

        if (Levels.LEVEL_NUMBER == 0):
            if (self.y < 5 and (self.x > 700 and self.x < 850)):
                self.y = SCREEN_SIZE_Y - 65
                ChangeLevel(2)

        if (Levels.LEVEL_NUMBER == 0):
            if (self.x > 950 and (self.y < 700)):
                self.x = self.x - 900
                ChangeLevel(3)

        if (Levels.LEVEL_NUMBER == 3):
            if (self.x < 20 and (self.y < 700)):
                self.x = self.x + 850
                ChangeLevel(0)

        if (Levels.LEVEL_NUMBER == 2):
            if (self.y > 550 and (self.x > 700 and self.x < 850)):
                self.y = 20
                ChangeLevel(0)

        if (Levels.LEVEL_NUMBER == 2):
            if (self.y > 370 and self.y < 415 and (self.x > 390 and self.x < 440)):
                font = pygame.font.Font('data/m5x7.ttf', 64)
                text = font.render("PRESS F TO ENTER", True, (255, 0, 0))
                textRect = text.get_rect()
                textRect.center = (self.x + 10, self.y + 70)
                dialogue_screen.blit(text, textRect)

        self.player_rect = pygame.Rect(
            self.x + 5, self.y + 4, self.width, self.height)
        self.image = player_sprites[self.direction][self.frame]
        player_screen.blit(self.image, (self.x, self.y))

    def damage(self):
        if self.current_time - self.last_damaged > 3000:
            if self.health > 0:
                self.health -= 1
            DisplayHealth()
            self.last_damaged = self.current_time
        if (self.health == 0):
            if self.ending_combat_time == 0:
                self.ending_combat_time = pygame.time.get_ticks()
            self.ending_combat_loss = True

    def immunity_indicator(self):
        temp = pygame.Rect(self.x - 4, self.y - 4,
                           self.width + 17, self.height + 28)
        pygame.draw.rect(screen, (255, 0, 255), temp, 4)
        temp = pygame.Rect(250, 140, 170, 60)
        pygame.draw.rect(screen, (255, 0, 255), temp)


player = Player()

#### ======================================================= ENEMIES ======================================================= ####


def get_enemy_image(x, y, tileset):
    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(tileset, (0, 0), ((x * 32 + 2), (y * 32), 32, 32))
    image = pygame.transform.scale(image, (TILE_SIZE * 1.5, TILE_SIZE * 1.5))
    image.set_colorkey((0, 0, 0))
    return image


enemy_tileset = pygame.image.load(
    "data/Enemy_Experiment/Enemy_ExperimentBattler.png").convert_alpha()
enemy_sprites = []
for i in range(3):
    for j in range(1):
        enemy_sprites.append(get_enemy_image(i, j, enemy_tileset))


class HomingCircle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 25
        self.r = random.random()
        self.speed = .1 + (2 * self.r)/20
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        enemy.attack_rects.append(self.rect)
        enemy.attackers.append(self)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def update(self):
        global player
        dx, dy = player.x - self.x, player.y - self.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        enemy.attack_rects.append(self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


class BouncingCircle:
    def __init__(self, x, y, slope):
        self.x = x
        self.y = y
        self.slope_x = slope
        self.slope_y = 1
        self.radius = 25
        self.bounced = False
        self.r = random.random()
        self.speed = .3
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        enemy.attack_rects.append(self.rect)
        enemy.attackers.append(self)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def update(self):
        global player
        self.x += self.slope_x * self.speed * dt
        self.y += self.slope_y * self.speed * dt
        if (self.bounced):
            if (self.x >= 715 or self.x <= 260):
                self.slope_x *= -1
            if (self.y >= 565 or self.y <= 210):
                self.slope_y *= -1
        else:
            if (self.x <= 715 and self.x >= 260 and self.y <= 565 and self.y >= 210):
                self.bounced = True

        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        enemy.attack_rects.append(self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)


class Enemy:
    def __init__(self, level_num, starting_x, starting_y):
        self.level_num = level_num
        self.x = starting_x
        self.y = starting_y
        self.starting_x = starting_x
        self.starting_y = starting_x
        self.width = 50
        self.height = 50
        self.image = enemy_sprites[0]

        self.boss = True
        self.attack_counter = 0
        self.last_attack = 0
        self.attack_cooldown = 2000
        self.attack_rects = []
        self.health = 3
        self.attacking = False
        self.attack_start = 0
        self.current_time = 0
        self.r = 0
        self.flip = 1
        self.attackers = []
        self.attack = 0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.image, (self.x, self.y))

    def update(self):
        if Levels.LEVEL_NUMBER != self.level_num and self.level_num != 1:
            self.x = -100
            self.y = -100
        global in_combat
        if Levels.LEVEL_NUMBER == self.level_num:
            self.x = self.starting_x
            self.y = self.starting_y
        self.current_time = pygame.time.get_ticks()
        if (in_combat and self.current_time - self.last_attack >= self.attack_cooldown):
            self.last_attack = self.current_time
            self.attack_start = self.current_time
            self.r = random.randint(0, 100)
            self.flip = random.randint(0, 1)
            if self.flip == 0:
                self.flip = -1

            self.attack = random.randint(1, 3)
            if (self.attack == 1):
                self.attacking = self.LineAttack(self.flip)
            elif (self.attack == 2):
                self.attacking = self.HomingAttack(self.flip)
            elif (self.attack == 3):
                self.attacking = self.BouncingAttack(self.flip)

        if (self.attacking):
            if (self.attack == 1):
                self.attacking = self.LineAttack(self.flip)
            elif (self.attack == 2):
                self.attacking = self.HomingAttack(self.flip)
            elif (self.attack == 3):
                self.attacking = self.BouncingAttack(self.flip)

        global player
        for rect in self.attack_rects:
            if (pygame.Rect.colliderect(player.player_rect, rect)):
                player.damage()

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        screen.blit(self.image, (self.x, self.y))

    def LineAttack(self, flip):
        self.attack_rects.clear()
        self.last_attack = self.current_time
        if (self.current_time - self.attack_start > 3000):
            return False
        s = ((self.current_time - self.attack_start) * (600 / (3000 / 2)))
        self.attack_rect = pygame.Rect(250 + s/10, -600 + s, 100, 600)
        self.attack_rects.append(self.attack_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)
        self.attack_rects.append(self.attack_rect)
        self.attack_rect = pygame.Rect(450 + s/10, -600 + s, 100, 600)
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)
        self.attack_rects.append(self.attack_rect)
        self.attack_rect = pygame.Rect(650 + s/10, -600 + s, 100, 600)
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)

        s = ((self.current_time - self.attack_start) * (1000 / (3000 / 2)))

        self.attack_rect = pygame.Rect(
            (-1000 + s) * self.flip, 500 + s/10, 1000, 100)
        self.attack_rects.append(self.attack_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)
        self.attack_rect = pygame.Rect(
            (-1000 + s) * self.flip, 300 + s/10, 1000, 100)
        self.attack_rects.append(self.attack_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)
        self.attack_rect = pygame.Rect(
            (-1000 + s) * self.flip, 100 + s/10, 1000, 100)
        self.attack_rects.append(self.attack_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)
        return True

    def HomingAttack(self, flip):
        self.attack_rects.clear()
        self.last_attack = self.current_time
        if (self.current_time - self.attack_start > 4000):
            self.attackers.clear()
            return False

        if len(self.attackers) == 0:
            attacker1 = HomingCircle(250, 100)
            attacker2 = HomingCircle(350, 100)
            attacker3 = HomingCircle(450, 100)
            attacker4 = HomingCircle(550, 100)
            attacker5 = HomingCircle(650, 100)
            attacker6 = HomingCircle(100, 300)
            attacker7 = HomingCircle(100, 400)
            attacker8 = HomingCircle(100, 500)
            attacker9 = HomingCircle(850, 300)
            attacker10 = HomingCircle(850, 400)
            attacker11 = HomingCircle(850, 500)
            '''
            attacker22 = HomingCircle(250, 50)
            attacker12 = HomingCircle(350, 50)
            attacker13 = HomingCircle(450, 50)
            attacker14 = HomingCircle(550, 50)
            attacker15 = HomingCircle(650, 50)
            attacker16 = HomingCircle(50, 300)
            attacker17 = HomingCircle(50, 400)
            attacker18 = HomingCircle(50, 500)
            attacker19 = HomingCircle(900, 300)
            attacker20 = HomingCircle(900, 400)
            attacker21 = HomingCircle(900, 500)
            '''
        for attacker in self.attackers:
            attacker.update()
        return True

    def BouncingAttack(self, flip):
        self.attack_rects.clear()
        self.last_attack = self.current_time
        if (self.current_time - self.attack_start > 4000):
            self.attackers.clear()
            return False

        if len(self.attackers) == 0:
            attacker1 = BouncingCircle(100, 100, 1)
            attacker1 = BouncingCircle(150, 75, 1)
            attacker1 = BouncingCircle(200, 50, 1)
            attacker1 = BouncingCircle(250, 25, 1)

            attacker1 = BouncingCircle(900, 100, -1)
            attacker1 = BouncingCircle(850, 75, -1)
            attacker1 = BouncingCircle(800, 50, -1)
            attacker1 = BouncingCircle(750, 25, -1)

        for attacker in self.attackers:
            attacker.update()
        return True


enemy = Enemy(0, 475, 50)


#### ====================================================== COMBAT ====================================================== ####

in_combat = False
bg = 0


def StartCombat():
    '''
    screen.fill((30, 30, 30))
    white_box = pygame.Rect(250, 200, 500, 400)
    pygame.draw.rect(screen, (255, 255, 255), white_box, 5)
    pygame.image.save(screen.copy(), "LEVEL_Combat.png")
    '''
    global in_combat
    in_combat = True

    player.x = 455
    player.y = 410
    player.speed = .3

    current_time = pygame.time.get_ticks()
    enemy.last_attack = current_time
    enemy.x = 175
    enemy.y = 50

    DisplayHealth()
    DisplayProblemBar()
    DrawProblem()

    # position player and enemy
    # stay inside box
    # start fight


def EndCombat():
    enemy.attacking = False
    enemy.attack_rects.clear()
    enemy.attackers.clear()
    health.fill((0, 0, 0))
    problem_bar.fill((0, 0, 0))
    math_screen.fill((0, 0, 0))
    global in_combat
    in_combat = False

    player.x = 500
    player.y = 300
    player.health = 3
    player.ending_combat_time = 0
    player.problems_completed = 0
    player.ending_combat_loss = False
    player.ending_combat_win = False
    player.speed = .2
    enemy.x = 475
    enemy.y = 50


health = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
heart = pygame.image.load("data/Heart/heart.png")
heart = pygame.transform.scale(heart, (TILE_SIZE, TILE_SIZE))

heart_border = pygame.image.load("data/Heart/border.png")
heart_border = pygame.transform.scale(heart_border, (TILE_SIZE, TILE_SIZE))


def DisplayHealth():
    health.fill((0, 0, 0))
    for i in range(player.health):
        health.blit(heart, (260 + i * 50, 145))
    for i in range(3):
        health.blit(heart_border, (260 + i * 50, 145))


problem_bar = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))


def DisplayProblemBar():
    problem_bar.fill((0, 0, 0))
    border_rect = pygame.Rect(850, 150, 50, 450)
    pygame.draw.rect(problem_bar, (255, 255, 255), border_rect, 5)
    inner_rect = pygame.Rect(860, 160 + (430 * ((player.problems_needed - player.problems_completed) / player.problems_needed)),
                             30, 430 - (430 * ((player.problems_needed - player.problems_completed) / player.problems_needed)))
    pygame.draw.rect(problem_bar, (0, 255, 0), inner_rect)


math_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))
dialogue_screen = pygame.surface.Surface((SCREEN_SIZE_X, SCREEN_SIZE_Y))

font = pygame.font.Font('data/m5x7.ttf', 64)

problem_number = 0


def DrawProblem(problem_n=-1):
    global back
    global problem_number
    math_screen.fill((0, 0, 0))
    if problem_n == -1:
        problem_number = random.randint(0, len(problems.problems) - 1)
    else:
        problem_number = problem_n
    text = font.render(problems.problems[problem_number].split("=")[
                       0] + "=", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (1000 // 2, 150 // 2)
    math_screen.blit(text, textRect)
    back = math_screen.copy()


answer = ''


def DrawAnswer():
    math_screen.fill((0, 0, 0))
    DrawProblem(problem_number)
    text = font.render(answer, True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (1000 // 2, 250 // 2)
    math_screen.blit(text, textRect)


def DrawResult(correct):
    text = ''
    if (correct):
        text = font.render("CORRECT", True, (0, 255, 0))
    else:
        text = font.render("WRONG", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.center = (1750 // 2, 200 // 2)
    math_screen.blit(text, textRect)


def CheckAnswer():
    global answer
    if (" " + answer == problems.problems[problem_number].split("=")[1]):
        player.problems_completed += 1
        DrawProblem()
        DrawResult(True)
        DisplayProblemBar()
        answer = ''
        if (player.problems_completed == player.problems_needed):
            player.ending_combat_win = True
            player.ending_combat_time = pygame.time.get_ticks()
    else:
        if (player.problems_completed != 0):
            player.problems_completed += 1
        DrawResult(False)


def DisplayLoss():
    font = pygame.font.Font('data/m5x7.ttf', 256)
    text = font.render("YOU LOSE", True, (255, 100, 0))
    textRect = text.get_rect()
    textRect.center = (1000 // 2, 600 // 2)
    math_screen.blit(text, textRect)


def DisplayWin():
    font = pygame.font.Font('data/m5x7.ttf', 256)
    text = font.render("YOU WIN", True, (0, 255, 10))
    textRect = text.get_rect()
    textRect.center = (1000 // 2, 600 // 2)
    math_screen.blit(text, textRect)

#### ========================================================= UI ========================================================= ####


def ConfirmFight():
    font = pygame.font.Font('data/m5x7.ttf', 128)
    text = font.render("PRESS F TO FIGHT", True, (255, 30, 100))
    textRect = text.get_rect()
    textRect.center = (1000 // 2, 600 // 2)
    dialogue_screen.blit(text, textRect)


def ClearDialogue():
    dialogue_screen.fill((0, 0, 0))


#### ====================================================== GAME LOOP ====================================================== ####

while True:

    dt = clock.tick(60)
    screen.blit(levels[level_number], (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.w_pressed = True
            if event.key == pygame.K_a:
                player.a_pressed = True
            if event.key == pygame.K_s:
                player.s_pressed = True
            if event.key == pygame.K_d:
                player.d_pressed = True
            if event.key == pygame.K_f:
                if (pygame.Rect.colliderect(player.player_rect, enemy.rect)):
                    StartCombat()
                    ChangeLevel(1)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player.w_pressed = False
            if event.key == pygame.K_a:
                player.a_pressed = False
            if event.key == pygame.K_s:
                player.s_pressed = False
            if event.key == pygame.K_d:
                player.d_pressed = False

        if event.type == pygame.KEYDOWN:
            if (in_combat):
                if event.key >= 48 and event.key < 59:
                    answer += str(event.key - 48)
                    DrawAnswer()
                if event.key == pygame.K_BACKSPACE:
                    answer = answer[:-1]
                    DrawAnswer()
                if event.key == pygame.K_RETURN:
                    CheckAnswer()

    if (pygame.Rect.colliderect(player.player_rect, enemy.rect)):
        player.colliding_with_enemy = True
        if (in_combat == False):
            ConfirmFight()

    if (player.colliding_with_enemy and not (pygame.Rect.colliderect(player.player_rect, enemy.rect))):
        player.colliding_with_enemy = False
        ClearDialogue()

    if (in_combat and player.health == 0 and player.ending_combat_loss):
        current_time = pygame.time.get_ticks()
        if (current_time - player.ending_combat_time > 2000):
            EndCombat()
            ChangeLevel(0)
        else:
            answer = ''
            player.w_pressed = False
            player.a_pressed = False
            player.s_pressed = False
            player.d_pressed = False
            DisplayLoss()

    if (in_combat and player.health != 0 and player.ending_combat_win):
        current_time = pygame.time.get_ticks()
        if (current_time - player.ending_combat_time > 2000):
            EndCombat()
            ChangeLevel(0)
        else:
            enemy.attack_rects = []
            enemy.attackers = []
            player.w_pressed = False
            player.a_pressed = False
            player.s_pressed = False
            player.d_pressed = False
            DisplayWin()

    # for i in range(len(solid_tiles)):
        # pygame.draw.rect(screen, (255, 0, 0), solid_tiles[i])
    health.set_colorkey((0, 0, 0))
    problem_bar.set_colorkey((0, 0, 0))
    math_screen.set_colorkey((0, 0, 0))
    dialogue_screen.set_colorkey((0, 0, 0))
    player_screen.set_colorkey((0, 0, 0))
    collision_screen.set_colorkey((0, 0, 0))
    player.update(dt)
    enemy.update()
    if level_number == 2 and player.y > 370:
        house_screen.set_colorkey((0, 0, 0))
        screen.blit(house_screen, (0, 0))

    screen.blit(player_screen, (0, 0))
    screen.blit(health, (0, 0))
    screen.blit(problem_bar, (0, 0))
    screen.blit(math_screen, (0, 0))
    screen.blit(dialogue_screen, (0, 0))
    # screen.blit(collision_screen, (0, 0))
    if level_number == 2 and player.y <= 370:
        house_screen.set_colorkey((0, 0, 0))
        screen.blit(house_screen, (0, 0))

    player_screen.fill((0, 0, 0))
    dialogue_screen.fill((0, 0, 0))
    pygame.display.update()
