import pygame
from .platforms import Platform
from .player import Player
from .powerups import SpeedBoost

VIRTUAL_SIZE = (1920, 1080)


def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    virtual = pygame.Surface(VIRTUAL_SIZE)

    clock = pygame.time.Clock()

    player1 = Player(1)
    player2 = Player(2)

    speed_boost = None
    BOOST_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BOOST_EVENT, 13000)  # spawn every 13 seconds

    punches_p1 = []
    punches_p2 = []

    background = pygame.image.load("assets/background.png").convert()
    background = pygame.transform.scale(background, (VIRTUAL_SIZE[0], VIRTUAL_SIZE[1]))

    platforms = [
        Platform(280, 420, 470, 73),
        Platform(1190, 420, 559, 73),
        Platform(422, 758, 1084, 79),
        Platform(524, 837, 223, 102),
        Platform(1120, 837, 223, 102),
        Platform(762, 869, 331, 135),
    ]

    running = True
    while running:
        clock.tick(120)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == BOOST_EVENT and speed_boost is None:
                speed_boost = SpeedBoost(VIRTUAL_SIZE[0])


        virtual.blit((background), (0, 0))

        #for p in platforms:
            #p.draw(virtual)

        player1.core_logic(platforms)
        player2.core_logic(platforms)
        PUNCH_WIDTH = 70
        PUNCH_HEIGHT = 20
        for p in player1.punches:
            pygame.draw.rect(
                virtual,
                (0, 255, 0),
                (p[0], p[1], PUNCH_WIDTH, PUNCH_HEIGHT),
            )
            if player1.rects_overlap(
                player2.x,
                player2.y,
                player2.w,
                player2.h,
                p[0],
                p[1],
                PUNCH_WIDTH,
                PUNCH_HEIGHT,
            ):
                player2.health -= 25
                player1.punches.remove(p)

        for p in player2.punches:
            pygame.draw.rect(
                virtual,
                (255, 0, 0),
                (p[0], p[1], PUNCH_WIDTH, PUNCH_HEIGHT),
            )
            if player2.rects_overlap(
                player1.x,
                player1.y,
                player1.w,
                player1.h,
                p[0],
                p[1],
                PUNCH_WIDTH,
                PUNCH_HEIGHT,
            ):
                player1.health -= 25
                player2.punches.remove(p)

        player1.check_death(VIRTUAL_SIZE[1])
        player2.check_death(VIRTUAL_SIZE[1])

        player1.x = max(0, min(VIRTUAL_SIZE[0] - player1.w, player1.x))
        player2.x = max(0, min(VIRTUAL_SIZE[0] - player2.w, player2.x))

        player1.draw(virtual)
        player2.draw(virtual)
        player1.draw_hearts(virtual)
        player1.draw_health_bar(virtual)
        player2.draw_hearts(virtual)
        player2.draw_health_bar(virtual)

        # ---------- SPEED BOOST LOGIC ----------
        if speed_boost:
            speed_boost.update(platforms)  # move down to platforms
            speed_boost.draw(virtual)  # draw yellow square

            speed_boost.check_collision(player1)
            speed_boost.check_collision(player2)

            speed_boost.handle_timer(player1)
            speed_boost.handle_timer(player2)

        # Fell off screen without being collected
        if speed_boost and speed_boost.state == "USED":
            speed_boost = None



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


main()
