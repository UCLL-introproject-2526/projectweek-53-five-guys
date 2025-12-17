import pygame
from .platforms import Platform
from .player import Player
import sys

VIRTUAL_SIZE = (1920, 1080)





def startpage(screen):

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 70)

   
    screen_w, screen_h = screen.get_size()

       
    name1 = ""
    name2 = ""
    active_box = None  

    input_font = pygame.font.Font(
        "assets/Font/Kaijuz.ttf", 32
    )

      
    title_img = pygame.image.load("assets/logo.png").convert_alpha()

    # Resize if needed
    title_img = pygame.transform.scale(title_img, (600, 150))




    

    
    menu_bg = pygame.image.load("assets/background.png").convert_alpha()
    menu_bg = pygame.transform.scale(menu_bg, screen.get_size())
    menu_bg.set_alpha(200) 

    




    
    start_img = pygame.image.load("assets/button/play.png").convert_alpha()
    quit_img  = pygame.image.load("assets/button/quit.png").convert_alpha()

    start_img = pygame.transform.scale(start_img, (500, 100))
    quit_img  = pygame.transform.scale(quit_img, (500, 100))

    start_rect = start_img.get_rect(topleft=(1400, 400))
    quit_rect  = quit_img.get_rect(topleft=(1400, 520))

    base_y = screen_h // 2 + 80   
    gap = 180                     

    start_rect = start_img.get_rect(
    center=(screen_w // 2, base_y))
    quit_rect = quit_img.get_rect(
    center=(screen_w // 2, base_y + gap))


    


   
    char1_img = pygame.image.load("assets/Character/Car1.png").convert_alpha()
    char2_img = pygame.image.load("assets/Character/Car1.png").convert_alpha()

    char1_img = pygame.transform.scale(char1_img, (340, 480))
    char2_img = pygame.transform.scale(char2_img, (340, 480))

    left_center_x = screen_w * 0.25
    char_center_y = screen_h * 0.52
    char_gap = 40

    char1_rect = char1_img.get_rect(
        center=(left_center_x - char1_img.get_width() // 2 - char_gap // 2,
                char_center_y)
    )
    char2_rect = char2_img.get_rect(
        center=(left_center_x + char2_img.get_width() // 2 + char_gap // 2,
                char_center_y)
    )
    
    box_width = 220
    box_height = 40
    box_gap = 20

    box1_rect = pygame.Rect(
        char1_rect.centerx - box_width // 2,
        char1_rect.bottom + box_gap,
        box_width,
        box_height
    )

    box2_rect = pygame.Rect(
        char2_rect.centerx - box_width // 2,
        char2_rect.bottom + box_gap,
        box_width,
        box_height
    )



    screen_w, screen_h = screen.get_size()

    left_center_x = screen_w * 0.25
    char_center_y = screen_h * 0.52
    char_gap = 40


    char1_rect = char1_img.get_rect(
        center=(left_center_x - char1_img.get_width() // 2 - char_gap // 2,
                char_center_y)
    )

    char2_rect = char2_img.get_rect(
        center=(left_center_x + char2_img.get_width() // 2 + char_gap // 2,
                char_center_y)
    )


    
    title_font = pygame.font.Font(
        "assets/Font/Attack_Of_Monster.ttf", 48
    )

    title_text = title_font.render(
        "CHOOSE YOUR CHARACTER", True, (255, 255, 255)
    )

    title_rect = title_text.get_rect(
        center=(screen_w * 0.25, screen_h * 0.25)
    )


    error_message = ""
    error_font = pygame.font.Font("assets/Font/Kaijuz.ttf", 32)


    title_img_rect = title_img.get_rect(
     center=(screen_w // 2, 300)  ) 



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if box1_rect.collidepoint(event.pos):
                    active_box = 1
                elif box2_rect.collidepoint(event.pos):
                    active_box = 2
                else:
                    active_box = None

            if event.type == pygame.KEYDOWN:
                if active_box == 1:
                    if event.key == pygame.K_BACKSPACE:
                        name1 = name1[:-1]
                    else:
                        name1 += event.unicode

                elif active_box == 2:
                    if event.key == pygame.K_BACKSPACE:
                        name2 = name2[:-1]
                    else:
                        name2 += event.unicode


            

        screen.fill((0, 0, 0))
        screen.blit(menu_bg, (0, 0))


        
        pygame.draw.rect(screen, (255, 255, 255), box1_rect, 2)
        pygame.draw.rect(screen, (255, 255, 255), box2_rect, 2)

        
        if active_box == 1:
            pygame.draw.rect(screen, (0, 150, 255), box1_rect, 2)
        if active_box == 2:
            pygame.draw.rect(screen, (0, 150, 255), box2_rect, 2)

        
        name1_surf = input_font.render(name1, True, (255, 255, 255))
        name2_surf = input_font.render(name2, True, (255, 255, 255))

        screen.blit(name1_surf, (box1_rect.x + 8, box1_rect.y + 6))
        screen.blit(name2_surf, (box2_rect.x + 8, box2_rect.y + 6))
       


        

        
        fade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        fade.fill((0, 0, 0, 150)) 
        screen.blit(fade, (0, 0))


        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
         

      
        if start_rect.collidepoint(mouse_pos):
            hover_img = pygame.transform.scale(
                start_img,
                (int(start_rect.width * 1.1), int(start_rect.height * 1.1))
            )
            hover_rect = hover_img.get_rect(center=start_rect.center)
            screen.blit(hover_img, hover_rect)

            if mouse_click:
                if name1 != "" and name2 != "":
                    return name1, name2
                else:
                    error_message = "Input your fucking name to play Dumass"
        else:
            screen.blit(start_img, start_rect)
        
      
        screen.blit(title_img, title_img_rect)


         
        if quit_rect.collidepoint(mouse_pos):
         hover_img = pygame.transform.scale(
         quit_img,
         (int(quit_rect.width * 1.1), int(quit_rect.height * 1.1)))

         hover_rect = hover_img.get_rect(center=quit_rect.center)

         screen.blit(hover_img, hover_rect)
        

         if mouse_click:
          pygame.quit()
          sys.exit()
        else:
          screen.blit(quit_img, quit_rect)



        
        screen.blit(title_text, title_rect)

        screen.blit(char1_img, char1_rect)
        screen.blit(char2_img, char2_rect)






        
        border_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        pygame.draw.rect(
        border_surface,
        (255, 255, 255, 200),  
        border_surface.get_rect(),20)

        screen.blit(border_surface, (0, 0))

        if error_message != "":
          error_surf = error_font.render(error_message, True, (255, 80, 80))
          error_rect = error_surf.get_rect(center=(screen_w // 2, screen_h * 0.85))
        
          screen.blit(error_surf, error_rect)


        pygame.display.flip()
        clock.tick(60)




def main():
   
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    virtual = pygame.Surface(VIRTUAL_SIZE)
    clock = pygame.time.Clock()

    while True:  
        player1_name, player2_name = startpage(screen)

        player1 = Player(1)
        player2 = Player(2)

        background = pygame.image.load("assets/background2.png").convert()
        background = pygame.transform.scale(background, (VIRTUAL_SIZE[0], VIRTUAL_SIZE[1]))



    
        game_quit_img = pygame.image.load("assets/button/quit.png").convert_alpha()
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

            virtual.blit(game_quit_img, game_quit_rect)

            if game_quit_rect.collidepoint(mouse_pos) and mouse_click:
                running = False   # exit game → back to menu



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


def screen_to_virtual(mouse_pos, screen):
    win_w, win_h = screen.get_size()
    scale = min(win_w / VIRTUAL_SIZE[0], win_h / VIRTUAL_SIZE[1])

    scaled_w = int(VIRTUAL_SIZE[0] * scale)
    scaled_h = int(VIRTUAL_SIZE[1] * scale)

    offset_x = (win_w - scaled_w) // 2
    offset_y = (win_h - scaled_h) // 2

    vx = (mouse_pos[0] - offset_x) / scale
    vy = (mouse_pos[1] - offset_y) / scale

    return int(vx), int(vy)



main()
