import pygame
import random
from abc import ABC, abstractmethod


class PowerUp(ABC):
    size = 50
    y = -size
    fall_speed = 4
    state = "FALLING"      # FALLING | ON_PLATFORM | USED
    landed_time = 0
    stay_duration = 6000

    @property
    @abstractmethod
    def image(self):
        ...

    def update(self, platforms):
        if self.state == "FALLING":
            self.y += self.fall_speed
            for p in platforms:
                if (
                    self.x + self.size > p.x
                    and self.x < p.x + p.w
                    and self.y + self.size >= p.y
                ):
                    self.y = p.y - self.size - 8
                    self.state = "ON_PLATFORM"
                    self.landed_time = pygame.time.get_ticks()
                    break
        elif self.state == "ON_PLATFORM":
            now = pygame.time.get_ticks()
            if now - self.landed_time >= self.stay_duration:
                self.state = "USED"

    def draw(self, screen):
        if self.state != "USED":
            screen.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        if self.state == "USED":
            return
        hit = not (
            player.x + player.w <= self.x
            or player.x >= self.x + self.size
            or player.y + player.h <= self.y
            or player.y >= self.y + self.size
        )
        if hit:
            self.apply(player)

    @abstractmethod
    def apply(self, player):
        ...


class SpeedBoost(PowerUp):
    def __init__(self):
        self.boost_amount = 15
        self.duration = 8000
        self.start_time = 0
        self.x = random.randint(50, 1920 - 50)

    @property
    def image(self):
        img = pygame.image.load("assets/items/speed_boost.png").convert_alpha()
        return pygame.transform.scale(img, (self.size, self.size))

    def apply(self, player):
        self.state = "USED"
        self.start_time = pygame.time.get_ticks()
        player.active_powerups.append((self, pygame.time.get_ticks()))


class Katana(PowerUp):
    def __init__(self):
        self.x = random.randint(50, 1920 - 50)
        self.images = {
            "left": pygame.transform.scale(
                pygame.image.load("assets/items/katana_left.png").convert_alpha(),
                (self.size, self.size),
            ),
            "right": pygame.transform.scale(
                pygame.image.load("assets/items/katana_right.png").convert_alpha(),
                (self.size, self.size),
            ),
        }

    @property
    def image(self):
        return self.images["right"]

    def apply(self, player):
        self.state = "USED"
        if hasattr(player, "equip_katana"):
            player.equip_katana(self.images)