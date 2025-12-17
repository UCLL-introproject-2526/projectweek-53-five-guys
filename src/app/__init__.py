import pygame
from .platforms import Platform
from .player import Player
import sys
from .menu import startpage
from .menu import screen_to_virtual
import math

VIRTUAL_SIZE = (1920, 1080)

import math

def draw_pulsing_glow_text(surface, text, font, base_color, center, time_ms):
    pulse = 1.0 + 0.05 * math.sin(time_ms / 200)
    glow_color = (255, 80, 80)

    # glow layers
    for offset in [6, 4, 2]:
        glow = font.render(text, True, glow_color)
        glow = pygame.transform.scale(
            glow,
            (int(glow.get_width() * pulse), int(glow.get_height() * pulse))
        )
        rect = glow.get_rect(center=center)
        surface.blit(glow, rect)

    # main text
    main = font.render(text, True, base_color)
    main = pygame.transform.scale(
        main,
        (int(main.get_width() * pulse), int(main.get_height() * pulse))
    )
    rect = main.get_rect(center=center)
    surface.blit(main, rect)


def main():
   
    pygame.init()
    font = pygame.font.Font("assets/Font/upheavtt.ttf", 64)

    title_font = pygame.font.Font("assets/Font/upheavtt.ttf", 110)
    name_font_big = pygame.font.Font("assets/Font/upheavtt.ttf", 64)
    info_font = pygame.font.Font("assets/Font/upheavtt.ttf", 40)



    overlay_color = (0, 0, 0, 200)   #nnnnnn

    button_font = pygame.font.Font("assets/Font/upheavtt.ttf", 48)

    restart_text = button_font.render("RESTART", True, (255, 255, 255))
    quit_text = button_font.render("QUIT", True, (255, 255, 255))

    restart_rect = pygame.Rect(
    VIRTUAL_SIZE[0] // 2 - 150, VIRTUAL_SIZE[1] // 2 + 260, 300, 6 )
    quit_rect = pygame.Rect(
    VIRTUAL_SIZE[0] // 2 - 150, VIRTUAL_SIZE[1] // 2 + 340, 300, 60 )   #nnnn




    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    virtual = pygame.Surface(VIRTUAL_SIZE)
    clock = pygame.time.Clock()

    while True:  

        player1_name, player2_name = startpage(screen)


        player1 = Player(1)
        player2 = Player(2)

        background = pygame.image.load("assets/background.png").convert()
        background = pygame.transform.scale(background, (VIRTUAL_SIZE[0], VIRTUAL_SIZE[1]))




    
        game_quit_img = pygame.image.load("assets/button/quit2.png").convert_alpha()
        game_quit_img = pygame.transform.scale(game_quit_img, (220, 70))
        game_quit_rect = game_quit_img.get_rect(bottomleft=(30, VIRTUAL_SIZE[1] - 30))






        name_font = pygame.font.Font("assets/Font/Kaijuz.ttf", 36)
        p1_name_surf = name_font.render(player1_name, True, (255, 255, 255))
        p2_name_surf = name_font.render(player2_name, True, (255, 255, 255))

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

            virtual.blit((background), (0, 0))

            
            virtual.blit(p1_name_surf, (40, 160))
            virtual.blit(p2_name_surf, (VIRTUAL_SIZE[0] - 240, 160))

            # for p in platforms:
            #  p.draw(virtual)

            player1.core_logic(platforms)
            player2.core_logic(platforms)
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
                    player2.health -= 25
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


            
            mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), screen)
            mouse_click = pygame.mouse.get_pressed()[0]



            if player1.game_over or player2.game_over:  #nnnn
                if restart_rect.collidepoint(mouse_pos) and mouse_click:
                    running = False  

                if quit_rect.collidepoint(mouse_pos) and mouse_click:
                    pygame.quit()
                    sys.exit()  #nnnn


            virtual.blit(game_quit_img, game_quit_rect)


            if game_quit_rect.collidepoint(mouse_pos) and mouse_click:
                running = False

                
            if player1.game_over or player2.game_over:   #nnnnnn

                overlay = pygame.Surface(VIRTUAL_SIZE, pygame.SRCALPHA)
                overlay.fill(overlay_color)
                virtual.blit(overlay, (0, 0))

                center_x = VIRTUAL_SIZE[0] // 2
                base_y = VIRTUAL_SIZE[1] // 2 - 160

               
                if player1.game_over:
                    loser_name = player1_name
                    winner_name = player2_name
                else:
                    loser_name = player2_name
                    winner_name = player1_name

                
                button_y = base_y + 300
                restart_rect.y = button_y
                quit_rect.y = button_y + 80

                
                now = pygame.time.get_ticks()

                draw_pulsing_glow_text(
                    virtual,
                    f"{winner_name} HAS WON!",
                    title_font,
                    (220, 40, 40),   # deep red
                    (center_x, base_y),
                    now
                )


                
                draw_text_with_shadow(
                    virtual,
                    f"{loser_name}'s journey ends here. Better luck Next time!",
                    info_font,
                    (220, 220, 220),
                    (center_x, base_y + 80),
                    shadow_color=(0, 0, 0),
                    offset=3
                )

                
                draw_text_with_shadow(
                    virtual,
                    "Press RESTART to play again",
                    info_font,
                    (180, 180, 180),
                    (center_x, base_y + 130),
                    shadow_color=(0, 0, 0),
                    offset=2
                )

                
                pygame.draw.rect(virtual, (80, 80, 80), restart_rect, border_radius=14)
                pygame.draw.rect(virtual, (80, 80, 80), quit_rect, border_radius=14)

                virtual.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
                virtual.blit(quit_text, quit_text.get_rect(center=quit_rect.center))




            blit_scaled(screen, virtual)
            pygame.display.flip()
            clock.tick(60)


def draw_text_with_shadow(surface, text, font, color, center, shadow_color=(0,0,0), offset=3):
    shadow = font.render(text, True, shadow_color)
    shadow_rect = shadow.get_rect(center=(center[0] + offset, center[1] + offset))
    surface.blit(shadow, shadow_rect)

    txt = font.render(text, True, color)
    txt_rect = txt.get_rect(center=center)
    surface.blit(txt, txt_rect)
        


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
