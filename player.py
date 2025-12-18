import pygame
import time
import math
import random
from powerups import Katana, SpeedBoost, Grenade
from throwables import ThrownKatana, ThrownGrenade


PUNCH_WIDTH = 120
PUNCH_HEIGHT = 50


class Player:
    def core_logic(self, platforms, events):
        keys = pygame.key.get_pressed()
        now_ms = pygame.time.get_ticks()

        if self.lives <= 0:
            return

        moving_left = False
        moving_right = False

        if not self.equiped_weapon == None and self.equiped_weapon.durability <= 0:
            self.equiped_weapon = None

        self.speed = self.base_speed
        for p in self.active_powerups:
            picked_up_on = p[1]
            powerup = p[0]
            now = pygame.time.get_ticks()
            ratio = now - picked_up_on
            if isinstance(powerup, SpeedBoost):
                if ratio > powerup.duration:
                    self.active_powerups.remove(p)
                    break
                else:
                    self.speed += 12

        if self.is_dashing and not self.dead:
            dx = self.dash_speed if self.facing == "RIGHT" else -self.dash_speed
            self.x += dx
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
                    self.x -= dx
                    self.end_dash()
                    break
            if now_ms >= self.dash_until:
                self.end_dash()
            moving_left = self.facing == "LEFT"
            moving_right = self.facing == "RIGHT"

        if keys[self.key_left] and not self.dead:
            self.x -= self.speed
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
                    self.x += self.speed
                    break

        if keys[self.key_right] and not self.dead:
            self.x += self.speed
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
                    self.x -= self.speed
                    break

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.key_punch:
                    self.punch()
                if event.key == self.key_dash:
                    self.start_dash(now_ms)
                if event.key == self.key_block:
                    self.block()
                if event.key == self.key_throw:
                    self.throw()

        for p in self.punches:
            now = pygame.time.get_ticks()
            if now - p[2] >= 300:
                self.punches.remove(p)

        if (
            keys[self.key_up]
            and not self.jump_held
            and self.jumps_left > 0
            and not self.dead
        ):
            self.velocity_y = self.jump_strength
            self.jumps_left -= 1
            self.audio_logic("jump")
        self.jump_held = keys[self.key_up]

        if keys[self.key_down] and not self.is_grounded and not self.dead:
            if self.velocity_y < 0:
                self.velocity_y = 0
            self.velocity_y += 3

        current_time = time.time()
        if keys[self.key_down] and not self.down_held and not self.dead:
            if current_time - self.last_down_tap < 0.25:
                self.down_tap_count += 1
            else:
                self.down_tap_count = 1
            self.last_down_tap = current_time

            if (
                self.is_grounded
                and self.drop_platform is not None
                and getattr(self.drop_platform, "fall_through", False)
                and self.down_tap_count >= 2
            ):
                self.drop_through_until = current_time + 0.8
                self.is_grounded = False
                self.velocity_y = max(self.velocity_y, 1)
        if current_time - self.last_down_tap > 0.25:
            self.down_tap_count = 0
        self.down_held = keys[self.key_down]

        self.velocity_y += self.gravity
        self.y += self.velocity_y

        self.is_grounded = False

        if not self.dead:
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

        now = pygame.time.get_ticks()
        ratio = now - self.hit_on
        if self.got_hit and (ratio < 300) and not self.dead:
            if self.hit_from == "RIGHT":
                self.x += int(ratio / 10)
                if ratio < 70:
                    self.velocity_y -= 5
            else:
                self.x -= int(ratio / 10)
                if ratio < 70:
                    self.velocity_y -= 5

        if not self.dead:
            for p in platforms:
                if (
                    current_time < self.drop_through_until
                    and self.drop_platform is not None
                    and getattr(self.drop_platform, "fall_through", False)
                    and p.x == self.drop_platform.x
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
                        self.drop_platform = p
                    elif self.velocity_y < 0:
                        self.y = p.y + p.h
                        self.velocity_y = 0
                    break

        self.update_animation(moving_left, moving_right)

    def hit(self, hit_from, weapon):
        if self.is_blocking:
            return

        self.hit_on = pygame.time.get_ticks()
        self.hit_from = hit_from
        self.got_hit = True
        
        if isinstance(weapon, Katana):
            self.health -= 33.5
        elif isinstance(weapon, Grenade):
            self.health -= 50
        else:
            self.health -= 10

    def punch(self):
        now = pygame.time.get_ticks()
        self.audio_logic("punch")

        if now - self.punched_on < 300:
            return
        if self.is_dashing:
            return

        if isinstance(self.equiped_weapon, Katana):
            if self.equiped_weapon.durability <= 0:
                self.equiped_weapon = None
                self.current_img = (
                    self.attack_left[0]
                    if self.facing == "LEFT"
                    else self.attack_right[0]
                )
            else:
                self.equiped_weapon.durability -= 1
                self.current_img = (
                    self.katana_attack_left[0]
                    if self.facing == "LEFT"
                    else self.katana_attack_right[0]
                )
        else:
            self.current_img = (
                self.attack_left[0] if self.facing == "LEFT" else self.attack_right[0]
            )

        self.is_attacking = True
        self.attack_frame = 0
        self.anim_timer = 0
        self.last_attack_frame_at = now
        self.current_img = (
            self.attack_left[0] if self.facing == "LEFT" else self.attack_right[0]
        )

        if self.facing == "LEFT":
            punch_meta = (
                self.x - PUNCH_WIDTH,
                self.y + int(0.3 * self.h),
                now,
                self.equiped_weapon,
            )
        else:
            punch_meta = (
                self.x + self.w,
                self.y + int(0.3 * self.h),
                now,
                self.equiped_weapon,
            )

        self.punched_on = now
        self.punches.append(punch_meta)

    def block(self):
        now = pygame.time.get_ticks()
        if self.is_dashing or self.dead:
            return

        self.is_blocking = True
        self.block_until = now + self.block_duration
        self.is_attacking = False
        self.current_img = (
            self.block_left if self.facing == "LEFT" else self.block_right
        )

    def throw(self):
        if self.equiped_weapon is None:
            return

        if isinstance(self.equiped_weapon, Katana):
            start_x = self.x + (
                self.w if self.facing == "RIGHT" else -self.equiped_weapon.size
            )
            start_y = self.y + int(0.35 * self.h)
            proj = ThrownKatana(start_x, start_y, self.facing, self.equiped_weapon)
            self.thrown_projectiles.append(proj)
            self.equiped_weapon = None
        
        elif isinstance(self.equiped_weapon, Grenade):
            start_x = self.x + (
                self.w if self.facing == "RIGHT" else -self.equiped_weapon.size
            )
            start_y = self.y + int(0.35 * self.h)
            proj = ThrownGrenade(start_x, start_y, self.facing, self.equiped_weapon)
            self.thrown_projectiles.append(proj)
            
            throw_sound = pygame.mixer.Sound("assets/audio/grenade_throw.mp3")
            throw_sound.set_volume(0.3)
            throw_sound.play()
            
            self.equiped_weapon = None

    def update_animation(self, moving_left, moving_right):
        if self.is_dashing:
            self.current_img = (
                self.dash_left if self.facing == "LEFT" else self.dash_right
            )
            return

        if self.is_blocking:
            now = pygame.time.get_ticks()
            if now < self.block_until:
                self.current_img = (
                    self.block_left if self.facing == "LEFT" else self.block_right
                )
                return
            else:
                self.is_blocking = False

        if self.is_attacking:
            if isinstance(self.equiped_weapon, Katana):
                frames = (
                    self.katana_attack_left
                    if self.facing == "LEFT"
                    else self.katana_attack_right
                )
                now = pygame.time.get_ticks()
                for splash in self.blood_splashes[:]:
                    age = now - splash[2]
                    if age > 800:
                        self.blood_splashes.remove(splash)
                    else:
                        alpha = int(255 * max(0, 1 - (age / 800) ** 0.6))
                        rotation = splash[3]
                        scale = splash[4]

                        blood_scaled = pygame.transform.scale(
                            self.blood_img, (int(80 * scale), int(80 * scale))
                        )
                        blood_rotated = pygame.transform.rotate(blood_scaled, rotation)
                        blood_copy = blood_rotated.copy()
                        blood_copy.set_alpha(alpha)

                        # Center the splash
                        rect = blood_copy.get_rect(center=(splash[0], splash[1]))
                        screen.blit(blood_copy, rect)
            else:
                frames = (
                    self.attack_left if self.facing == "LEFT" else self.attack_right
                )

            now = pygame.time.get_ticks()
            if now - self.last_attack_frame_at >= self.attack_frame_duration_ms:
                self.last_attack_frame_at = now
                self.attack_frame += 1
                if self.attack_frame >= len(frames):
                    self.is_attacking = False
                    self.attack_frame = 0

                    if self.facing == "RIGHT":
                        self.current_img = pygame.transform.flip(
                            self.idle_img, True, False
                        )
                    else:
                        self.current_img = self.idle_img
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
            if self.facing == "RIGHT":
                self.current_img = pygame.transform.flip(self.idle_img, True, False)
            else:
                self.current_img = self.idle_img
            self.frame_index = 0
            self.anim_timer = 0
            return

        self.anim_timer += 1
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(frames)

        self.current_img = frames[self.frame_index]

    def draw(self, screen, opponent_dead: bool = False):
        if self.lives > 0:
            if self.dead:
                if self.facing == "RIGHT":
                    death_img = pygame.transform.flip(self.death_img, True, False)
                    screen.blit(death_img, (self.x, self.y))
                else:
                    screen.blit(self.death_img, (self.x, self.y))
            elif opponent_dead:
                screen.blit(self.victory_img, (self.x, self.y))
            else:
                screen.blit(self.current_img, (self.x, self.y))

                if isinstance(self.equiped_weapon, Katana) and not self.is_attacking:
                    if self.player == 1:
                        right_off = (
                            self.x + int(0.58 * self.w),
                            self.y + int(0.18 * self.h),
                        )
                        left_off = (
                            self.x + int(-0.06 * self.w),
                            self.y + int(0.18 * self.h),
                        )
                    else:
                        right_off = (
                            self.x + int(0.60 * self.w) + 15,
                            self.y + int(0.22 * self.h),
                        )
                        left_off = (
                            self.x + int(-0.10 * self.w) - 15,
                            self.y + int(0.22 * self.h),
                        )

                    katana_img = (
                        self.equiped_weapon.images["right"]
                        if self.facing == "RIGHT"
                        else self.equiped_weapon.images["left"]
                    )
                    offset = right_off if self.facing == "RIGHT" else left_off
                    screen.blit(katana_img, offset)

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

    def draw_powerups(self, screen):
        if self.player == 1:
            powerup_x = 60
            invert = 1
        else:
            powerup_x = screen.get_width() - 50
            invert = -1

        increment = 70
        powerup_y = 190

        for i, p in enumerate(self.active_powerups):
            rel_x_cen = powerup_x + (increment * i) * invert
            rel_y_cen = powerup_y

            ratio = pygame.time.get_ticks() - p[1]

            end_angle = math.radians(self.map_value(ratio, 0, p[0].duration, 0, 360))
            bounding_box = pygame.Rect(rel_x_cen - 30, rel_y_cen - 30, 60, 60)

            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (rel_x_cen, rel_y_cen),
                30,
            )
            screen.blit(
                p[0].image,
                (rel_x_cen - 25, rel_y_cen - 25),
            )

            pygame.draw.arc(screen, (34, 34, 34), bounding_box, 0, end_angle, 7)

        if not self.equiped_weapon == None:
            rel_x_cen = powerup_x + (increment * len(self.active_powerups)) * invert
            rel_y_cen = powerup_y

            end_angle = math.radians(
                self.map_value(
                    self.equiped_weapon.durability,
                    0,
                    self.equiped_weapon.max_durability,
                    0,
                    360,
                )
            )
            bounding_box = pygame.Rect(rel_x_cen - 30, rel_y_cen - 30, 60, 60)

            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (rel_x_cen, rel_y_cen),
                30,
            )

            pygame.draw.arc(screen, (34, 34, 34), bounding_box, 0, end_angle, 7)

            screen.blit(
                self.equiped_weapon.image,
                (rel_x_cen - 25, rel_y_cen - 25),
            )

    def draw_blood(self, screen):
        now = pygame.time.get_ticks()
        for splash in self.blood_splashes[:]:
            age = now - splash[2]
            if age > 800:
                self.blood_splashes.remove(splash)
            else:
                alpha = int(255 * max(0, 1 - (age / 800) ** 0.6))
                rotation = splash[3]

                scale = splash[4]
                blood_scaled = pygame.transform.scale(
                    self.blood_img, (int(80 * scale), int(80 * scale))
                )
                blood_rotated = pygame.transform.rotate(blood_scaled, rotation)
                blood_copy = blood_rotated.copy()
                blood_copy.set_alpha(alpha)

                rect = blood_copy.get_rect(center=(splash[0], splash[1]))
                screen.blit(blood_copy, rect)

    def rects_overlap(self, px, py, pw, ph, x, y, w, h):
        return not (px + pw <= x or px >= x + w or py + ph <= y or py >= y + h)

    def audio_logic(self, audioName):
        try:
            sfx = pygame.mixer.Sound(f"assets/audio/{audioName}.wav")
            sfx.set_volume(1.0)
            sfx.play()
        except pygame.error:
            pass

    def check_death(self, screen_height):
        RESPAWN_DELAY = 2500  # 1 second

        now = pygame.time.get_ticks()

        if (self.y >= screen_height and not self.dead) or (
            self.health <= 0 and not self.dead
        ):
            self.dead = True
            self.death_time = now
            self.lives -= 1
            self.health = 0

            num_splashes = random.randint(3, 5)
            for _ in range(num_splashes):
                splash_x = self.x + random.randint(
                    int(-0.2 * self.w), int(1.2 * self.w)
                )
                splash_y = self.y + random.randint(
                    int(-0.2 * self.h), int(1.2 * self.h)
                )
                rotation = random.randint(0, 360)
                scale = random.uniform(1.0, 2.0)
                self.blood_splashes.append(
                    (splash_x, splash_y, pygame.time.get_ticks(), rotation, scale)
                )

            self.velocity_y -= 20

        if self.dead and now - self.death_time >= RESPAWN_DELAY:
            self.respawn()

    def respawn(self):
        RESPAWN_OFFSET_Y = 60

        self.x = self.respawn_x
        self.y = self.respawn_y - RESPAWN_OFFSET_Y

        self.health = 100
        self.active_powerups = []
        self.equiped_weapon = None
        self.thrown_projectiles = []

        self.dead = False

    def start_dash(self, now_ms):
        if self.is_dashing:
            return
        if now_ms - self.last_dash_at < self.dash_cooldown_ms:
            return
        self.is_dashing = True
        self.dash_until = now_ms + self.dash_duration_ms
        self.last_dash_at = now_ms
        self.invincible_until = self.dash_until
        self.is_attacking = False
        self.attack_frame = 0
        self.anim_timer = 0

    def end_dash(self):
        self.is_dashing = False

    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until

    def map_value(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def __init__(self, player):
        self.player = player
        self.w = 100
        self.h = 100
        self.health = 100
        self.lives = 3
        self.punches = []
        self.punched_on = 0
        self.got_hit = False
        self.hit_on = 0
        self.hit_from = "RIGHT"
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
        self.base_speed = 10
        self.speed = self.base_speed
        self.dead = False
        self.death_time = 0
        self.respawn_y = 290
        self.active_powerups = []
        self.equiped_weapon = None
        self.blood_img = pygame.image.load("assets/blood.png").convert_alpha()
        self.blood_img = pygame.transform.scale(self.blood_img, (80, 80))
        self.blood_splashes = []
        self.facing = "RIGHT"
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 8
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_anim_speed = 5
        self.attack_frame_duration_ms = 90
        self.last_attack_frame_at = 0
        self.is_dashing = False
        self.dash_speed = 28
        self.dash_duration_ms = 220
        self.dash_cooldown_ms = 800
        self.dash_until = 0
        self.last_dash_at = -9999
        self.invincible_until = 0
        self.dash_frame = 0
        self.dash_anim_speed = 4
        self.is_blocking = False
        self.block_duration = 400
        self.block_until = 0
        self.thrown_projectiles = []
        self.dash_hit_done = False

        self.block_left = pygame.transform.scale(
            pygame.image.load(
                f"assets/player_{player}/block/block_left.png"
            ).convert_alpha(),
            (self.w, self.h),
        )

        if player == 1:
            self.key_left = pygame.K_a
            self.key_right = pygame.K_d
            self.key_up = pygame.K_w
            self.key_down = pygame.K_s
            self.key_punch = pygame.K_e
            self.key_dash = pygame.K_r
            self.key_block = pygame.K_q
            self.key_throw = pygame.K_t
            self.x = 550
            self.respawn_x = 550
            self.y = 400
            self.respawn_y = 400
            base = "assets/player_1"
            items = 12
        else:
            self.key_left = pygame.K_LEFT
            self.key_right = pygame.K_RIGHT
            self.key_up = pygame.K_UP
            self.key_down = pygame.K_DOWN
            self.key_punch = pygame.K_m
            self.key_dash = pygame.K_n
            self.key_block = pygame.K_COMMA
            self.key_throw = pygame.K_b
            self.x = 1470
            self.respawn_x = 1470
            self.y = 400
            self.respawn_y = 400
            base = "assets/player_2"
            items = 6

        self.jump_img = pygame.image.load(
            f"{base}/movement_jumping.png"
        ).convert_alpha()
        self.fall_img = pygame.image.load(
            f"{base}/movement_falling.png"
        ).convert_alpha()
        self.heart_img = pygame.transform.scale(
            (pygame.image.load("assets/heart_full.png").convert_alpha()), (60, 60)
        )
        self.death_img = pygame.transform.scale(
            pygame.image.load(f"assets/player_{player}/death.png").convert_alpha(),
            (self.w * 0.70, self.h * 0.83),
        )
        self.victory_img = pygame.transform.scale(
            pygame.image.load(f"assets/player_{player}/victory.png").convert_alpha(),
            (self.w, self.h),
        )
        self.walk_right = [
            pygame.image.load(f"{base}/right/movement_right_{i}.png").convert_alpha()
            for i in range(1, items)
        ]
        self.walk_left = [
            pygame.image.load(f"{base}/left/movement_left_{i}.png").convert_alpha()
            for i in range(1, items)
        ]
        self.walk_right = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.walk_right
        ]
        self.walk_left = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.walk_left
        ]
        self.jump_img = pygame.transform.scale(self.jump_img, (0.75 * self.w, self.h))
        self.fall_img = pygame.transform.scale(self.fall_img, (self.w, self.h))

        self.attack_right = [
            pygame.image.load(f"{base}/attack/attack_right_{i}.png").convert_alpha()
            for i in range(1, 4)
        ]
        self.attack_left = [
            pygame.image.load(f"{base}/attack/attack_left_{i}.png").convert_alpha()
            for i in range(1, 4)
        ]
        self.attack_right = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.attack_right
        ]
        self.attack_left = [
            pygame.transform.scale(img, (self.w, self.h)) for img in self.attack_left
        ]

        self.idle_img = pygame.transform.scale(
            pygame.image.load(f"assets/player_{player}/idle.png").convert_alpha(),
            (self.w, self.h),
        )
        self.current_img = self.idle_img

        self.dash_right = pygame.transform.scale(
            pygame.image.load(
                f"assets/player_{player}/dash/dash_right.png"
            ).convert_alpha(),
            (self.w, self.h),
        )
        self.dash_left = pygame.transform.scale(
            pygame.image.load(
                f"assets/player_{player}/dash/dash_left.png"
            ).convert_alpha(),
            (self.w, self.h),
        )

        self.katana_attack_right = [
            pygame.image.load(
                f"assets/player_{player}/katana/katana_right_{i}.png"
            ).convert_alpha()
            for i in range(1, 4)
        ]
        self.katana_attack_left = [
            pygame.image.load(
                f"assets/player_{player}/katana/katana_left_{i}.png"
            ).convert_alpha()
            for i in range(1, 4)
        ]
        self.katana_attack_right = [
            pygame.transform.scale(img, (self.w, self.h))
            for img in self.katana_attack_right
        ]
        self.katana_attack_left = [
            pygame.transform.scale(img, (self.w, self.h))
            for img in self.katana_attack_left
        ]
        self.block_right = pygame.transform.scale(
            pygame.image.load(
                f"assets/player_{player}/block/block_right.png"
            ).convert_alpha(),
            (self.w, self.h),
        )
        self.block_left = pygame.transform.scale(
            pygame.image.load(
                f"assets/player_{player}/block/block_left.png"
            ).convert_alpha(),
            (self.w, self.h),
        )
