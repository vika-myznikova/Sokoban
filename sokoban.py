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
        while self.running:
            self.game_event()
            self.update_game()
            self.update_screen()

    def game_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move = "up"
                elif event.key == pygame.K_DOWN:
                    self.move = "down"
                elif event.key == pygame.K_LEFT:
                    self.move = "left"
                elif event.key == pygame.K_RIGHT:
                    self.move = "right"

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

    def update_move_up(self):
        x, y = self.levels[self.select_level - 1]["player_cord"][0]
        if (x, y - 1) in self.levels[self.select_level - 1]["box"]:
            if ((x, y - 2) not in self.levels[self.select_level - 1]["box"]
                    and self.levels[self.select_level - 1]["map"][y - 2][x] != "#"):
                self.levels[self.select_level - 1]["box"].remove((x, y - 1))
                self.levels[self.select_level - 1]["box"].append((x, y - 2))

        if (self.levels[self.select_level - 1]["map"][y - 1][x] in ["-", "X"]
                and (x, y - 1) not in self.levels[self.select_level - 1]["box"]):
            self.levels[self.select_level - 1]["player_cord"].pop()
            self.levels[self.select_level - 1]["player_cord"].append((x, y - 1))
            self.dir = "up"

    def update_move_down(self):
        x, y = self.levels[self.select_level - 1]["player_cord"][0]
        if (x, y + 1) in self.levels[self.select_level - 1]["box"]:
            if ((x, y + 2) not in self.levels[self.select_level - 1]["box"]
                    and self.levels[self.select_level - 1]["map"][y + 2][x] != "#"):
                self.levels[self.select_level - 1]["box"].remove((x, y + 1))
                self.levels[self.select_level - 1]["box"].append((x, y + 2))
        if (self.levels[self.select_level - 1]["map"][y + 1][x] in ["-", "X"]
                and (x, y + 1) not in self.levels[self.select_level - 1]["box"]):
            self.levels[self.select_level - 1]["player_cord"].pop()
            self.levels[self.select_level - 1]["player_cord"].append((x, y + 1))
            self.dir = "down"

    def update_move_left(self):
        x, y = self.levels[self.select_level - 1]["player_cord"][0]
        if (x - 1, y) in self.levels[self.select_level - 1]["box"]:
            if ((x - 2, y) not in self.levels[self.select_level - 1]["box"]
                    and self.levels[self.select_level - 1]["map"][y][x - 2] != "#"):
                self.levels[self.select_level - 1]["box"].remove((x - 1, y))
                self.levels[self.select_level - 1]["box"].append((x - 2, y))
        if (self.levels[self.select_level - 1]["map"][y][x - 1] in ["-", "X"]
                and (x - 1, y) not in self.levels[self.select_level - 1]["box"]):
            self.levels[self.select_level - 1]["player_cord"].pop()
            self.levels[self.select_level - 1]["player_cord"].append((x - 1, y))
            self.dir = "left"

    def update_move_right(self):
        x, y = self.levels[self.select_level - 1]["player_cord"][0]
        if (x + 1, y) in self.levels[self.select_level - 1]["box"]:

            if ((x + 2, y) not in self.levels[self.select_level - 1]["box"]
                    and self.levels[self.select_level - 1]["map"][y][x + 2] != "#"):
                self.levels[self.select_level - 1]["box"].remove((x + 1, y))
                self.levels[self.select_level - 1]["box"].append((x + 2, y))

        if (self.levels[self.select_level - 1]["map"][y][x + 1] in ["-", "X"]
                and (x + 1, y) not in self.levels[self.select_level - 1]["box"]):
            self.levels[self.select_level - 1]["player_cord"].pop()
            self.levels[self.select_level - 1]["player_cord"].append((x + 1, y))
            self.dir = "right"

    def update_screen(self):
        self.screen.fill(BACKGROUND)
        self.update_board()
        pygame.display.flip()

    def update_board(self):
        self.draw_board()
        self.print_level()

    def draw_board(self):
        start_x = (WIDTH - self.get_row() * IMAGE_SIZE) // 2
        start_y = (HEIGHT - len(self.levels[self.select_level - 1]["map"]) * IMAGE_SIZE) // 2
        i, j = 0, 0
        for y in range(start_y, start_y + len(self.levels[self.select_level - 1]["map"]) * IMAGE_SIZE, IMAGE_SIZE):

            for x in range(start_x, start_x + len(self.levels[self.select_level - 1]["map"][j]) * IMAGE_SIZE,
                           IMAGE_SIZE):
                s = self.levels[self.select_level - 1]["map"][j][i]
                if s == "#":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.wall_img, (x, y))
                elif s == "-":
                    self.screen.blit(self.floor_img, (x, y))
                elif s == "X":
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.point_img, (x, y))
                if (i, j) in self.levels[self.select_level - 1]["player_cord"]:
                    if self.dir == "down":
                        self.screen.blit(self.down_img, (x, y))
                    elif self.dir == "up":
                        self.screen.blit(self.up_img, (x, y))
                    elif self.dir == "left":
                        self.screen.blit(self.left_img, (x, y))
                    elif self.dir == "right":
                        self.screen.blit(self.right_img, (x, y))
                if (i, j) in self.levels[self.select_level - 1]["box"]:
                    self.screen.blit(self.floor_img, (x, y))
                    self.screen.blit(self.box_img, (x, y))
                i += 1
            i = 0
            j += 1

    def get_row(self):
        return max([len(line) for line in self.levels[self.select_level - 1]["map"]])

    def print_level(self):
        ...

    def __del__(self):
        pygame.quit()
