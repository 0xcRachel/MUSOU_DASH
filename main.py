import pygame
from settings import *
from player import Player
from obstacle import Obstacle
from score import load_high_score, save_high_score

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Musou Dash")
clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def calc_speed(score):
    # Tăng cấp số nhân: speed = 5 * 1.0008^score
    return 5 * (1.0008 ** score)

def calc_spawn_delay(score):
    # Giảm dần tối thiểu 400ms
    return max(400, int(1500 * (0.9992 ** score)))

def reset_game():
    return Player(), [], 0, 0, 1500, set()

high_score = load_high_score()
player, obstacles, score, score_timer, spawn_delay, passed_obs = reset_game()
spawn_timer = 0
game_over = False
running = True

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                player.jump()
            if game_over and event.key == pygame.K_r:
                high_score = save_high_score(score)
                player, obstacles, score, score_timer, spawn_delay, passed_obs = reset_game()
                spawn_timer = 0
                game_over = False

    if not game_over:
        # Score theo thời gian
        score_timer += dt
        if score_timer >= 100:
            score += 1
            score_timer = 0

        # Spawn delay và speed tính từ score
        spawn_delay = calc_spawn_delay(score)
        current_speed = calc_speed(score)

        spawn_timer += dt
        if spawn_timer >= spawn_delay:
            obstacles.append(Obstacle(speed=current_speed))
            spawn_timer = 0

        player.update()

        for obstacle in obstacles:
            obstacle.speed = current_speed
            obstacle.update()

        # Thưởng +10 vượt obstacle
        for obstacle in obstacles:
            obs_id = id(obstacle)
            if obs_id not in passed_obs:
                if obstacle.x + obstacle.width < player.rect.left:
                    score += 10
                    passed_obs.add(obs_id)

        obstacles = [o for o in obstacles if not o.is_off_screen()]
        passed_obs = {i for i in passed_obs if i in {id(o) for o in obstacles}}

        for obstacle in obstacles:
            if obstacle.collides_with(player.rect):
                game_over = True
                high_score = save_high_score(score)

    # Draw
    screen.fill(BACKGROUND_COLOR)
    player.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)

    draw_text(screen, f"SCORE: {score}", 40, 20, 20)
    draw_text(screen, f"BEST: {high_score}", 35, 20, 60, (200, 200, 100))

    if game_over:
        draw_text(screen, "GAME OVER", 80, 230, 220)
        draw_text(screen, f"SCORE: {score}", 50, 300, 310)
        draw_text(screen, f"BEST:  {high_score}", 50, 300, 360, (200, 200, 100))
        draw_text(screen, "Press R to restart", 35, 270, 420, (180, 180, 180))

    pygame.display.update()

pygame.quit()