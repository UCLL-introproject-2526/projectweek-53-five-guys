import pygame
import random
import asyncio
from platforms import Platform
from player import Player
from menu import startpage
from menu import screen_to_virtual
from powerups import SpeedBoost, Heart, Katana
from end_page import EndPage
import sys


VIRTUAL_SIZE = (1920, 1080)


async def main():
    # pygame.mixer.init()
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    virtual = pygame.Surface(VIRTUAL_SIZE)
    clock = pygame.time.Clock()

    while True:
        player1_name, player2_name, background_img = startpage(virtual, screen)

        player1 = Player(1)
        player2 = Player(2)

        background = pygame.image.load(background_img).convert()
        background = pygame.transform.scale(
            background, (VIRTUAL_SIZE[0], VIRTUAL_SIZE[1])
        )

        game_quit_img = pygame.image.load("assets/button/quit_game.png").convert_alpha()
        game_quit_img = pygame.transform.scale(game_quit_img, (220, 70))
        game_quit_rect = game_quit_img.get_rect(bottomleft=(30, VIRTUAL_SIZE[1] - 30))


        # control page 
        controls_btn_img = pygame.image.load("assets/button/control.png").convert_alpha()
        controls_btn_img = pygame.transform.scale(controls_btn_img, (250, 70))
        controls_btn_rect = controls_btn_img.get_rect(
            bottomleft=(30, VIRTUAL_SIZE[1] - 30 - 80)  
        )

       
        popup_img = pygame.image.load("assets/controlPage.png").convert_alpha()
        popup_img = pygame.transform.smoothscale(popup_img, (1400, 800))
        popup_img = round_corners(popup_img, radius=50) 
        popup_rect = popup_img.get_rect(center=(VIRTUAL_SIZE[0] // 2, VIRTUAL_SIZE[1] // 2))


        close_img = None
        try:
            close_img = pygame.image.load("assets/button/control_exit.png").convert_alpha()
            close_img = pygame.transform.smoothscale(close_img, (55, 55))
        except:
            close_img = None  

        close_rect = pygame.Rect(0, 0, 55, 55)
        close_rect.topright = (popup_rect.right - 15, popup_rect.top + 15)

        show_popup = False

        #ends the contols


        name_font = pygame.font.Font("assets/font/Kaijuz.ttf", 36)
        p1_name_surf = name_font.render(player1_name, True, (255, 255, 255))
        p2_name_surf = name_font.render(player2_name, True, (255, 255, 255))

        speed_boost = None
        heart = None
        katana = None
        powerups = [
            (None, 0.8),
            ("SPEED_BOOST", 0.1),
            ("HEART", 0.07),
            ("KATANA", 0.03),
        ]
        ITEM_SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(ITEM_SPAWN_EVENT, 1000)

        platforms = [
            Platform(280, 420, 470, 73, True),
            Platform(1190, 420, 559, 73, True),
            Platform(422, 758, 1084, 79, False),
            Platform(524, 837, 223, 102, False),
            Platform(1120, 837, 223, 102, False),
            Platform(762, 869, 331, 135, False),
        ]

        end_page = EndPage()

        running = True
        while running:
            clock.tick(60)
            virtual.blit((background), (0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == ITEM_SPAWN_EVENT and speed_boost is None:
                    check = {
                        None: True,
                        "SPEED_BOOST": speed_boost == None,
                        "HEART": heart == None,
                        "KATANA": katana == None,
                    }
                    powerups = [p for p in powerups if check[p[0]]]

                    cum = 0.0
                    for p in powerups:
                        cum += p[1]
                    if cum < 1.0:
                        powerups.append((None, 1.0 - cum))

                    r = random.random()
                    cum = 0.0
                    result = None

                    for outcome, p in powerups:
                        cum += p
                        if r < cum:
                            result = outcome
                            break

                    match result:
                        case None:
                            pass
                        case "SPEED_BOOST":
                            speed_boost = SpeedBoost()
                        case "HEART":
                            heart = Heart()
                        case "KATANA":
                            katana = Katana()

            mouse_click = any(
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                for event in events
            )
            mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), screen)

            virtual.blit((background), (0, 0))

            # for p in platforms:
            # p.draw(virtual)


            #draw button for control
            virtual.blit(controls_btn_img, controls_btn_rect)
            virtual.blit(game_quit_img, game_quit_rect)

            
            if controls_btn_rect.collidepoint(mouse_pos) and mouse_click:
                show_popup = True

           
            if show_popup:
               
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        show_popup = False

                should_close = draw_image_popup(
                    virtual, popup_img, popup_rect, close_img, close_rect, mouse_pos, mouse_click
                )
                if should_close:
                    show_popup = False

                blit_scaled(screen, virtual)
                pygame.display.flip()
                continue  

            #ends here 
        






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

            if player1.lives <= 0 or player2.lives <= 0:
                if player1.lives <= 0:
                    winner_name = player2_name
                    loser_name = player1_name
                else:
                    winner_name = player1_name
                    loser_name = player2_name

                action = end_page.handle_input(mouse_pos, mouse_click)
                end_page.draw(virtual, winner_name, mouse_pos, mouse_click)

                blit_scaled(screen, virtual)
                pygame.display.flip()

                if action == "restart":
                    break

                if action == "quit":
                    pygame.quit()
                    sys.exit()

                continue

            player1.x = max(0, min(VIRTUAL_SIZE[0] - player1.w, player1.x))
            player2.x = max(0, min(VIRTUAL_SIZE[0] - player2.w, player2.x))

            player1.draw(virtual, opponent_dead=(player2.dead or player2.lives <= 0))
            player2.draw(virtual, opponent_dead=(player1.dead or player1.lives <= 0))
            player1.draw_hearts(virtual)
            player1.draw_health_bar(virtual)
            player1.draw_powerups(virtual)
            player1.draw_blood(virtual)
            player2.draw_hearts(virtual)
            player2.draw_health_bar(virtual)
            player2.draw_powerups(virtual)
            player2.draw_blood(virtual)

            if katana:
                katana.update(platforms)
                katana.draw(virtual)

                katana.check_collision(player1)
                katana.check_collision(player2)

                if katana.state == "USED":
                    katana = None

            if heart:
                heart.update(platforms)
                heart.draw(virtual)

                heart.check_collision(player1)
                heart.check_collision(player2)

                if heart.state == "USED":
                    heart = None

            if speed_boost:
                speed_boost.update(platforms)
                speed_boost.draw(virtual)

                speed_boost.check_collision(player1)
                speed_boost.check_collision(player2)

                if speed_boost.state == "USED":
                    speed_boost = None

            virtual.blit(p1_name_surf, (40, 104))
            virtual.blit(p2_name_surf, (VIRTUAL_SIZE[0] - 320, 104))

            virtual.blit(game_quit_img, game_quit_rect)

            if game_quit_rect.collidepoint(mouse_pos) and mouse_click:
                running = False

            blit_scaled(screen, virtual)
            pygame.display.flip()



def draw_image_popup(virtual, popup_img, popup_rect, close_img, close_rect, mouse_pos, mouse_click):
    
    overlay = pygame.Surface(virtual.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    virtual.blit(overlay, (0, 0))

    
    virtual.blit(popup_img, popup_rect)

    
    if close_img is not None:
        virtual.blit(close_img, close_rect)
    else:
        pygame.draw.rect(virtual, (30, 30, 30), close_rect, border_radius=8)
        pygame.draw.rect(virtual, (255, 255, 255), close_rect, width=2, border_radius=8)
        font = pygame.font.Font(None, 48)
        x_surf = font.render("X", True, (255, 255, 255))
        x_rect = x_surf.get_rect(center=close_rect.center)
        virtual.blit(x_surf, x_rect)

   
    return mouse_click and close_rect.collidepoint(mouse_pos)

def round_corners(surf: pygame.Surface, radius: int) -> pygame.Surface:
    w, h = surf.get_size()
    radius = max(0, min(radius, min(w, h)//2))

   
    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)

   
    rounded = surf.copy()
    rounded.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return rounded






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


