import pygame


class Platform:
    def __init__(self, xloc, yloc, width, height, fall_through):
        self.x = xloc
        self.y = yloc
        self.h = height
        self.w = width
        self.fall_through = fall_through

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (128, 94, 2),
            (self.x, self.y, self.w, self.h),
        )
