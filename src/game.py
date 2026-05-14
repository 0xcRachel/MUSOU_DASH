# pyrefly: ignore [missing-import]
import pygame
from settings import *  
from player import Player
from pipe import Pipe
from ui import draw_score, draw_game_over
import os

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.player = Player()
        self.pipes = []

        self.score = 0
        self.game_over = False

        self.spawn_timer = 0

        # Load background
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "background")
        try:
            self.background_img = pygame.image.load(os.path.join(base_path, "background-night.png")).convert()
            self.background_img = pygame.transform.scale(self.background_img, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background_img = None

        # Load floor
        self.floor_x = 0
        base_path_obs = os.path.join(os.path.dirname(__file__), "..", "assets", "images", "obstacles")
        try:
            self.floor_img = pygame.image.load(os.path.join(base_path_obs, "floor.png")).convert_alpha()
            # Scale floor to match WIDTH and FLOOR_HEIGHT
            self.floor_img = pygame.transform.scale(self.floor_img, (WIDTH, FLOOR_HEIGHT))
        except Exception as e:
            print(f"Error loading floor: {e}")
            self.floor_img = None

    def reset_game(self):
        self.player = Player()
        self.player.is_dead = False
        self.pipes = []

        self.score = 0
        self.game_over = False

        self.spawn_timer = 0

    def check_collision(self):
        # Floor / ceiling collision
        if self.player.y < 0 or self.player.y + PLAYER_HEIGHT > HEIGHT - FLOOR_HEIGHT:
            self.game_over = True
            self.player.is_dead = True

        # Pipe collision
        for pipe in self.pipes:
            if (
                self.player.rect.colliderect(pipe.top_rect)
                or
                self.player.rect.colliderect(pipe.bottom_rect)
            ):
                self.game_over = True
                self.player.is_dead = True

    def update_score(self):
        for pipe in self.pipes:
            if (
                not pipe.passed
                and pipe.x + PIPE_WIDTH < self.player.x
            ):
                pipe.passed = True
                self.score += 1

    def run(self):
        running = True

        while running:
            dt = self.clock.tick(FPS)
            self.spawn_timer += dt

            # Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.player.flap()

                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()

            if not self.game_over:
                # Spawn pipe
                if self.spawn_timer >= PIPE_SPAWN_TIME:
                    self.pipes.append(Pipe())
                    self.spawn_timer = 0

                # Update player
                self.player.update()

                # Update pipes
                for pipe in self.pipes:
                    pipe.update()

                # Remove old pipes
                self.pipes = [
                    pipe for pipe in self.pipes
                    if not pipe.is_off_screen()
                ]

                self.check_collision()
                self.update_score()

                # Update floor scroll
                self.floor_x -= PIPE_SPEED
                if self.floor_x <= -WIDTH:
                    self.floor_x = 0

            # Draw
            if self.background_img:
                self.screen.blit(self.background_img, (0, 0))
            else:
                self.screen.fill(BACKGROUND_COLOR)

            self.player.draw(self.screen)

            for pipe in self.pipes:
                pipe.draw(self.screen)

            # Draw floor
            if self.floor_img:
                self.screen.blit(self.floor_img, (self.floor_x, HEIGHT - FLOOR_HEIGHT))
                self.screen.blit(self.floor_img, (self.floor_x + WIDTH, HEIGHT - FLOOR_HEIGHT))
            else:
                pygame.draw.rect(self.screen, (150, 75, 0), (0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT))

            draw_score(self.screen, self.score)

            if self.game_over:
                draw_game_over(
                    self.screen,
                    self.score
                )

            pygame.display.update()

        pygame.quit()

