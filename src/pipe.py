import pygame
import random
from settings import *


class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.gap_y = random.randint(150, HEIGHT - 150)

        # Top pipe
        self.top_rect = pygame.Rect(
            self.x,
            0,
            PIPE_WIDTH,
            self.gap_y - (PIPE_GAP // 2)
        )

        # Bottom pipe
        self.bottom_rect = pygame.Rect(
            self.x,
            self.gap_y + (PIPE_GAP // 2),
            PIPE_WIDTH,
            HEIGHT - (self.gap_y + (PIPE_GAP // 2))
        )

        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            PIPE_COLOR,
            self.top_rect
        )

        pygame.draw.rect(
            screen,
            PIPE_COLOR,
            self.bottom_rect
        )

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

