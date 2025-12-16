import pygame
from .platforms import Platform
from .player import Player


def main():
    pygame.init()

    WIDTH = 1024
    HEIGHT = 768
    screen_size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(screen_size)

    player1 = Player(1)
    player2 = Player(2)

    clock = pygame.time.Clock()

    jump = 0

    running = True
    while running:
        
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

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
            p.draw(screen)

        player1.move_logic(platforms)
        player2.move_logic(platforms)

        player1.x = max(0, min(WIDTH - player1.w, player1.x))
        player1.y = max(0, min(HEIGHT - player1.h, player1.y))

        player2.x = max(0, min(WIDTH - player2.w, player2.x))
        player2.y = max(0, min(HEIGHT - player2.h, player2.y))

        pygame.draw.rect(
            screen,
            player1.color,
            (player1.x, player1.y, player1.w, player1.h),
        )
        pygame.draw.rect(
            screen,
            player2.color,
            (player2.x, player2.y, player2.w, player2.h),
        )
        pygame.display.flip()

main()