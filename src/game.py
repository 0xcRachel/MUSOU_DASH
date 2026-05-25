import pygame
import sys
import os
import json

# pyrefly: ignore [missing-import]
from settings import *
from player import Player
from pipe import Pipe
from ui import draw_score, draw_game_over


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        self.player = Player()
        self.pipes = []

        self.score = 0
        self.game_over = False
        self.spawn_timer = 0

        # Load background
        base_path = os.path.join(
            os.path.dirname(__file__), "..", "assets", "images", "background"
        )
        try:
            self.background_img = pygame.image.load(
                os.path.join(base_path, "background-night.png")
            ).convert()
            self.background_img = pygame.transform.scale(
                self.background_img, (WIDTH, HEIGHT)
            )
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background_img = None

        # Load floor
        self.floor_x = 0
        base_path_obs = os.path.join(
            os.path.dirname(__file__), "..", "assets", "images", "obstacles"
        )
        try:
            self.floor_img = pygame.image.load(
                os.path.join(base_path_obs, "floor.png")
            ).convert_alpha()
            self.floor_img = pygame.transform.scale(
                self.floor_img, (WIDTH, FLOOR_HEIGHT)
            )
        except Exception as e:
            print(f"Error loading floor: {e}")
            self.floor_img = None

        # Load game over sound
        base_sounds = os.path.join(
            os.path.dirname(__file__), "..", "assets", "sounds"
        )
        try:
            self.game_over_sound = pygame.mixer.Sound(
                os.path.join(base_sounds, "game_over.mp3")
            )
        except Exception as e:
            print(f"Error loading game over sound: {e}")
            self.game_over_sound = None

        # Load point sound
        try:
            self.point_sound = pygame.mixer.Sound(
                os.path.join(base_sounds, "point.mp3")
            )
        except Exception as e:
            print(f"Error loading point sound: {e}")
            self.point_sound = None

    # ------------------------------------------------------------------ helpers
    def reset_game(self):
        self.player = Player()
        self.player.is_dead = False
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.spawn_timer = 0

    def check_collision(self):
        if self.player.y < 0 or self.player.y + PLAYER_HEIGHT > HEIGHT - FLOOR_HEIGHT:
            self.game_over = True
            self.player.is_dead = True

        for pipe in self.pipes:
            if (
                self.player.rect.colliderect(pipe.top_rect)
                or self.player.rect.colliderect(pipe.bottom_rect)
            ):
                self.game_over = True
                self.player.is_dead = True

    def update_score(self):
        for pipe in self.pipes:
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.player.x:
                pipe.passed = True
                self.score += 1
                # Play point sound
                if self.point_sound and pygame.mixer.get_init():
                    from config import load_settings
                    settings = load_settings()
                    if not settings.get("muted", False):
                        self.point_sound.set_volume(settings.get("volume", 0.5))
                        self.point_sound.play()

    def _save_score(self):
        """Append the current score to scores.json, keeping only top-3."""
        path = os.path.join(os.path.dirname(__file__), "..", "scores.json")
        try:
            with open(path) as f:
                scores = json.load(f)
        except Exception:
            scores = []

        scores.append(self.score)
        scores = sorted(scores, reverse=True)[:3]

        with open(path, "w") as f:
            json.dump(scores, f)

    # ------------------------------------------------------------------ main loop
    def run(self):
        """Run the game loop. Returns 'menu' or 'quit'."""
        score_saved = False
        running = True

        while running:
            dt = self.clock.tick(FPS)
            self.spawn_timer += dt

            # ---- Events ----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.player.flap()

                    if self.game_over:
                        if event.key == pygame.K_r:
                            score_saved = False
                            self.reset_game()
                            if pygame.mixer.get_init():
                                pygame.mixer.music.unpause()
                        if event.key == pygame.K_m:
                            if pygame.mixer.get_init():
                                pygame.mixer.music.unpause()
                            return "menu"

            # ---- Update (only when alive) ----
            if not self.game_over:
                if self.spawn_timer >= PIPE_SPAWN_TIME:
                    self.pipes.append(Pipe())
                    self.spawn_timer = 0

                self.player.update()

                for pipe in self.pipes:
                    pipe.update()

                self.pipes = [p for p in self.pipes if not p.is_off_screen()]

                self.check_collision()
                self.update_score()

                self.floor_x -= PIPE_SPEED
                if self.floor_x <= -WIDTH:
                    self.floor_x = 0

            else:
                # Save score once when game ends
                if not score_saved:
                    self._save_score()
                    score_saved = True
                    # Pause background music and play game over sound
                    if pygame.mixer.get_init():
                        try:
                            pygame.mixer.music.pause()
                            if self.game_over_sound:
                                from config import load_settings
                                settings = load_settings()
                                if not settings.get("muted", False):
                                    self.game_over_sound.set_volume(settings.get("volume", 0.5))
                                    self.game_over_sound.play()
                        except Exception as e:
                            print(f"Error playing game over sound: {e}")

            # ---- Draw ----
            if self.background_img:
                self.screen.blit(self.background_img, (0, 0))
            else:
                self.screen.fill(BACKGROUND_COLOR)

            self.player.draw(self.screen)

            for pipe in self.pipes:
                pipe.draw(self.screen)

            if self.floor_img:
                self.screen.blit(self.floor_img, (self.floor_x, HEIGHT - FLOOR_HEIGHT))
                self.screen.blit(
                    self.floor_img, (self.floor_x + WIDTH, HEIGHT - FLOOR_HEIGHT)
                )
            else:
                pygame.draw.rect(
                    self.screen,
                    (150, 75, 0),
                    (0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT),
                )

            draw_score(self.screen, self.score)

            if self.game_over:
                draw_game_over(self.screen, self.score)

            pygame.display.update()

        return "quit"
