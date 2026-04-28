import pygame
from settings import *
from score import load_high_score

class Button:
    def __init__(self, text, x, y, width=220, height=55):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, screen):
        color = (80, 80, 120) if self.hovered else (40, 40, 70)
        border_color = (150, 150, 255) if self.hovered else (80, 80, 150)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=10)

        font = pygame.font.SysFont(None, 38)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.state = "main"  # main | highscore | settings

        cx = WIDTH // 2 - 110
        self.buttons = {
            "play":       Button("PLAY",       cx, 220),
            "highscore":  Button("HIGH SCORE", cx, 295),
            "settings":   Button("SETTINGS",   cx, 370),
            "quit":       Button("QUIT",        cx, 445),
        }
        self.back_btn = Button("← BACK", cx, 480, 160, 45)

        # Settings state
        self.volume = 5       # 0-10
        self.difficulty = 1   # 0=Easy 1=Normal 2=Hard

    def run(self):
        """Trả về 'play' hoặc 'quit'"""
        clock = pygame.time.Clock()
        while True:
            clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    result = self._handle_click(mouse_pos)
                    if result in ("play", "quit"):
                        return result

            self._update_hover(mouse_pos)
            self._draw()
            pygame.display.update()

    def _handle_click(self, mouse_pos):
        if self.state == "main":
            if self.buttons["play"].is_clicked(mouse_pos):
                return "play"
            if self.buttons["highscore"].is_clicked(mouse_pos):
                self.state = "highscore"
            if self.buttons["settings"].is_clicked(mouse_pos):
                self.state = "settings"
            if self.buttons["quit"].is_clicked(mouse_pos):
                return "quit"

        elif self.state in ("highscore", "settings"):
            if self.back_btn.is_clicked(mouse_pos):
                self.state = "main"

            if self.state == "settings":
                # Volume
                if pygame.Rect(WIDTH//2 + 30, 260, 36, 36).collidepoint(mouse_pos):
                    self.volume = min(10, self.volume + 1)
                if pygame.Rect(WIDTH//2 - 70, 260, 36, 36).collidepoint(mouse_pos):
                    self.volume = max(0, self.volume - 1)
                # Difficulty
                if pygame.Rect(WIDTH//2 + 30, 330, 36, 36).collidepoint(mouse_pos):
                    self.difficulty = min(2, self.difficulty + 1)
                if pygame.Rect(WIDTH//2 - 70, 330, 36, 36).collidepoint(mouse_pos):
                    self.difficulty = max(0, self.difficulty - 1)

        return None

    def _update_hover(self, mouse_pos):
        if self.state == "main":
            for btn in self.buttons.values():
                btn.check_hover(mouse_pos)
        else:
            self.back_btn.check_hover(mouse_pos)

    def _draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self._draw_title()

        if self.state == "main":
            self._draw_main()
        elif self.state == "highscore":
            self._draw_highscore()
        elif self.state == "settings":
            self._draw_settings()

    def _draw_title(self):
        font_big = pygame.font.SysFont(None, 90)
        font_sub = pygame.font.SysFont(None, 32)
        title = font_big.render("MUSOU DASH", True, (180, 120, 255))
        sub   = font_sub.render("How far can you go?", True, (140, 140, 180))
        self.screen.blit(title, title.get_rect(center=(WIDTH//2, 110)))
        self.screen.blit(sub,   sub.get_rect(center=(WIDTH//2, 170)))

    def _draw_main(self):
        for btn in self.buttons.values():
            btn.draw(self.screen)

    def _draw_highscore(self):
        font = pygame.font.SysFont(None, 50)
        hs = load_high_score()
        lines = [
            ("HIGH SCORE", (200, 200, 100)),
            (f"🏆  {hs}", (255, 255, 255)),
        ]
        for i, (text, color) in enumerate(lines):
            surf = font.render(text, True, color)
            self.screen.blit(surf, surf.get_rect(center=(WIDTH//2, 240 + i * 80)))
        self.back_btn.draw(self.screen)

    def _draw_settings(self):
        font = pygame.font.SysFont(None, 40)
        small = pygame.font.SysFont(None, 32)

        # Volume
        vol_text = font.render(f"Volume:  {self.volume} / 10", True, (255, 255, 255))
        self.screen.blit(vol_text, vol_text.get_rect(center=(WIDTH//2, 270)))
        self._draw_arrow_buttons(WIDTH//2 - 52, 260)

        # Difficulty
        diff_names = ["Easy", "Normal", "Hard"]
        diff_colors = [(100, 255, 100), (255, 200, 50), (255, 80, 80)]
        diff_text = font.render(
            f"Difficulty:  {diff_names[self.difficulty]}",
            True, diff_colors[self.difficulty]
        )
        self.screen.blit(diff_text, diff_text.get_rect(center=(WIDTH//2, 340)))
        self._draw_arrow_buttons(WIDTH//2 - 52, 330)

        hint = small.render("(click ◀ ▶ to change)", True, (120, 120, 150))
        self.screen.blit(hint, hint.get_rect(center=(WIDTH//2, 410)))

        self.back_btn.draw(self.screen)

    def _draw_arrow_buttons(self, base_x, y):
        font = pygame.font.SysFont(None, 36)
        for label, rx in [("◀", base_x - 80), ("▶", base_x + 160)]:
            rect = pygame.Rect(rx, y, 36, 36)
            pygame.draw.rect(self.screen, (60, 60, 100), rect, border_radius=6)
            pygame.draw.rect(self.screen, (120, 120, 200), rect, 2, border_radius=6)
            surf = font.render(label, True, (255, 255, 255))
            self.screen.blit(surf, surf.get_rect(center=rect.center))

    def get_settings(self):
        return {
            "volume": self.volume,
            "difficulty": self.difficulty
        }