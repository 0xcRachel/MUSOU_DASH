import pygame
from settings import *


def draw_text(screen, text, size, x, y):
    font = pygame.font.SysFont(None, size)

    text_surface = font.render(
        text,
        True,
        WHITE
    )

    screen.blit(text_surface, (x, y))


def draw_score(screen, score):
    draw_text(
        screen,
        f"Score: {score}",
        35,
        20,
        20
    )


def draw_game_over(screen, score):
    draw_text(
        screen,
        "GAME OVER",
        60,
        250,
        200
    )

    draw_text(
        screen,
        f"Score: {score}",
        40,
        320,
        280
    )

    draw_text(
        screen,
        "Press R to Restart",
        35,
        230,
        350
    )

