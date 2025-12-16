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

            self.color = (0, 255, 0)
            self.x = WIDTH // 2 - self.w // 2 + 60
            self.y = HEIGHT // 2 - self.h // 2 + 60
        else:
            self.key_left = pygame.K_a
            self.key_right = pygame.K_d
            self.key_up = pygame.K_w
            self.key_down = pygame.K_s

            self.color = (255, 0, 0)
            self.x = WIDTH // 2 - self.w // 2
            self.y = HEIGHT // 2 - self.h // 2
        
        self.dead = False
        self.death_time = 0
        self.respawn_x = 500
        self.respawn_y = 290

    def move_logic(self, platforms):
        keys = pygame.key.get_pressed()

        #freeze the player while dead
        if self.dead:
            return

        if keys[self.key_left]:
            self.x -= 7
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
                    self.x += 7
                    break
        if keys[self.key_right]:
            self.x += 7
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
                    self.x -= 7
                    break
        if keys[self.key_up]:
            self.y -= 7
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
                    self.y += 7
                    break
        if keys[self.key_down]:
            self.y += 7
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
                    self.y -= 7
                    break

        if not keys[self.key_up]:
            stop = False
            for i in range(1, 4):
                self.y += 7
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
                        self.y -= 7
                        stop = True
                        break
                if stop:
                    break

    def rects_overlap(self, px, py, pw, ph, x, y, w, h):
        # Check if one rectangle is completely to the left, right, above, or below the other
        return not (px + pw <= x or px >= x + w or py + ph <= y or py >= y + h)
    
    def player_respawn(self, screen_height):
        RESPAWN_DELAY = 1000  # 1 second
        RESPAWN_OFFSET_Y= 60
        now = pygame.time.get_ticks()

        # Detect falling off screen
        if self.y >= screen_height and not self.dead:
            self.dead = True
            self.death_time = now

        # Respawn after delay
        if self.dead and now - self.death_time >= RESPAWN_DELAY:
            self.x = self.respawn_x
            self.y = self.respawn_y - RESPAWN_OFFSET_Y
            self.dead = False
       

