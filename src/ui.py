import pygame
from settings import *


def _draw_outlined_text(surface, text, font, text_color, outline_color, x, y):
    """Draw text with a thick outline."""
    # Render outline by rendering text at offset positions
    offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2),
               (-2, 0), (2, 0), (0, -2), (0, 2)]
    
    for ox, oy in offsets:
        out_surf = font.render(text, True, outline_color)
        surface.blit(out_surf, (x + ox, y + oy))
        
    # Render main text
    in_surf = font.render(text, True, text_color)
    surface.blit(in_surf, (x, y))
    return in_surf.get_width(), in_surf.get_height()


def draw_score(screen, score):
    """Draw the current score at the top center during gameplay."""
    font = pygame.font.SysFont("impact", 50)
    text = str(score)
    
    # Calculate position (top center)
    # Get dimensions roughly by rendering
    surf = font.render(text, True, WHITE)
    w, h = surf.get_size()
    x = WIDTH // 2 - w // 2
    y = int(HEIGHT * 0.1)
    
    _draw_outlined_text(screen, text, font, WHITE, (50, 50, 50), x, y)


def draw_game_over(screen, score):
    """Draw the game over overlay, score panel, and instructions."""
    # 1. Dim background
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    # Fonts
    font_title = pygame.font.SysFont("impact", 64)
    font_sub = pygame.font.SysFont("impact", 32)
    font_small = pygame.font.SysFont(None, 28)
    
    DARK = (50, 50, 50)
    
    # 2. "GAME OVER" Title
    title_txt = "GAME OVER"
    t_surf = font_title.render(title_txt, True, WHITE)
    tx = WIDTH // 2 - t_surf.get_width() // 2
    ty = int(HEIGHT * 0.25)
    _draw_outlined_text(screen, title_txt, font_title, (255, 100, 50), WHITE, tx, ty)
    
    # 3. Score Panel
    panel_w, panel_h = 240, 120
    px = WIDTH // 2 - panel_w // 2
    py = int(HEIGHT * 0.45)
    
    # Draw panel shadow and body
    rect_shadow = pygame.Rect(px + 4, py + 4, panel_w, panel_h)
    rect_body = pygame.Rect(px, py, panel_w, panel_h)
    
    pygame.draw.rect(screen, (80, 80, 80), rect_shadow, border_radius=12)
    pygame.draw.rect(screen, (220, 215, 200), rect_body, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), rect_body, width=4, border_radius=12)
    pygame.draw.rect(screen, DARK, rect_body, width=2, border_radius=12)
    
    # 4. Score Texts inside Panel
    lbl_score = font_sub.render("SCORE", True, (200, 100, 50))
    val_score = font_title.render(str(score), True, WHITE)
    
    screen.blit(lbl_score, (px + panel_w // 2 - lbl_score.get_width() // 2, py + 15))
    
    # Draw value with outline
    vx = px + panel_w // 2 - val_score.get_width() // 2
    vy = py + 45
    _draw_outlined_text(screen, str(score), font_title, WHITE, DARK, vx, vy)
    
    # 5. Instructions
    inst_txt = "[ R ] RESTART    |    [ M ] MENU"
    ix = WIDTH // 2 - font_sub.render(inst_txt, True, WHITE).get_width() // 2
    iy = int(HEIGHT * 0.75)
    _draw_outlined_text(screen, inst_txt, font_sub, WHITE, DARK, ix, iy)
