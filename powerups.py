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

            if self.y >= 1080:
                self.state = "USED"

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


class Katana(PowerUp):
    def __init__(self):
        self.x = random.randint(50, 1920 - 50)
        self.durability = 3
        self.max_durability = 3
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
        player.equiped_weapon = self


class Grenade:
    def __init__(self):
        self.size = 40
        self.x = random.randint(200, 1720)
        self.y = -self.size
        self.vy = 0
        self.fall_speed = 4  
        self.state = "FALLING"  
        self.max_durability = 1  
        self.durability = 1
        self.landed_time = 0
        self.stay_duration = 6000

        
        try:
            self.grenade_img = pygame.transform.scale(
                pygame.image.load("assets/items/grenade/grenade.png").convert_alpha(),
                (self.size, self.size),
            )
            self.explosion_imgs = [
                pygame.transform.scale(
                    pygame.image.load(f"assets/items/grenade/bomb_{i}.png").convert_alpha(),
                    (100, 100),
                )
                for i in range(1, 4)  
            ]
            self.images = {
                "grenade": self.grenade_img,
                "explosion": self.explosion_imgs,
            }
        except pygame.error as e:
            print(f"Error loading grenade images: {e}")
            raise

    @property
    def image(self):
        return self.grenade_img

    def update(self, platforms):
        if self.state == "FALLING":
            self.y += self.fall_speed

            if self.y >= 1080:
                self.state = "USED"
                return

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
            screen.blit(self.grenade_img, (self.x, self.y))

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
            player.equiped_weapon = self
            self.state = "USED"
