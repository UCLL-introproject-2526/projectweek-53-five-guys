import pygame
import random
import asyncio
from platforms import Platform
from player import Player
from menu import startpage
from menu import screen_to_virtual
from powerups import SpeedBoost, Heart, Katana


VIRTUAL_SIZE = (1920, 1080)


async def main():
    # pygame.mixer.init()
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    virtual = pygame.Surface(VIRTUAL_SIZE)
    clock = pygame.time.Clock()

    player1_name, player2_name = startpage(virtual, screen)

    player1 = Player(1)
    player2 = Player(2)

    background = pygame.image.load("assets/background.png").convert()
    background = pygame.transform.scale(background, (VIRTUAL_SIZE[0], VIRTUAL_SIZE[1]))

    game_quit_img = pygame.image.load("assets/button/quit2.png").convert_alpha()
    game_quit_img = pygame.transform.scale(game_quit_img, (220, 70))
    game_quit_rect = game_quit_img.get_rect(bottomleft=(30, VIRTUAL_SIZE[1] - 30))

    name_font = pygame.font.Font("assets/font/Kaijuz.ttf", 36)
    p1_name_surf = name_font.render(player1_name, True, (255, 255, 255))
    p2_name_surf = name_font.render(player2_name, True, (255, 255, 255))

    speed_boost = None
    BOOST_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BOOST_EVENT, 13000)  # spawn every 13 seconds

    heart = None
    HEART_EVENT = pygame.USEREVENT + 2
    pygame.time.set_timer(HEART_EVENT, 20000)

    katana = None
    KATANA_EVENT = pygame.USEREVENT + 3
    pygame.time.set_timer(KATANA_EVENT, 20000)

    platforms = [
        Platform(280, 420, 470, 73, True),
        Platform(1190, 420, 559, 73, True),
        Platform(422, 758, 1084, 79, False),
        Platform(524, 837, 223, 102, False),
        Platform(1120, 837, 223, 102, False),
        Platform(762, 869, 331, 135, False),
    ]

    running = True
    while running:
        clock.tick(60)
        virtual.blit((background), (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == BOOST_EVENT and speed_boost is None:
                speed_boost = SpeedBoost()
            if event.type == HEART_EVENT and heart is None:
                if random.random() <= 0.3:
                    heart = Heart()
            if event.type == KATANA_EVENT and katana is None:
                katana = Katana()

        virtual.blit((background), (0, 0))

        # for p in platforms:
        # p.draw(virtual)

        player1.core_logic(platforms, events)
        player2.core_logic(platforms, events)
        PUNCH_WIDTH = 70
        PUNCH_HEIGHT = 20
        for p in player1.punches:
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
                player2.hit(player1.facing, p[3])
                player1.punches.remove(p)

        for p in player2.punches:
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
                player1.hit(player2.facing, p[3])
                player2.punches.remove(p)

        player1.check_death(VIRTUAL_SIZE[1])
        player2.check_death(VIRTUAL_SIZE[1])

        player1.x = max(0, min(VIRTUAL_SIZE[0] - player1.w, player1.x))
        player2.x = max(0, min(VIRTUAL_SIZE[0] - player2.w, player2.x))

        player1.draw(virtual, opponent_dead=(player2.dead or player2.lives <= 0))
        player2.draw(virtual, opponent_dead=(player1.dead or player1.lives <= 0))
        player1.draw_hearts(virtual)
        player1.draw_health_bar(virtual)
        player1.draw_powerups(virtual)
        player2.draw_hearts(virtual)
        player2.draw_health_bar(virtual)
        player2.draw_powerups(virtual)

        if katana:
            katana.update(platforms)
            katana.draw(virtual)

            katana.check_collision(player1)
            katana.check_collision(player2)

            if katana.state == "USED":
                katana = None

        if heart:
            heart.update(platforms)  # falls down / lands on platforms
            heart.draw(virtual)  # draw the heart

            heart.check_collision(player1)
            heart.check_collision(player2)

            # Remove heart if collected or expired
            if heart.state == "USED":
                heart = None

        if speed_boost:
            speed_boost.update(platforms)
            speed_boost.draw(virtual)

            speed_boost.check_collision(player1)
            speed_boost.check_collision(player2)

            # Fell off screen without being collected
            if speed_boost.state == "USED":
                speed_boost = None

        virtual.blit(p1_name_surf, (40, 104))
        virtual.blit(p2_name_surf, (VIRTUAL_SIZE[0] - 320, 104))

        mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), screen)
        mouse_click = pygame.mouse.get_pressed()[0]

        virtual.blit(game_quit_img, game_quit_rect)

        if game_quit_rect.collidepoint(mouse_pos) and mouse_click:
            running = False

        blit_scaled(screen, virtual)
        pygame.display.flip()


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


asyncio.run(main())
