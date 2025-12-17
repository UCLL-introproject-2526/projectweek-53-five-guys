import pygame
import random
from abc import ABC, abstractmethod


class PowerUp(ABC):
    size = 50
    y = -size

    fall_speed = 4
    state = "FALLING"  # used for: FALLING | ON_PLATFORM | USED

    # timers
    landed_time = 0
    stay_duration = 6000

    @property
    @abstractmethod
    def image(self):
        pass

    def update(self, platforms):
        if self.state == "FALLING":
            self.y += self.fall_speed

            for p in platforms:
                if (
                    self.x + self.size > p.x
                    and self.x < p.x + p.w
                    and self.y + self.size >= p.y
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
            player.x + player.w <= self.x
            or player.x >= self.x + self.size
            or player.y + player.h <= self.y
            or player.y >= self.y + self.size
        )

        if hit:
            self.apply(player)

    @abstractmethod
    def apply(self, player):
        pass


class SpeedBoost(PowerUp):
    def __init__(self):
        self.boost_amount = 15
        self.duration = 8000  # 8 seconds
        self.start_time = 0
        self.x = random.randint(50, 1920 - 50)

    @property
    def image(self):
        image = pygame.image.load("assets/items/speed_boost.png").convert_alpha()
        return pygame.transform.scale(image, (self.size, self.size))

    def apply(self, player):
        self.audio_logic("itemReceive")
        self.state = "USED"
        self.start_time = pygame.time.get_ticks()
        player.active_powerups.append((self, pygame.time.get_ticks()))
        player.speed += self.boost_amount

    def audio_logic(self, audioName):
        try:
            sfx = pygame.mixer.Sound(f"assets/audio/{audioName}.wav")
            sfx.set_volume(1.0)
            sfx.play()
        except pygame.error:
            pass


class Heart(PowerUp):
    def __init__(self):
        self.x = random.randint(50, 1920 - 50)
        self.heal_amount = 1

    @property
    def image(self):
        img = pygame.image.load("assets/heart_full.png").convert_alpha()
        return pygame.transform.scale(img, (self.size, self.size))

    def apply(self, player):
        self.state = "USED"
        player.lives += self.heal_amount
