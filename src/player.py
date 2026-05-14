
# pyrefly: ignore [missing-import]
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
        self.hit_frames = []
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "charcter")
        try:
            # Load Idle frames
            for i in range(4):
                img = pygame.image.load(os.path.join(base_path, f"animations_{i:03d}.png")).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                self.frames.append(img)
            
            # Load Hit frames (based on montage identification)
            for i in [32, 48, 52]:
                img = pygame.image.load(os.path.join(base_path, f"animations_{i:03d}.png")).convert_alpha()
                img = pygame.transform.scale(img, (self.width, self.height))
                self.hit_frames.append(img)
        except Exception as e:
            print(f"Error loading player sprites: {e}")

        self.animation_index = 0
        self.animation_speed = 0.1
        self.is_dead = False

    def flap(self):
        if not self.is_dead:
            self.velocity = FLAP_POWER

    def update(self):
        # Gravity
        self.velocity += GRAVITY
        self.y += self.velocity

        # Update hit box positon
        self.rect.y = int(self.y)

        # Animation
        if self.is_dead:
            if self.hit_frames:
                self.animation_index += self.animation_speed
                if self.animation_index >= len(self.hit_frames):
                    self.animation_index = len(self.hit_frames) - 1 # Stay on last frame
        elif self.frames:
            self.animation_index += self.animation_speed
            if self.animation_index >= len(self.frames):
                self.animation_index = 0

    def draw(self, screen):
        current_frames = self.hit_frames if self.is_dead and self.hit_frames else self.frames
        if current_frames:
            idx = int(self.animation_index)
            if idx >= len(current_frames):
                idx = len(current_frames) - 1
            current_frame = current_frames[idx]
            screen.blit(current_frame, (self.x, self.y))
        else:
            pygame.draw.rect(
                screen,
                PLAYER_COLOR,
                self.rect
            )
