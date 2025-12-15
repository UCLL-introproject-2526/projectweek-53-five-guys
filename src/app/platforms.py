import pygame


class Platform:
    def __init__(self, xloc, yloc, width, height):
        self.x = xloc
        self.y = yloc
        self.h = height
        self.w = width

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (128, 94, 2),
            (self.x, self.y, self.w, self.h),
        )
