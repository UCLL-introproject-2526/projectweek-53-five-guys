import pygame
from .platforms import Platform
from .player import Player


def main():
    pygame.init()

    WIDTH, HEIGHT = 1024, 768
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    clock = pygame.time.Clock()  

    player1 = Player(1)
    player2 = Player(2)

    
        

   
    platforms = [
        Platform(180, 550, 600, 10),
       
        Platform(60, 300, int(WIDTH * 0.3), 10),
        Platform(WIDTH - int(WIDTH * 0.3) - 40, 300, int(WIDTH * 0.3), 10)


    ]

    running = True
    while running:
        clock.tick(60)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for p in platforms:
            p.draw(screen)

        player1.move_logic(platforms)
        player2.move_logic(platforms)

        player1.x = max(0, min(WIDTH - player1.w, player1.x))
        player1.y = max(0, min(HEIGHT - player1.h, player1.y))

        player2.x = max(0, min(WIDTH - player2.w, player2.x))
        player2.y = max(0, min(HEIGHT - player2.h, player2.y))

        pygame.draw.rect(screen, player1.color,
                         (player1.x, player1.y, player1.w, player1.h))
        pygame.draw.rect(screen, player2.color,
                         (player2.x, player2.y, player2.w, player2.h))

        pygame.display.flip()

    pygame.quit()


main()
