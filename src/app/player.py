import pygame


class Player:
    def __init__(self, player):
        self.player = player
        self.w = 50
        self.h = 50
        WIDTH = 1024
        HEIGHT = 768

        if player == 1:
            self.key_left = pygame.K_LEFT
            self.key_right = pygame.K_RIGHT
            self.key_up = pygame.K_UP
            self.key_down = pygame.K_DOWN

            self.color = (0, 255, 0)
            self.x = WIDTH // 2 - self.w // 2 + 60
            self.y = HEIGHT // 2 - self.h // 2 + 60
        else:
            self.key_left = pygame.K_a
            self.key_right = pygame.K_d
            self.key_up = pygame.K_w
            self.key_down = pygame.K_s

            self.color = (255, 0, 0)
            self.x = WIDTH // 2 - self.w // 2
            self.y = HEIGHT // 2 - self.h // 2

    def move_logic(self, platforms):
        keys = pygame.key.get_pressed()

        if keys[self.key_left]:
            self.x -= 1
            for p in platforms:
                if self.rects_overlap(
                    self.x,
                    self.y,
                    self.w,
                    self.h,
                    p.x,
                    p.y,
                    p.w,
                    p.h,
                ):
                    self.x += 1
                    break
        if keys[self.key_right]:
            self.x += 1
            for p in platforms:
                if self.rects_overlap(
                    self.x,
                    self.y,
                    self.w,
                    self.h,
                    p.x,
                    p.y,
                    p.w,
                    p.h,
                ):
                    self.x -= 1
                    break
        if keys[self.key_up]:
            self.y -= 1
            for p in platforms:
                if self.rects_overlap(
                    self.x,
                    self.y,
                    self.w,
                    self.h,
                    p.x,
                    p.y,
                    p.w,
                    p.h,
                ):
                    self.y += 1
                    break
        if keys[self.key_down]:
            self.y += 1
            for p in platforms:
                if self.rects_overlap(
                    self.x,
                    self.y,
                    self.w,
                    self.h,
                    p.x,
                    p.y,
                    p.w,
                    p.h,
                ):
                    self.y -= 1
                    break

        if not keys[self.key_up]:
            stop = False
            for i in range(1, 4):
                self.y += 1
                for p in platforms:
                    if self.rects_overlap(
                        self.x,
                        self.y,
                        self.w,
                        self.h,
                        p.x,
                        p.y,
                        p.w,
                        p.h,
                    ):
                        self.y -= 1
                        stop = True
                        break
                if stop:
                    break

    def rects_overlap(self, px, py, pw, ph, x, y, w, h):
        # Check if one rectangle is completely to the left, right, above, or below the other
        return not (px + pw <= x or px >= x + w or py + ph <= y or py >= y + h)
