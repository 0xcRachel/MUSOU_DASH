import pygame
import os
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

        # Load animations
        self.frames = []
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "charcter")
        try:
            # Load first 4 frames (Idle)
            for i in range(4):
                img = pygame.image.load(os.path.join(base_path, f"animations_{i:03d}.png")).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                self.frames.append(img)
        except Exception as e:
            print(f"Error loading player sprites: {e}")

        self.animation_index = 0
        self.animation_speed = 0.1

    def flap(self):
        self.velocity = FLAP_POWER

    def update(self):
        # Gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Update hit box positon
        self.rect.y = int(self.y)

        # Animation
        if self.frames:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.frames):
                self.animation_index = 0

    def draw(self, screen):
        if self.frames:
            current_frame = self.frames[int(self.animation_index)]
            screen.blit(current_frame, (self.x, self.y))
        else:
            pygame.draw.rect(
                screen,
                PLAYER_COLOR,
                self.rect
            )
