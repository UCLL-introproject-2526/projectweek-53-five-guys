import pygame
import random

class SpeedBoost:
    def __init__(self, screen_width):
        self.size = 30
        self.x = random.randint(50, screen_width - 50)
        self.y = -self.size

        self.fall_speed = 4
        self.active = True

        # boost settings
        self.boost_amount = 3
        self.duration = 6000  # 6 seconds
        self.start_time = None
        self.used = False

    def update(self):
        if self.active:
            self.y += self.fall_speed

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(
                screen,
                (255, 255, 0),
                (self.x, self.y, self.size, self.size)
            )

    def check_collision(self, player):
        if not self.active:
            return

        hit = not (
            player.x + player.w <= self.x or
            player.x >= self.x + self.size or
            player.y + player.h <= self.y or
            player.y >= self.y + self.size
        )

        if hit:
            self.apply(player)

    def apply(self, player):
        self.active = False
        self.used = True
        self.start_time = pygame.time.get_ticks()
        player.speed += self.boost_amount

    def handle_timer(self, player):
        if self.used and self.start_time:
            now = pygame.time.get_ticks()
            if now - self.start_time >= self.duration:
                player.speed = player.base_speed
                self.used = False
