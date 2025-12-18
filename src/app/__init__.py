import pygame
import random
from .platforms import Platform
from .player import Player
from .menu import startpage
from .menu import screen_to_virtual
<<<<<<< HEAD
from .powerups import SpeedBoost, Heart

||||||| 8b6e555
from .powerups import SpeedBoost, Heart


=======
from .powerups import SpeedBoost, Heart, Shield
import random

>>>>>>> origin/shield-item
VIRTUAL_SIZE = (1920, 1080)

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    virtual = pygame.Surface(VIRTUAL_SIZE)
    clock = pygame.time.Clock()

    pygame.mixer.music.load("assets/audio/background_menu_song.wav") 
    pygame.mixer.music.play(-1)

    player1_name, player2_name, chosen_bg = startpage(virtual, screen)

    pygame.mixer.music.stop()

    player1 = Player(1)
    player2 = Player(2)

    background = pygame.image.load(chosen_bg).convert()
    background = pygame.transform.scale(background, (VIRTUAL_SIZE[0], VIRTUAL_SIZE[1]))

    game_quit_img = pygame.image.load("assets/button/quit_game.png").convert_alpha()
    game_quit_img = pygame.transform.scale(game_quit_img, (220, 70))
    game_quit_rect = game_quit_img.get_rect(bottomleft=(30, VIRTUAL_SIZE[1] - 30))

    name_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 36)
    p1_name_surf = name_font.render(player1_name, True, (255, 255, 255))
    p2_name_surf = name_font.render(player2_name, True, (255, 255, 255))
<<<<<<< HEAD
    
||||||| 8b6e555
=======


>>>>>>> origin/shield-item
    speed_boost = None
    BOOST_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BOOST_EVENT, 13000)

    heart = None
    HEART_EVENT = pygame.USEREVENT + 2
<<<<<<< HEAD
    pygame.time.set_timer(HEART_EVENT, 20000)
||||||| 8b6e555
    pygame.time.set_timer(
        HEART_EVENT, 20000
    )  # spawn every 20 seconds (adjust as you like)
=======
    pygame.time.set_timer(HEART_EVENT, 20000)  # spawn every 20 seconds 

    shield = None
    SHIELD_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BOOST_EVENT, 12000) 

>>>>>>> origin/shield-item

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
            if event.type == SHIELD_EVENT and shield is None:
                if random.random() < 0.35:  # 35% chance
                    shield = Shield()

            

        player1.core_logic(platforms, events)
        player2.core_logic(platforms, events)
        PUNCH_WIDTH, PUNCH_HEIGHT = 70, 20
        
        # P1 hits P2
        for p in player1.punches[:]:
            if player1.rects_overlap(player2.x, player2.y, player2.w, player2.h, p[0], p[1], PUNCH_WIDTH, PUNCH_HEIGHT):
                player2.hit(player1.facing)
                player1.punches.remove(p)

        # P2 hits P1
        for p in player2.punches[:]:
            if player2.rects_overlap(player1.x, player1.y, player1.w, player1.h, p[0], p[1], PUNCH_WIDTH, PUNCH_HEIGHT):
                player1.hit(player2.facing)
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

        if speed_boost:
            speed_boost.update(platforms)
            speed_boost.draw(virtual)
            speed_boost.check_collision(player1)
            speed_boost.check_collision(player2)
            if speed_boost.state == "USED": speed_boost = None

        if heart:
            heart.update(platforms)
            heart.draw(virtual)
            heart.check_collision(player1)
            heart.check_collision(player2)
            if heart.state == "USED": heart = None

        virtual.blit(p1_name_surf, (40, 104))
        virtual.blit(p2_name_surf, (VIRTUAL_SIZE[0] - 320, 104))

        mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), screen)
        mouse_click = pygame.mouse.get_pressed()[0]
        virtual.blit(game_quit_img, game_quit_rect)

        if game_quit_rect.collidepoint(mouse_pos) and mouse_click:
            running = False

<<<<<<< HEAD
||||||| 8b6e555
        if heart:
            heart.update(platforms)  # falls down / lands on platforms
            heart.draw(virtual)  # draw the heart

            heart.check_collision(player1)
            heart.check_collision(player2)

            # Remove heart if collected or expired
            if heart.state == "USED":
                heart = None

=======
        if heart:
            heart.update(platforms)  # falls down / lands on platforms
            heart.draw(virtual)  # draw the heart

            heart.check_collision(player1)
            heart.check_collision(player2)

            # Remove heart if collected or expired
            if heart.state == "USED":
                heart = None

        
        if shield:
            shield.update(platforms)  # falls down / lands on platforms
            shield.draw(virtual)  # draw the heart

            shield.check_collision(player1)
            shield.check_collision(player2)

            # Remove heart if collected or expired
            if shield.state == "USED":
                shield = None
   

>>>>>>> origin/shield-item
        blit_scaled(screen, virtual)
        pygame.display.flip()

def blit_scaled(screen, virtual):
    win_w, win_h = screen.get_size()
    scale = min(win_w / VIRTUAL_SIZE[0], win_h / VIRTUAL_SIZE[1])
    scaled_w, scaled_h = int(VIRTUAL_SIZE[0] * scale), int(VIRTUAL_SIZE[1] * scale)
    scaled = pygame.transform.smoothscale(virtual, (scaled_w, scaled_h))
    x, y = (win_w - scaled_w) // 2, (win_h - scaled_h) // 2
    screen.fill((0, 0, 0))
    screen.blit(scaled, (x, y))

main()