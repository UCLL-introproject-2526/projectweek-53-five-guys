import pygame
import time

PUNCH_WIDTH = 120
PUNCH_HEIGHT = 50


class Player:
    def __init__(self, player):
        self.player = player
        self.w = 100
        self.h = 100

        self.health = 100
        self.lives = 3

        self.punches = []
        self.punched_on = 0

        self.velocity_y = 0
        self.gravity = 1
        self.jump_strength = -24
        self.is_grounded = False
        self.jumps_left = 2
        self.max_jumps = 2
        self.jump_held = False
        self.last_down_tap = 0
        self.down_tap_count = 0
        self.drop_through_until = 0
        self.down_held = False
        self.drop_platform = None
        self.heart_img = pygame.transform.scale(
            (pygame.image.load("assets/heart_full.png").convert_alpha()), (60, 60)
        )

        if player == 1:
            self.key_left = pygame.K_LEFT
            self.key_right = pygame.K_RIGHT
            self.key_up = pygame.K_UP
            self.key_down = pygame.K_DOWN
            self.key_punch = pygame.K_MINUS
            self.x = 550
            self.respawn_x = 550
            self.y = 400
            self.respawn_y = 400
        else:
            self.key_left = pygame.K_a
            self.key_right = pygame.K_d
            self.key_up = pygame.K_w
            self.key_down = pygame.K_s
            self.key_punch = pygame.K_e
            self.x = 1470
            self.respawn_x = 1470
            self.y = 400
            self.respawn_y = 400

        self.dead = False
        self.death_time = 0
        self.respawn_y = 290

        self.game_over = False   #n


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
        self.jump_img = pygame.transform.scale(self.jump_img, (0.75 * self.w, self.h))
        self.fall_img = pygame.transform.scale(self.fall_img, (self.w, self.h))

        self.attack_right = [
            pygame.image.load(f"assets/attack/attack_right_{i}.png").convert_alpha()
            for i in range(1,5)
        ]
        self.attack_left = [
            pygame.image.load(f"assets/attack/attack_left_{i}.png").convert_alpha()
            for i in range(1,5)
        ]
        self.attack_right = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.attack_right
        ]
        self.attack_left = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.attack_left
        ]

        self.facing = "RIGHT"
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 8

        self.is_attacking = False
        self.attack_frame = 0
        self.attack_anim_speed = 5
        
        self.attack_frame_duration_ms = 90
        self.last_attack_frame_at = 0

        self.current_img = self.walk_right[0]

    def core_logic(self, platforms):
        keys = pygame.key.get_pressed()

        if self.dead or self.lives <= 0:
            return

        moving_left = False
        moving_right = False

        if keys[self.key_left]:
            self.x -= 10
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
                    self.x += 10
                    break
        if keys[self.key_right]:
            self.x += 10
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
                    self.x -= 10
                    break

        if keys[self.key_punch]:
            self.punch()

        
        now = pygame.time.get_ticks()
        for p in self.punches[:]:
            if now - p[2] >= 150:
                self.punches.remove(p)

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
                self.drop_through_until = current_time + 0.8

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

    def punch(self):
        now = pygame.time.get_ticks()

        if now - self.punched_on < 300:
            return

        self.is_attacking = True
        self.attack_frame = 0
        self.anim_timer = 0
        self.last_attack_frame_at = now
        self.current_img = self.attack_left[0] if self.facing == "LEFT" else self.attack_right[0]

        if self.facing == "LEFT":
            punch_meta = (self.x - PUNCH_WIDTH, self.y + int(0.3 * self.h), now)
        else:
            punch_meta = (self.x + self.w, self.y + int(0.3 * self.h), now)

        self.punched_on = now
        self.punches.append(punch_meta)

    def update_animation(self, moving_left, moving_right):
       
        if self.is_attacking:
            frames = self.attack_left if self.facing == "LEFT" else self.attack_right
            now = pygame.time.get_ticks()
            if now - self.last_attack_frame_at >= self.attack_frame_duration_ms:
                self.last_attack_frame_at = now
                self.attack_frame += 1
                if self.attack_frame >= len(frames):
                    self.is_attacking = False
                    self.attack_frame = 0
                    
                    self.current_img = self.walk_left[0] if self.facing == "LEFT" else self.walk_right[0]
                else:
                    self.current_img = frames[self.attack_frame]
            return

        if not self.is_grounded:
            if self.velocity_y < 0:
                if self.facing == "LEFT":
                    self.current_img = pygame.transform.flip(self.jump_img, True, False)
                else:
                    self.current_img = self.jump_img
            else:
                if self.facing == "RIGHT":
                    self.current_img = pygame.transform.flip(self.fall_img, True, False)
                else:
                    self.current_img = self.fall_img
            return

        if moving_left:
            frames = self.walk_left
        elif moving_right:
            frames = self.walk_right
        else:
            self.current_img = self.walk_right[0] if self.facing == "RIGHT" else self.walk_left[0]
            self.frame_index = 0
            self.anim_timer = 0
            return

        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        self.current_img = frames[self.frame_index]

    def draw(self, screen):
        if (self.lives > 0) and not self.dead:
            screen.blit(self.current_img, (self.x, self.y))

    def draw_hearts(self, screen):
        start_y = 20
        heart_spacing = 50
        if self.player == 1:
            start_x = 20
            for i in range(self.lives):
                screen.blit(self.heart_img, (start_x + (i * heart_spacing), start_y))
        else:
            start_x = screen.get_width() - 73
            for i in range(self.lives):
                screen.blit(self.heart_img, (start_x - (i * heart_spacing), start_y))

    def draw_health_bar(self, screen):
        if self.player == 1:
            health_x = 30
        else:
            health_x = screen.get_width() - 330

        health_y = 100
        health = max(0, self.health)

        if self.lives <= 0:
            return

        pygame.draw.rect(
            screen, (34, 34, 34), pygame.Rect(health_x, health_y, 310, 50), 0
        )
        pygame.draw.rect(
            screen,
            (251, 0, 38),
            pygame.Rect(health_x + 5, health_y + 5, 3 * health, 40),
            0,
        )

    def rects_overlap(self, px, py, pw, ph, x, y, w, h):
        return not (px + pw <= x or px >= x + w or py + ph <= y or py >= y + h)

    def check_death(self, screen_height):
        RESPAWN_DELAY = 1000  # 1 second

        now = pygame.time.get_ticks()

        if (self.y >= screen_height and not self.dead) or (
            self.health <= 0 and not self.dead
        ):
            self.dead = True
            self.death_time = now
            self.lives -= 1
            self.health = 0

        if self.lives <= 0: #n
            self.game_over = True

        if self.dead and now - self.death_time >= RESPAWN_DELAY:
            self.respawn()

            


    def respawn(self):
        RESPAWN_OFFSET_Y = 60

        self.x = self.respawn_x
        self.y = self.respawn_y - RESPAWN_OFFSET_Y

        self.health = 100

        self.dead = False

