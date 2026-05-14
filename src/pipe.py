import pygame
import random
import os
from settings import *


class Pipe:
    PIPE_IMG_TOP = None
    PIPE_IMG_BOTTOM = None

    def __init__(self):
        # Lazy load images once after pygame.display.set_mode is called
        if Pipe.PIPE_IMG_TOP is None:
            base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "obstacles")
            try:
                original_img = pygame.image.load(os.path.join(base_path, "prs_000.png")).convert_alpha()
                aspect_ratio = original_img.get_height() / original_img.get_width()
                scaled_width = PIPE_WIDTH
                scaled_height = int(scaled_width * aspect_ratio)
                
                Pipe.PIPE_IMG_BOTTOM = pygame.transform.scale(original_img, (scaled_width, scaled_height))
                Pipe.PIPE_IMG_TOP = pygame.transform.flip(Pipe.PIPE_IMG_BOTTOM, False, True)
            except Exception as e:
                print(f"Error loading pipe images: {e}")
                # Set to something non-None to avoid repeating error
                Pipe.PIPE_IMG_TOP = False 
                Pipe.PIPE_IMG_BOTTOM = False
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

        # Pre-scale images for this specific pipe instance to save performance
        if isinstance(Pipe.PIPE_IMG_TOP, pygame.Surface) and isinstance(Pipe.PIPE_IMG_BOTTOM, pygame.Surface):
            self.top_surface = pygame.transform.scale(Pipe.PIPE_IMG_TOP, (self.top_rect.width, self.top_rect.height))
            self.bottom_surface = pygame.transform.scale(Pipe.PIPE_IMG_BOTTOM, (self.bottom_rect.width, self.bottom_rect.height))
        else:
            self.top_surface = None
            self.bottom_surface = None

    def update(self):
        self.x -= PIPE_SPEED

        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, screen):
        if self.top_surface and self.bottom_surface:
            screen.blit(self.top_surface, self.top_rect)
            screen.blit(self.bottom_surface, self.bottom_rect)
        else:
            pygame.draw.rect(screen, PIPE_COLOR, self.top_rect)
            pygame.draw.rect(screen, PIPE_COLOR, self.bottom_rect)

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

