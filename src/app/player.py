import pygame


class Player:
    def __init__(self, player):
        self.player = player
        self.w = 50
        self.h = 50
        WIDTH = 1024
        HEIGHT = 768

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

        self.speed = 2

        self.vy = 0
        self.jump_strength = 8
        self.gravity = 0.5
        self.on_ground = False

        self.walk_right = [
            pygame.image.load("assets/movement_right_1.png").convert_alpha(),
            pygame.image.load("assets/movement_right_2.png").convert_alpha(),
            pygame.image.load("assets/movement_right_3.png").convert_alpha(),
        ]
        self.walk_left = [
            pygame.image.load("assets/movement_left_1.png").convert_alpha(),
            pygame.image.load("assets/movement_left_2.png").convert_alpha(),
            pygame.image.load("assets/movement_left_3.png").convert_alpha(),
        ]

        self.jump_img = pygame.image.load("assets/movement_jumping.png").convert_alpha()
        self.fall_img = pygame.image.load("assets/movement_falling.png").convert_alpha()

        self.walk_right = [pygame.transform.scale(img, (self.w, self.h)) for img in self.walk_right]
        self.walk_left = [pygame.transform.scale(img, (self.w, self.h)) for img in self.walk_left]
        self.jump_img = pygame.transform.scale(self.jump_img, (self.w, self.h))
        self.fall_img = pygame.transform.scale(self.fall_img, (self.w, self.h))

    
        self.facing = "RIGHT"
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 8

        self.current_img = self.walk_right[0]

    def move_logic(self, platforms):
        keys = pygame.key.get_pressed()

        moving_left = False
        moving_right = False

        if keys[self.key_left]:
            self.x -= self.speed
            moving_left = True
            self.facing = "LEFT"
            for p in platforms:
                if self.rects_overlap(self.x, self.y, self.w, self.h, p.x, p.y, p.w, p.h):
                    self.x += self.speed
                    break

        if keys[self.key_right]:
            self.x += self.speed
            moving_right = True
            self.facing = "RIGHT"
            for p in platforms:
                if self.rects_overlap(self.x, self.y, self.w, self.h, p.x, p.y, p.w, p.h):
                    self.x -= self.speed
                    break

        if keys[self.key_up] and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False

        self.vy += self.gravity
        self.y += self.vy

        self.on_ground = False
        for p in platforms:
            if self.rects_overlap(self.x, self.y, self.w, self.h, p.x, p.y, p.w, p.h):
                if self.vy > 0:
                    self.y = p.y - self.h
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = p.y + p.h
                    self.vy = 0

        
        self.update_animation(moving_left, moving_right)

    def update_animation(self, moving_left, moving_right):
        if not self.on_ground:
            if self.vy < 0:
                self.current_img = self.jump_img
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
        screen.blit(self.current_img, (self.x, self.y))

    def rects_overlap(self, px, py, pw, ph, x, y, w, h):
        return not (px + pw <= x or px >= x + w or py + ph <= y or py >= y + h)
