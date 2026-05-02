import pygame
from settings import *
from player import Player
from pipe import Pipe
from ui import draw_score, draw_game_over


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

    def reset_game(self):
        self.player = Player()
        self.pipes = []

        self.score = 0
        self.game_over = False

        self.spawn_timer = 0

    def check_collision(self):
        # Floor / ceiling collision
        if self.player.y < 0 or self.player.y > HEIGHT:
            self.game_over = True

        # Pipe collision
        for pipe in self.pipes:
            if (
                self.player.rect.colliderect(pipe.top_rect)
                or
                self.player.rect.colliderect(pipe.bottom_rect)
            ):
                self.game_over = True

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

            # Draw
            self.screen.fill(BACKGROUND_COLOR)

            self.player.draw(self.screen)

            for pipe in self.pipes:
                pipe.draw(self.screen)

            draw_score(self.screen, self.score)

            if self.game_over:
                draw_game_over(
                    self.screen,
                    self.score
                )

            pygame.display.update()

        pygame.quit()

