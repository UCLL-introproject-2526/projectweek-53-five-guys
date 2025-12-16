import pygame
import time


class Player:
    def __init__(self, player):
        self.player = player
        self.w = 80
        self.h = 80
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
            self.x = WIDTH // 2 - self.w // 2 + 60
            self.y = HEIGHT // 2 - self.h // 2 + 60
        else:
            self.key_left = pygame.K_a
            self.key_right = pygame.K_d
            self.key_up = pygame.K_w
            self.key_down = pygame.K_s
            self.x = WIDTH // 2 - self.w // 2
            self.y = HEIGHT // 2 - self.h // 2

        self.dead = False
        self.death_time = 0
        self.respawn_x = 500
        self.respawn_y = 290

        self.walk_right = [
            pygame.image.load(f"assets/right/movement_right_{i}.png").convert_alpha()
            for i in range(1, 13)
        ]

        self.walk_left = [
            pygame.image.load(f"assets/left/movement_left_{i}.png").convert_alpha()
            for i in range(1, 13)
        ]


        self.jump_img = pygame.image.load("assets/movement_jumping.png").convert_alpha()
        self.fall_img = pygame.image.load("assets/movement_falling.png").convert_alpha()

        self.walk_right = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.walk_right
        ]
        self.walk_left = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.walk_left
        ]
        self.jump_img = pygame.transform.scale(self.jump_img, (self.w, self.h))
        self.fall_img = pygame.transform.scale(self.fall_img, (self.w, self.h))

        self.facing = "RIGHT"
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 8

        self.current_img = self.walk_right[0]

    def move_logic(self, platforms):
        keys = pygame.key.get_pressed()

        if self.dead:
            return

        moving_left = False
        moving_right = False

        if keys[self.key_left]:
            self.x -= 5
            moving_left = True
            self.facing = "LEFT"
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
            moving_right = True
            self.facing = "RIGHT"
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

            if self.is_grounded and self.down_tap_count >= 2:
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

        self.update_animation(moving_left, moving_right)

    def update_animation(self, moving_left, moving_right):
        if not self.is_grounded:
            if self.velocity_y < 0:
                self.current_img = self.jump_img
            else:
                self.current_img = self.fall_img
            return

        if moving_left:
            frames = self.walk_left
        elif moving_right:
            frames = self.walk_right
        else:
            self.current_img = (
                self.walk_right[0] if self.facing == "RIGHT" else self.walk_left[0]
            )
            self.frame_index = 0
            self.anim_timer = 0
            return

        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        self.current_img = frames[self.frame_index]

    def draw(self, screen):
        screen.blit(self.current_img, (self.x, self.y))

    def rects_overlap(self, px, py, pw, ph, x, y, w, h):
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
