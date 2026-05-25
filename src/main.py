import pygame
import sys
from game import Game
from interface.menu import Menu
from config import start_music

# pyrefly: ignore [missing-import]
from settings import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    # Start background music
    start_music()

    while True:
        menu = Menu(screen)
        result = menu.run()

        if result == "play":
            game = Game(screen)
            game.run()
