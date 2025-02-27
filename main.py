import pygame
import pygame_menu

from sokoban import *


def main():
    pygame.init()
    surface = pygame.display.set_mode((1280, 960))

    def start_the_game():
        game = Sokoban(1)
        game.launch()

    def select_level1():
        game = Sokoban(1)
        game.launch()

    def select_level2():
        game = Sokoban(2)
        game.launch()

    def select_level3():
        game = Sokoban(3)
        game.launch()

    menu = pygame_menu.Menu('Sokoban', 1280, 960,
                            theme=pygame_menu.themes.THEME_GREEN)

    menu.add.button('Play', start_the_game)
    menu.add.button('Level-1', select_level1)
    menu.add.button('Level-2', select_level2)
    menu.add.button('Level-3', select_level3)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)


if __name__ == "__main__":
    main()
