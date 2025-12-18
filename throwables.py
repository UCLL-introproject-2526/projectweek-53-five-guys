import pygame


class ThrownKatana:
    def __init__(self, start_x, start_y, facing, weapon_ref):
        self.size = 50
        self.x = start_x
        self.y = start_y
        self.vx = 22 if facing == "RIGHT" else -22
        self.vy = -6
        self.gravity = 0.9
        self.rotation = 0
        self.rot_speed = 18
        self.state = "ACTIVE"  # ACTIVE | USED
        self.weapon_ref = weapon_ref

        base_img = (
            weapon_ref.images["right"]
            if facing == "RIGHT"
            else weapon_ref.images["left"]
        )
        self.base_img = base_img

    def update(self, platforms):
        if self.state != "ACTIVE":
            return

        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.rotation = (self.rotation + self.rot_speed) % 360

        if self.y > 1080 or self.x < -self.size or self.x > 1920 + self.size:
            self.state = "USED"
            return

        for p in platforms:
            if not (
                self.x + self.size <= p.x
                or self.x >= p.x + p.w
                or self.y + self.size <= p.y
                or self.y >= p.y + p.h
            ):
                self.state = "USED"
                return

    def draw(self, screen):
        if self.state != "ACTIVE":
            return
        rotated = pygame.transform.rotate(self.base_img, self.rotation)
        rect = rotated.get_rect(
            center=(self.x + self.size // 2, self.y + self.size // 2)
        )
        screen.blit(rotated, rect)

    def check_collision(self, player):
        if self.state != "ACTIVE":
            return
        hit = not (
            player.x + player.w <= self.x
            or player.x >= self.x + self.size
            or player.y + player.h <= self.y
            or player.y >= self.y + self.size
        )
        if hit:
            hit_from = "RIGHT" if self.vx > 0 else "LEFT"
            player.hit(hit_from, self.weapon_ref)
            self.state = "USED"


class ThrownGrenade:
    def __init__(self, start_x, start_y, facing, weapon_ref):
        self.size = 40
        self.x = start_x
        self.y = start_y
        self.vx = 18 if facing == "RIGHT" else -18
        self.vy = 0
        self.rotation = 0
        self.rot_speed = 25
        self.state = "ACTIVE"
        self.weapon_ref = weapon_ref
        self.explosion_frame = 0
        self.explosion_start_time = None
        self.frame_duration = 100
        self.hit_players = set()
        self.explosion_sound_played = False

    def update(self, platforms):
        if self.state == "USED":
            return

        if self.state == "ACTIVE":
            self.x += self.vx
            self.rotation = (self.rotation + self.rot_speed) % 360

            if self.y > 1080 or self.x < -self.size or self.x > 1920 + self.size:
                self.state = "USED"
                return

            for p in platforms:
                if not (
                    self.x + self.size <= p.x
                    or self.x >= p.x + p.w
                    or self.y + self.size <= p.y
                    or self.y >= p.y + p.h
                ):
                    self.start_explosion()
                    return

        elif self.state == "EXPLODING":
            now = pygame.time.get_ticks()
            elapsed = now - self.explosion_start_time

            self.explosion_frame = min(
                elapsed // self.frame_duration,
                len(self.weapon_ref.images["explosion"]) - 1,
            )

            if elapsed > self.frame_duration * len(self.weapon_ref.images["explosion"]):
                self.state = "USED"

    def start_explosion(self):
        self.state = "EXPLODING"
        self.explosion_start_time = pygame.time.get_ticks()
        self.vx = 0
        self.hit_players = set()

        if not self.explosion_sound_played:
            try:
                explosion_sound = pygame.mixer.Sound("assets/audio/explosion.mp3")
                explosion_sound.set_volume(0.3)
                explosion_sound.play()
                self.explosion_sound_played = True
            except:
                pass

    def draw(self, screen):
        if self.state == "ACTIVE":
            rotated = pygame.transform.rotate(
                self.weapon_ref.images["grenade"], self.rotation
            )
            rect = rotated.get_rect(
                center=(self.x + self.size // 2, self.y + self.size // 2)
            )
            screen.blit(rotated, rect)

        elif self.state == "EXPLODING":
            explosion_img = self.weapon_ref.images["explosion"][self.explosion_frame]
            rect = explosion_img.get_rect(
                center=(self.x + self.size // 2, self.y + self.size // 2)
            )
            screen.blit(explosion_img, rect)

    def check_collision(self, player):
        if self.state == "ACTIVE":
            hit = not (
                player.x + player.w <= self.x
                or player.x >= self.x + self.size
                or player.y + player.h <= self.y
                or player.y >= self.y + self.size
            )
            if hit:
                self.start_explosion()
                return

        if self.state == "EXPLODING" and player.player not in self.hit_players:
            now = pygame.time.get_ticks()
            elapsed = now - self.explosion_start_time

            if elapsed < 50:
                return

            explosion_radius = 80
            hit = not (
                player.x + player.w <= self.x - explosion_radius
                or player.x >= self.x + self.size + explosion_radius
                or player.y + player.h <= self.y - explosion_radius
                or player.y >= self.y + self.size + explosion_radius
            )
            if hit:
                hit_from = "RIGHT" if player.x > self.x else "LEFT"
                player.hit(hit_from, self.weapon_ref)
                self.hit_players.add(player.player)

