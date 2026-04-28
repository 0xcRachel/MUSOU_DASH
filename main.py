import pygame

pygame.init()

# Window settings
WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Musou Dash")

clock = pygame.time.Clock()

# Player settings
player_x = 150
player_y = 250
player_width = 50
player_height = 50

velocity = 0
gravity = 0.5
jump_strength = -10

running = True

while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = jump_strength

    # Gravity
    velocity += gravity
    player_y += velocity

    # Floor / ceiling limit
    if player_y < 0:
        player_y = 0

    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height
        velocity = 0

    # Draw
    screen.fill((20, 20, 30))

    player = pygame.Rect(
        player_x,
        int(player_y),
        player_width,
        player_height
    )

    pygame.draw.rect(screen, (255, 255, 255), player)

    pygame.display.update()

pygame.quit()
