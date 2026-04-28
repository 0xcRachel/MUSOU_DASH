import pygame
import random
from settings import *

SPIKE_COLOR = (255, 0, 0)

class Obstacle:
    def __init__(self, speed=15):
        self.speed = speed
        self.x = float(WIDTH)
        self.width = random.randint(30, 55)
        self.obstacle_type = random.choice(["floor", "ceiling", "middle", "pair"])

        floor_y = HEIGHT - 50

        if self.obstacle_type == "floor":
            # Cột mọc từ đất
            h = random.randint(50, 120)
            self.rects = [
                pygame.Rect(int(self.x), floor_y - h, self.width, h)
            ]

        elif self.obstacle_type == "ceiling":
            # Gai thòng từ trần
            h = random.randint(50, 120)
            self.rects = [
                pygame.Rect(int(self.x), 0, self.width, h)
            ]

        elif self.obstacle_type == "middle":
            # Khối lơ lửng giữa màn hình
            h = random.randint(60, 130)
            mid_y = random.randint(
                HEIGHT // 4,
                HEIGHT - HEIGHT // 4 - h
            )
            self.rects = [
                pygame.Rect(int(self.x), mid_y, self.width, h)
            ]

        elif self.obstacle_type == "pair":
            # Gai đất + trần cùng lúc, chừa khe giữa
            floor_h = random.randint(10, 90)
            ceil_h  = random.randint(50, 90)
            self.rects = [
                pygame.Rect(int(self.x), floor_y - floor_h, self.width, floor_h),
                pygame.Rect(int(self.x), 0, self.width, ceil_h),
            ]

    def update(self):
        self.x -= self.speed
        for r in self.rects:
            r.x = int(self.x)

    def draw(self, screen):
        for r in self.rects:
            pygame.draw.rect(screen, SPIKE_COLOR, r)
            pygame.draw.rect(screen, (180, 0, 0), r, 3)

    def collides_with(self, player_rect):
        return any(player_rect.colliderect(r) for r in self.rects)

    def is_off_screen(self):
        return self.x < -self.width