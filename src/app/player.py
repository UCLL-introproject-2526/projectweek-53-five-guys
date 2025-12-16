import pygame
import time


class Player:
    def __init__(self, player):
        self.player = player
        self.w = 50
        self.h = 50
        WIDTH = 1024
        HEIGHT = 768

        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -12
        self.is_grounded = False
        self.jumps_left = 2
        self.max_jumps = 2
        self.jump_held = False
        self.last_down_tap = 0
        self.down_tap_count = 0
        self.drop_through_until = 0
        self.down_held = False
        self.drop_platform = None

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

        self.dead = False
        self.death_time = 0
        self.respawn_x = 500
        self.respawn_y = 290

    def move_logic(self, platforms):
        keys = pygame.key.get_pressed()

        # freeze the player while dead
        if self.dead:
            return

        if keys[self.key_left]:
            self.x -= 5
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
                    self.x += 5
                    break
        if keys[self.key_right]:
            self.x += 5
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
                    self.x -= 5
                    break

        if keys[self.key_up] and not self.jump_held and self.jumps_left > 0:
            self.velocity_y = self.jump_strength
            self.jumps_left -= 1
        self.jump_held = keys[self.key_up]

        current_time = time.time()
        if keys[self.key_down] and not self.down_held:
            if current_time - self.last_down_tap < 0.25:
                self.down_tap_count += 1
            else:
                self.down_tap_count = 1
            self.last_down_tap = current_time

            if self.is_grounded == True and self.down_tap_count >= 2:
                self.drop_through_until = current_time + 0.3

                self.is_grounded = False
                self.velocity_y = max(self.velocity_y, 1)
        if current_time - self.last_down_tap > 0.25:
            self.down_tap_count = 0
        self.down_held = keys[self.key_down]

        self.velocity_y += self.gravity
        self.y += self.velocity_y

        self.is_grounded = False
        for p in platforms:
            if (
                current_time < self.drop_through_until
                and self.drop_platform is not None
            ):
                if (
                    p.x == self.drop_platform.x
                    and p.y == self.drop_platform.y
                    and p.w == self.drop_platform.w
                    and p.h == self.drop_platform.h
                ):
                    continue
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
                if self.velocity_y > 0:
                    self.y = p.y - self.h
                    self.velocity_y = 0
                    self.is_grounded = True
                    self.jumps_left = self.max_jumps
                    self.drop_platform = p  # Store platform when landing
                elif self.velocity_y < 0:
                    self.y = p.y + p.h
                    self.velocity_y = 0
                break

    def rects_overlap(self, px, py, pw, ph, x, y, w, h):
        # Check if one rectangle is completely to the left, right, above, or below the other
        return not (px + pw <= x or px >= x + w or py + ph <= y or py >= y + h)

    def player_respawn(self, screen_height):
        RESPAWN_DELAY = 1000  # 1 second
        RESPAWN_OFFSET_Y = 60
        now = pygame.time.get_ticks()

        # Detect falling off screen
        if self.y >= screen_height and not self.dead:
            self.dead = True
            self.death_time = now

        # Respawn after delay
        if self.dead and now - self.death_time >= RESPAWN_DELAY:
            self.x = self.respawn_x
            self.y = self.respawn_y - RESPAWN_OFFSET_Y
            self.dead = False
