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

        base_img = weapon_ref.images["right"] if facing == "RIGHT" else weapon_ref.images["left"]
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
            if not (self.x + self.size <= p.x or self.x >= p.x + p.w or self.y + self.size <= p.y or self.y >= p.y + p.h):
                self.state = "USED"
                return

    def draw(self, screen):
        if self.state != "ACTIVE":
            return
        rotated = pygame.transform.rotate(self.base_img, self.rotation)
        rect = rotated.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
        screen.blit(rotated, rect)

    def check_collision(self, player):
        if self.state != "ACTIVE":
            return
        hit = not (
            player.x + player.w <= self.x or
            player.x >= self.x + self.size or
            player.y + player.h <= self.y or
            player.y >= self.y + self.size
        )
        if hit:
            hit_from = "RIGHT" if self.vx > 0 else "LEFT"
            player.hit(hit_from, self.weapon_ref)
            self.state = "USED"