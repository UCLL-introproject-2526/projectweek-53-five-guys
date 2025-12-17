import pygame
import random

class SpeedBoost:
    def __init__(self, screen_width):
        self.size = 50
        self.x = random.randint(50, screen_width - 50)
        self.y = -self.size

        self.fall_speed = 4
        self.state = "FALLING"  #used for: FALLING | ON_PLATFORM | USED

        # timers
        self.landed_time = 0
        self.stay_duration = 6000

        # boost settings
        self.boost_amount = 15
        self.duration =8000  # 8 seconds
        self.start_time = None

        # images
        self.image = pygame.image.load("assets/items/speed_boost.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def update(self, platforms):
        if self.state == "FALLING":
            self.y += self.fall_speed

            for p in platforms:
                 if (
                    self.x + self.size > p.x and
                    self.x < p.x + p.w and
                    self.y + self.size >= p.y
            ):
                        # land on platform
                        self.y = p.y - self.size - 8
                        self.state = "ON_PLATFORM"
                        self.landed_time = pygame.time.get_ticks()
                        break
                 
        elif self.state == "ON_PLATFORM":
            now = pygame.time.get_ticks()
            if now - self.landed_time >= self.stay_duration:
                self.state = "USED"  # despawn

    def draw(self, screen):
        if self.state != "USED":
            screen.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        if self.state == "USED":
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
        self.state = "USED"
        self.start_time = pygame.time.get_ticks()
        player.speed += self.boost_amount

    def handle_timer(self, player):
        if self.start_time:
            now = pygame.time.get_ticks()
            if now - self.start_time >= self.duration:
                player.speed = player.base_speed
                self.start_time= None
