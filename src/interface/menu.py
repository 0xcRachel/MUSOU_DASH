import pygame
import sys
import os
import json
import math

# pyrefly: ignore [missing-import]
from settings import *


# ───────────────────────────────────────────────────────────────────────────────
#  Colours (Flappy-Bird palette)
# ───────────────────────────────────────────────────────────────────────────────
SKY_TOP    = (78,  192, 202)   # teal sky
SKY_BOT    = (113, 213, 222)   # lighter at horizon
WHITE      = (255, 255, 255)
DARK       = (30,  30,  30)
PANEL_BG   = (240, 240, 230)   # off-white panel
PANEL_BDR  = (190, 185, 168)   # panel border (bottom shadow)
PANEL_TOP  = (255, 255, 255)   # panel top highlight
BTN_GREEN  = (111, 196, 68)
BTN_GRN_DK = (83,  165, 51)
BTN_ORANGE = (219, 126, 30)
BTN_ORG_DK = (180, 100, 20)
GOLD       = (255, 200, 0)
GOLD_DK    = (200, 140, 0)
TXT_YEL    = (236, 180, 0)
TXT_ORG    = (255, 130, 0)


def _draw_outlined_text(surface, text, font, color, outline_color, cx, cy, outline=4):
    """Draw text with a solid pixel-art outline (draws outline first, then main)."""
    surf = font.render(text, True, color)
    out  = font.render(text, True, outline_color)
    ox   = cx - surf.get_width() // 2
    oy   = cy - surf.get_height() // 2
    for dx in range(-outline, outline + 1):
        for dy in range(-outline, outline + 1):
            if dx != 0 or dy != 0:
                surface.blit(out, (ox + dx, oy + dy))
    surface.blit(surf, (ox, oy))


def _draw_panel_button(surface, rect, font, text, txt_color, panel_color, border_color,
                        shadow_color, hovered=False):
    """Flappy-Bird style white-panel button with bottom shadow."""
    shadow_h = 5
    # Shadow
    shadow_rect = pygame.Rect(rect.x, rect.y + shadow_h, rect.w, rect.h)
    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=10)
    # Body (shifts up when hovered to simulate press)
    body_rect = pygame.Rect(rect.x, rect.y + (shadow_h if not hovered else shadow_h + 2),
                             rect.w, rect.h - shadow_h)
    pygame.draw.rect(surface, panel_color, body_rect, border_radius=10)
    # Top highlight line
    pygame.draw.rect(surface, border_color, body_rect, 2, border_radius=10)
    # Label
    label = font.render(text, True, txt_color)
    lx = body_rect.centerx - label.get_width() // 2
    ly = body_rect.centery - label.get_height() // 2
    surface.blit(label, (lx, ly))


def _draw_icon_button(surface, rect, icon_surf, panel_color, border_color,
                       shadow_color, hovered=False):
    """Flappy-Bird style white-panel button with an icon image."""
    shadow_h = 5
    shadow_rect = pygame.Rect(rect.x, rect.y + shadow_h, rect.w, rect.h)
    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=10)
    body_rect = pygame.Rect(rect.x, rect.y + (shadow_h if not hovered else shadow_h + 2),
                             rect.w, rect.h - shadow_h)
    pygame.draw.rect(surface, panel_color, body_rect, border_radius=10)
    pygame.draw.rect(surface, border_color, body_rect, 2, border_radius=10)
    if icon_surf:
        ix = body_rect.centerx - icon_surf.get_width() // 2
        iy = body_rect.centery - icon_surf.get_height() // 2
        surface.blit(icon_surf, (ix, iy))


