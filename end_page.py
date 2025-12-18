import pygame
import math

VIRTUAL_SIZE = (1920, 1080)


def draw_shadow_text(surface, text, font, color, center, shadow=(0, 0, 0), offset=3):
    shadow_surf = font.render(text, True, shadow)
    surface.blit(
        shadow_surf,
        shadow_surf.get_rect(center=(center[0] + offset, center[1] + offset)),
    )

    text_surf = font.render(text, True, color)
    surface.blit(text_surf, text_surf.get_rect(center=center))


def draw_moving_text(surface, text, font, color, center, speed=0.002, strength=0.06):
    t = pygame.time.get_ticks()
    scale = 1.0 + math.sin(t * speed) * strength

    text_surf = font.render(text, True, color)
    w, h = text_surf.get_size()
    scaled = pygame.transform.smoothscale(text_surf, (int(w * scale), int(h * scale)))

    surface.blit(scaled, scaled.get_rect(center=center))


class EndPage:
    def __init__(self):
        self.title_font = pygame.font.Font("assets/font/upheavtt.ttf", 110)
        self.text_font = pygame.font.Font("assets/font/upheavtt.ttf", 40)
        self.hint_font = pygame.font.Font("assets/font/upheavtt.ttf", 28)

        self.button_font = pygame.font.Font("assets/font/upheavtt.ttf", 48)

        self.restart_text = self.button_font.render("RESTART", True, (255, 255, 255))
        self.quit_text = self.button_font.render("QUIT", True, (255, 255, 255))

        self.restart_rect = pygame.Rect(0, 0, 300, 64)
        self.quit_rect = pygame.Rect(0, 0, 300, 64)

    def update_layout(self):
        cx = VIRTUAL_SIZE[0] // 2
        cy = VIRTUAL_SIZE[1] // 2

        self.title_y = cy - 220
        self.winner_y = cy - 60
        self.hint_y = cy + 10

        self.restart_rect.center = (cx, cy + 120)
        self.quit_rect.center = (cx, cy + 200)

    def handle_input(self, mouse_pos, click):
        if click and self.restart_rect.collidepoint(mouse_pos):
            return "restart"
        if click and self.quit_rect.collidepoint(mouse_pos):
            return "quit"
        return None

    def draw(self, surface, winner_name, mouse_pos, click):
        self.update_layout()

        overlay = pygame.Surface(VIRTUAL_SIZE, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        surface.blit(overlay, (0, 0))

        cx = VIRTUAL_SIZE[0] // 2

        draw_moving_text(
            surface,
            "GAME OVER",
            self.title_font,
            (220, 40, 40),
            (cx, self.title_y),
        )

        draw_shadow_text(
            surface,
            f"{winner_name} - has won the battle!",
            self.text_font,
            (235, 235, 235),
            (cx, self.winner_y),
        )

        draw_shadow_text(
            surface,
            "Click Restart to play again!",
            self.hint_font,
            (150, 150, 150),
            (cx, self.hint_y),
        )

        self.draw_button(
            surface, self.restart_rect, self.restart_text, mouse_pos, click
        )
        self.draw_button(surface, self.quit_rect, self.quit_text, mouse_pos, click)

    def draw_button(self, surface, rect, text, mouse_pos, click):
        hovered = rect.collidepoint(mouse_pos)

        fill = (50, 50, 60) if hovered else (30, 30, 35)
        border = (220, 40, 40) if hovered else (100, 100, 100)

        pygame.draw.rect(surface, fill, rect, border_radius=14)
        pygame.draw.rect(surface, border, rect, 3, border_radius=14)

        surface.blit(text, text.get_rect(center=rect.center))
