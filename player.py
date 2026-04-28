import pygame
from settings import *

class Player:
    def __init__(self):
        self.x = PLAYER_X
        self.y = PLAYER_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.velocity = 0
        
        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        # Gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Ceiling limit
        if self.y < 0:
            self.y = 0

        # Floor limit
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.velocity = 0

        self.rect.y = int(self.y)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            PLAYER_COLOR,
            self.rect
        )