class Menu:
    FLOOR_H = 80   # height of the floor strip drawn in the menu

    def __init__(self, screen):
        self.screen = screen
        self.clock  = pygame.time.Clock()
        self.tick   = 0

        # ── Fonts ────────────────────────────────────────────────────────────
        self.font_title  = pygame.font.SysFont("impact", 90)
        self.font_sub    = pygame.font.SysFont(None, 32)
        self.font_btn    = pygame.font.SysFont("impact", 36)
        self.font_small  = pygame.font.SysFont(None, 26)
        self.font_icon   = pygame.font.SysFont("segoeuisymbol,arial", 56)   # for ▶ ⚙ icons

        # ── Background ───────────────────────────────────────────────────────
        base_bg = os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "images", "background"
        )
        try:
            self.bg = pygame.image.load(
                os.path.join(base_bg, "background-night.png")
            ).convert()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Menu: could not load background – {e}")
            self.bg = None

        # ── Floor ────────────────────────────────────────────────────────────
        base_obs = os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "images", "obstacles"
        )
        self.floor_x = 0
        try:
            self.floor_img = pygame.image.load(
                os.path.join(base_obs, "floor.png")
            ).convert_alpha()
            self.floor_img = pygame.transform.scale(self.floor_img, (WIDTH, self.FLOOR_H))
        except Exception as e:
            print(f"Menu: could not load floor – {e}")
            self.floor_img = None

        # ── Character sprite (first animation frame) ─────────────────────────
        base_char = os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "images", "charcter"
        )
        try:
            raw = pygame.image.load(
                os.path.join(base_char, "animations_000.png")
            ).convert_alpha()
            # Scale to a nice menu size
            ch = 90
            cw = int(raw.get_width() * ch / raw.get_height())
            self.char_surf = pygame.transform.scale(raw, (cw, ch))
        except Exception as e:
            print(f"Menu: could not load character – {e}")
            self.char_surf = None

        # ── Settings ─────────────────────────────────────────────────────────
        from config import load_settings
        self.menu_state      = "main"
        self.settings        = load_settings()
        self.dragging_slider = False

        # ── Layout ───────────────────────────────────────────────────────────
        # Main menu: two big icon buttons side by side (Play | Settings)
        btn_w, btn_h = 160, 100
        gap          = 30
        total_w      = btn_w * 2 + gap
        left_x       = WIDTH // 2 - total_w // 2
        btn_y        = HEIGHT - self.FLOOR_H - btn_h - 50   # sit just above floor

        self.btn_play     = pygame.Rect(left_x,            btn_y, btn_w, btn_h)
        self.btn_settings = pygame.Rect(left_x + btn_w + gap, btn_y, btn_w, btn_h)

        # Settings page rects
        self.slider_rect = pygame.Rect(WIDTH // 2 - 140, 260, 280, 18)
        self.btn_mute    = pygame.Rect(WIDTH // 2 - 140, 310, 280, 54)
        self.btn_back    = pygame.Rect(WIDTH // 2 - 140, 395, 280, 54)

        self.best_score = self._load_best_score()

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _load_best_score(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "scores.json")
        try:
            with open(path) as f:
                data = json.load(f)
            return max(data) if data else 0
        except Exception:
            return 0

    def _get_knob_x(self):
        volume = self.settings.get("volume", 0.5)
        return self.slider_rect.left + int(volume * self.slider_rect.width)

    def _update_volume_from_mouse(self, mouse_x):
        from config import save_settings, update_music_volume
        rel    = mouse_x - self.slider_rect.left
        volume = max(0.0, min(1.0, rel / self.slider_rect.width))
        self.settings["volume"] = volume
        save_settings(self.settings)
        update_music_volume()

    def _draw_sky(self):
        """Gradient sky from SKY_TOP to SKY_BOT."""
        sky_area_h = HEIGHT - self.FLOOR_H
        for y in range(sky_area_h):
            t   = y / max(sky_area_h - 1, 1)
            r   = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
            g   = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
            b   = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    def _draw_floor(self):
        """Scrolling floor strip."""
        fy = HEIGHT - self.FLOOR_H
        if self.floor_img:
            self.screen.blit(self.floor_img, (self.floor_x, fy))
            self.screen.blit(self.floor_img, (self.floor_x + WIDTH, fy))
        else:
            pygame.draw.rect(self.screen, (110, 170, 50), (0, fy, WIDTH, self.FLOOR_H))

    def _draw_settings_panel(self, mouse_pos):
        """Draw the settings overlay."""
        # Dim overlay
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, 160))
        self.screen.blit(dim, (0, 0))

        # Panel box
        panel = pygame.Rect(WIDTH // 2 - 170, 130, 340, 355)
        pygame.draw.rect(self.screen, PANEL_BG,  panel,            border_radius=14)
        pygame.draw.rect(self.screen, PANEL_BDR, panel,            border_radius=14)
        pygame.draw.rect(self.screen, PANEL_TOP,
                         pygame.Rect(panel.x + 2, panel.y + 2, panel.w - 4, 8),
                         border_radius=6)

        # Title
        _draw_outlined_text(self.screen, "SETTINGS",
                            self.font_btn, WHITE, DARK,
                            WIDTH // 2, 165, outline=3)

        # Volume label
        vol     = self.settings.get("volume", 0.5)
        muted   = self.settings.get("muted", False)
        vol_pct = 0 if muted else int(vol * 100)
        lbl_txt = f"MUSIC VOLUME: {vol_pct}%"
        lbl     = self.font_sub.render(lbl_txt, True, (80, 60, 30))
        self.screen.blit(lbl, (WIDTH // 2 - lbl.get_width() // 2, 218))

        # Slider track
        pygame.draw.rect(self.screen, (190, 185, 168), self.slider_rect, border_radius=9)
        knob_x = self._get_knob_x()
        # Progress fill
        if knob_x > self.slider_rect.left:
            fill = pygame.Rect(self.slider_rect.left, self.slider_rect.top,
                               knob_x - self.slider_rect.left, self.slider_rect.height)
            pygame.draw.rect(self.screen, BTN_GREEN, fill, border_radius=9)
        # Knob circle
        kc = (255, 255, 255) if not self.dragging_slider else GOLD
        pygame.draw.circle(self.screen, kc, (knob_x, self.slider_rect.centery), 13)
        pygame.draw.circle(self.screen, (140, 130, 110), (knob_x, self.slider_rect.centery), 13, 2)

        # Mute button
        mute_hovered = self.btn_mute.collidepoint(mouse_pos)
        mute_label   = "♪  MUTED" if muted else "♪  PLAYING"
        mute_color   = BTN_ORANGE if not muted else (160, 160, 160)
        mute_shadow  = BTN_ORG_DK if not muted else (110, 110, 110)
        _draw_panel_button(self.screen, self.btn_mute, self.font_btn,
                           mute_label, WHITE, mute_color, mute_shadow,
                           (80, 60, 30), hovered=mute_hovered)

        # Back button
        back_hovered = self.btn_back.collidepoint(mouse_pos)
        _draw_panel_button(self.screen, self.btn_back, self.font_btn,
                           "◀  BACK", WHITE, BTN_GREEN, BTN_GRN_DK,
                           (50, 100, 30), hovered=back_hovered)

        # ESC hint
        hint = self.font_small.render("ESC  to return", True, (130, 110, 80))
        self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 36))

    # ── Main loop ────────────────────────────────────────────────────────────
    def run(self):
        while True:
            dt        = self.clock.tick(FPS)
            self.tick += dt
            mouse_pos = pygame.mouse.get_pos()

            # ---- Events ----
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.menu_state == "main":
                        if self.btn_play.collidepoint(mouse_pos):
                            return "play"
                        if self.btn_settings.collidepoint(mouse_pos):
                            self.menu_state = "settings"
                    elif self.menu_state == "settings":
                        from config import save_settings, update_music_volume
                        if self.btn_mute.collidepoint(mouse_pos):
                            self.settings["muted"] = not self.settings.get("muted", False)
                            save_settings(self.settings)
                            update_music_volume()
                        elif self.btn_back.collidepoint(mouse_pos):
                            self.menu_state = "main"
                        elif (self.slider_rect.collidepoint(mouse_pos) or
                              math.hypot(mouse_pos[0] - self._get_knob_x(),
                                         mouse_pos[1] - self.slider_rect.centery) < 16):
                            self.dragging_slider = True
                            self._update_volume_from_mouse(mouse_pos[0])

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dragging_slider = False

                if event.type == pygame.MOUSEMOTION:
                    if self.menu_state == "settings" and self.dragging_slider:
                        self._update_volume_from_mouse(mouse_pos[0])

                if event.type == pygame.KEYDOWN:
                    if self.menu_state == "main":
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                            return "play"
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif self.menu_state == "settings":
                        if event.key == pygame.K_ESCAPE:
                            self.menu_state = "main"

            # ── Floor scroll (always) ────────────────────────────────────────
            self.floor_x -= 2
            if self.floor_x <= -WIDTH:
                self.floor_x = 0

            # ──────────────────────────────────────────────────────────────────
            #  DRAW BACKGROUND
            # ──────────────────────────────────────────────────────────────────
            if self.bg:
                self.screen.blit(self.bg, (0, 0))
            else:
                self._draw_sky()

            # ──────────────────────────────────────────────────────────────────
            #  MAIN MENU
            # ──────────────────────────────────────────────────────────────────
            # ── Title ────────────────────────────────────────────────────────
            title_bob = int(math.sin(self.tick * 0.002) * 5)
            _draw_outlined_text(self.screen, "MUSOU DASH",
                                self.font_title, WHITE, DARK,
                                WIDTH // 2, 90 + title_bob, outline=5)

            # ── Bobbing character ────────────────────────────────────────────
            char_bob = int(math.sin(self.tick * 0.003) * 12)
            char_y   = HEIGHT // 2 - 90 + char_bob
            if self.char_surf:
                cx = WIDTH // 2 - self.char_surf.get_width() // 2
                self.screen.blit(self.char_surf, (cx, char_y))
            else:
                # Fallback: simple circle
                pygame.draw.circle(self.screen, GOLD, (WIDTH // 2, char_y + 30), 28)

            # ── Best Score badge ─────────────────────────────────────────────
            if self.best_score > 0:
                badge_txt = f"BEST:  {self.best_score}"
            else:
                badge_txt = "TAP TO START!"
            badge_surf = self.font_sub.render(badge_txt, True, TXT_YEL)
            bw  = badge_surf.get_width() + 32
            bh  = badge_surf.get_height() + 14
            bx  = WIDTH // 2 - bw // 2
            by  = char_y + (self.char_surf.get_height() if self.char_surf else 60) + 12

            pygame.draw.rect(self.screen, DARK, pygame.Rect(bx + 3, by + 3, bw, bh), border_radius=10)
            pygame.draw.rect(self.screen, PANEL_BG, pygame.Rect(bx, by, bw, bh), border_radius=10)
            pygame.draw.rect(self.screen, PANEL_BDR, pygame.Rect(bx, by, bw, bh), 2, border_radius=10)
            self.screen.blit(badge_surf, (bx + 16, by + 7))

            # ── Play button ──────────────────────────────────────────────────
            play_hovered     = self.btn_play.collidepoint(mouse_pos)
            settings_hovered = self.btn_settings.collidepoint(mouse_pos)

            # Play: white panel with green ▶
            _draw_icon_button(self.screen, self.btn_play,
                              None, PANEL_BG, PANEL_BDR,
                              (180, 175, 155), hovered=play_hovered)
            # Draw ▶ triangle manually
            pb = self.btn_play
            shift = 2 if play_hovered else 0
            tri_cx, tri_cy = pb.centerx, pb.centery + shift + (5 if not play_hovered else 7)
            tri_size = 28
            pts = [
                (tri_cx - tri_size // 2, tri_cy - tri_size // 2),
                (tri_cx - tri_size // 2, tri_cy + tri_size // 2),
                (tri_cx + tri_size // 2, tri_cy),
            ]
            pygame.draw.polygon(self.screen, BTN_GREEN, pts)
            pygame.draw.polygon(self.screen, BTN_GRN_DK, pts, 2)
            lbl_play = self.font_small.render("PLAY", True, DARK)
            self.screen.blit(lbl_play, (pb.centerx - lbl_play.get_width() // 2, pb.y + 14))

            # Settings: white panel with ⚙ icon
            _draw_icon_button(self.screen, self.btn_settings,
                              None, PANEL_BG, PANEL_BDR,
                              (180, 175, 155), hovered=settings_hovered)
            sb     = self.btn_settings
            shift2 = 2 if settings_hovered else 0
            gear   = self.font_icon.render("⚙", True, BTN_ORANGE)
            self.screen.blit(gear, (sb.centerx - gear.get_width() // 2,
                                    sb.centery - gear.get_height() // 2 + shift2 + 4))
            lbl_set = self.font_small.render("SETTINGS", True, DARK)
            self.screen.blit(lbl_set, (sb.centerx - lbl_set.get_width() // 2, sb.y + 14))

            # ── Floor ────────────────────────────────────────────────────────
            self._draw_floor()

            # ── Copyright hint ───────────────────────────────────────────────
            hint = self.font_small.render("SPACE / ENTER to play   •   ESC to quit", True, DARK)
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 22))

            # ──────────────────────────────────────────────────────────────────
            #  SETTINGS OVERLAY  (drawn on top of everything)
            # ──────────────────────────────────────────────────────────────────
            if self.menu_state == "settings":
                self._draw_settings_panel(mouse_pos)

            pygame.display.update()
