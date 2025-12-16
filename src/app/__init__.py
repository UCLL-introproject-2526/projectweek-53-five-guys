import pygame
from .platforms import Platform
from .player import Player

VIRTUAL_SIZE = (1920, 1080)


def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    virtual = pygame.Surface(VIRTUAL_SIZE)

    clock = pygame.time.Clock()

    player1 = Player(1)
    player2 = Player(2)

    pygame.time.Clock().tick(60)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        virtual.fill((0, 0, 0))

        platforms = [
            Platform(180, 490, 800, 10),
            Platform(180, 410, 170, 10),
            Platform(400, 410, 350, 10),
            Platform(180, 410, 10, 80),
            Platform(80, 210, 50, 10),
            Platform(400, 210, 50, 10),
            Platform(80, 600, 50, 10),
        ]

        for p in platforms:
            p.draw(virtual)

        player1.move_logic(platforms)
        player2.move_logic(platforms)

        player1.x = max(0, min(VIRTUAL_SIZE[0] - player1.w, player1.x))
        player1.y = max(0, min(VIRTUAL_SIZE[1] - player1.h, player1.y))

        player2.x = max(0, min(VIRTUAL_SIZE[0] - player2.w, player2.x))
        player2.y = max(0, min(VIRTUAL_SIZE[1] - player2.h, player2.y))

        pygame.draw.rect(
            virtual,
            player1.color,
            (player1.x, player1.y, player1.w, player1.h),
        )
        pygame.draw.rect(
            virtual,
            player2.color,
            (player2.x, player2.y, player2.w, player2.h),
        )

        blit_scaled(screen, virtual)
        pygame.display.flip()
        clock.tick(60)


def blit_scaled(screen, virtual):
    win_w, win_h = screen.get_size()
    scale = min(win_w / VIRTUAL_SIZE[0], win_h / VIRTUAL_SIZE[1])

    scaled_w = int(VIRTUAL_SIZE[0] * scale)
    scaled_h = int(VIRTUAL_SIZE[1] * scale)

    scaled = pygame.transform.smoothscale(virtual, (scaled_w, scaled_h))

    x = (win_w - scaled_w) // 2
    y = (win_h - scaled_h) // 2

    screen.fill((0, 0, 0))
    screen.blit(scaled, (x, y))
