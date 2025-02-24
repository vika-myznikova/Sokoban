from copy import deepcopy

import pygame

from sokoban_settings import *


class Sokoban:

    def __init__(self):
        pygame.init()
        self.init_screen()
        self.init_images()
        self.init_sounds()
        self.levels = self.load_levels()
        self.select_level = 1
        self.victory = False
        self.dir = "down"
        self.move = None
        self.running = True

    def init_screen(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sokoban")
        icon = pygame.image.load("data/images/icon.png")
        pygame.display.set_icon(icon)

    def init_images(self):
        self.wall_img = pygame.image.load("data/images/wall.png").convert_alpha()
        self.wall_img = pygame.transform.smoothscale(self.wall_img, (IMAGE_SIZE, IMAGE_SIZE))

        self.point_img = pygame.image.load("data/images/point.png").convert_alpha()
        self.point_img = pygame.transform.smoothscale(self.point_img, (IMAGE_SIZE, IMAGE_SIZE))

        self.floor_img = pygame.image.load("data/images/floor.png").convert_alpha()
        self.floor_img = pygame.transform.smoothscale(self.floor_img, (IMAGE_SIZE, IMAGE_SIZE))

        self.up_img = pygame.image.load("data/images/up.png").convert_alpha()
        self.up_img = pygame.transform.smoothscale(self.up_img, (IMAGE_SIZE, IMAGE_SIZE))

        self.down_img = pygame.image.load("data/images/down.png").convert_alpha()
        self.down_img = pygame.transform.smoothscale(self.down_img, (IMAGE_SIZE, IMAGE_SIZE))

        self.right_img = pygame.image.load("data/images/right.png").convert_alpha()
        self.right_img = pygame.transform.smoothscale(self.right_img, (IMAGE_SIZE, IMAGE_SIZE))

        self.left_img = pygame.image.load("data/images/left.png").convert_alpha()
        self.left_img = pygame.transform.smoothscale(self.left_img, (IMAGE_SIZE, IMAGE_SIZE))

        self.box_img = pygame.image.load("data/images/box.png").convert_alpha()
        self.box_img = pygame.transform.smoothscale(self.box_img, (IMAGE_SIZE, IMAGE_SIZE))

    def init_sounds(self):
        pygame.mixer.init()
        self.music = pygame.mixer.Sound("data/sounds/music.mp3")
        self.music.set_volume(0.1)
        self.music.play()

        self.step = pygame.mixer.Sound("data/sounds/step.mp3")
        self.step.set_volume(0.2)

    def load_levels(self):
        with open(FILE_LEVEL) as file:
            levels = []
            for line in file:
                line = line.rstrip()
                if line:
                    if line.startswith("level"):
                        level = {"map": [], "player_cord": [], "box": []}
                    elif line.startswith("P: "):
                        x, y = map(int, line[3:].split(","))
                        level["player_cord"].append((x, y))
                    elif line.startswith("C: "):
                        crates = line[3:].split()
                        for crate in crates:
                            x, y = map(int, crate.split(","))
                            level["box"].append((x, y))
                    elif line == "end":
                        levels.append(level)
                    else:
                        level["map"].append(line)
            return tuple(levels)

    def launch(self):
        self.level_copy = self.copy_level()
        while self.running:
            self.game_event()
            self.update_game()
            self.update_screen()

    def copy_level(self):
        level_copy = deepcopy(self.levels[self.select_level - 1])
        return level_copy

    def game_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.victory:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.select_level < len(self.levels):
                        self.select_level += 1

                    self.level_copy = self.copy_level()
                    self.victory = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move = "up"
                    elif event.key == pygame.K_DOWN:
                        self.move = "down"
                    elif event.key == pygame.K_LEFT:
                        self.move = "left"
                    elif event.key == pygame.K_RIGHT:
                        self.move = "right"
                    elif event.key == pygame.K_ESCAPE:
                        self.dir = "down"
                        self.level_copy = self.copy_level()

    def update_game(self):
        if self.move:
            self.step.play()
            if self.move == "up":
                self.update_move_up()
            elif self.move == "down":
                self.update_move_down()
            elif self.move == "left":
                self.update_move_left()
            elif self.move == "right":
                self.update_move_right()
            self.move = None
            self.check_results()

    def update_move_up(self):
        x, y = self.level_copy["player_cord"][0]
        if (x, y - 1) in self.level_copy["box"]:
            if ((x, y - 2) not in self.level_copy["box"]
                    and self.level_copy["map"][y - 2][x] != "#"):
                self.level_copy["box"].remove((x, y - 1))
                self.level_copy["box"].append((x, y - 2))

        if (self.level_copy["map"][y - 1][x] in ["-", "X"]
                and (x, y - 1) not in self.level_copy["box"]):
            self.level_copy["player_cord"].pop()
            self.level_copy["player_cord"].append((x, y - 1))
            self.dir = "up"

    def update_move_down(self):
        x, y = self.level_copy["player_cord"][0]
        if (x, y + 1) in self.level_copy["box"]:
            if ((x, y + 2) not in self.level_copy["box"]
                    and self.level_copy["map"][y + 2][x] != "#"):
                self.level_copy["box"].remove((x, y + 1))
                self.level_copy["box"].append((x, y + 2))
        if (self.level_copy["map"][y + 1][x] in ["-", "X"]
                and (x, y + 1) not in self.level_copy["box"]):
            self.level_copy["player_cord"].pop()
            self.level_copy["player_cord"].append((x, y + 1))
            self.dir = "down"

    def update_move_left(self):
        x, y = self.level_copy["player_cord"][0]
        if (x - 1, y) in self.level_copy["box"]:
            if ((x - 2, y) not in self.level_copy["box"]
                    and self.level_copy["map"][y][x - 2] != "#"):
                self.level_copy["box"].remove((x - 1, y))
                self.level_copy["box"].append((x - 2, y))
        if (self.level_copy["map"][y][x - 1] in ["-", "X"]
                and (x - 1, y) not in self.level_copy["box"]):
            self.level_copy["player_cord"].pop()
            self.level_copy["player_cord"].append((x - 1, y))
            self.dir = "left"

    def update_move_right(self):
        x, y = self.level_copy["player_cord"][0]
        if (x + 1, y) in self.level_copy["box"]:

            if ((x + 2, y) not in self.level_copy["box"]
                    and self.level_copy["map"][y][x + 2] != "#"):
                self.level_copy["box"].remove((x + 1, y))
                self.level_copy["box"].append((x + 2, y))

        if (self.level_copy["map"][y][x + 1] in ["-", "X"]
                and (x + 1, y) not in self.level_copy["box"]):
            self.level_copy["player_cord"].pop()
            self.level_copy["player_cord"].append((x + 1, y))
            self.dir = "right"

    def check_results(self):
        self.victory = True
        for y in range(len(self.level_copy["map"])):
            for x in range(len(self.level_copy["map"][y])):
                if self.level_copy["map"][y][x] == "X" and (x, y) not in self.level_copy["box"]:
                    self.victory = False

    def update_screen(self):
        self.screen.fill(BACKGROUND)
        background_text = ["Esc - перезапуск уровня", ]

        for line in background_text:
            font = pygame.font.Font(None, 50)
            text_coord = 50
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 0
            intro_rect.top = text_coord
            intro_rect.x = 50
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        self.update_board()
        if self.victory:
            self.draw_victory()
        pygame.display.flip()

    def update_board(self):
        self.draw_board()

    def draw_board(self):
        start_x = (WIDTH - self.get_row() * IMAGE_SIZE) // 2
        start_y = (HEIGHT - len(self.level_copy["map"]) * IMAGE_SIZE) // 2
        i, j = 0, 0
        for y in range(start_y, start_y + len(self.level_copy["map"]) * IMAGE_SIZE, IMAGE_SIZE):

            for x in range(start_x, start_x + len(self.level_copy["map"][j]) * IMAGE_SIZE,
                           IMAGE_SIZE):
                s = self.level_copy["map"][j][i]
                if s == "#":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.wall_img, (x, y))
                elif s == "-":
                    self.screen.blit(self.floor_img, (x, y))
                elif s == "X":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.point_img, (x, y))
                if (i, j) in self.level_copy["player_cord"]:
                    if self.dir == "down":
                        self.screen.blit(self.down_img, (x, y))
                    elif self.dir == "up":
                        self.screen.blit(self.up_img, (x, y))
                    elif self.dir == "left":
                        self.screen.blit(self.left_img, (x, y))
                    elif self.dir == "right":
                        self.screen.blit(self.right_img, (x, y))
                if (i, j) in self.level_copy["box"]:
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.box_img, (x, y))
                i += 1
            i = 0
            j += 1

    def get_row(self):
        return max([len(line) for line in self.levels[self.select_level - 1]["map"]])

    def draw_victory(self):
        text_1 = ["Вы выиграли!"]
        text_2 = ["Для продолжения нажмите enter"]
        fon = pygame.transform.scale(pygame.image.load("data/images/fon.jpeg"), (WIDTH, HEIGHT))
        self.screen.blit(fon, (0, 0))

        for line in text_1:
            font = pygame.font.Font(None, 250)
            text_coord = 50
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 0
            intro_rect.top = text_coord
            intro_rect.x = 50
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        for line in text_2:
            font = pygame.font.Font(None, 50)
            text_coord = 50
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coord += 150
            intro_rect.top = text_coord
            intro_rect.x = 60
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

    def __del__(self):
        pygame.quit()

