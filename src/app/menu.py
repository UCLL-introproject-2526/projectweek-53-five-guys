import pygame
import sys

VIRTUAL_SIZE = (1920, 1080)

GAME_PLAYING = "playing"
GAME_END = "end"

game_state = GAME_PLAYING



def startpage(screen):

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 70)


    screen_w, screen_h = screen.get_size()
    right_x = int(screen_w * 0.75)   


       
    name1 = ""
    name2 = ""
    active_box = None  

    input_font = pygame.font.Font(
        "assets/Font/Kaijuz.ttf", 24
    )

      
    title_img = pygame.image.load("assets/logo.png").convert_alpha()
    title_img = pygame.transform.scale(title_img, (700, 380))



    menu_bg = pygame.image.load("assets/background.png").convert_alpha()
    menu_bg = pygame.transform.scale(menu_bg, screen.get_size())
    menu_bg.set_alpha(200) 

    

    
    start_img = pygame.image.load("assets/button/play.png").convert_alpha()
    quit_img  = pygame.image.load("assets/button/quit.png").convert_alpha()

    start_img = pygame.transform.scale(start_img, (360, 75))
    quit_img  = pygame.transform.scale(quit_img,  (360, 75))


    start_rect = start_img.get_rect(topleft=(1400, 400))
    quit_rect  = quit_img.get_rect(topleft=(1400, 520))

    base_y = screen_h // 2 + 40   
    gap = 120                    

    start_rect = start_img.get_rect(center=(right_x, base_y))
    quit_rect  = quit_img.get_rect(center=(right_x, base_y + gap))


   
    char1_img = pygame.image.load("assets/Character/player_1_poster_choosing.png").convert_alpha()
    char2_img = pygame.image.load("assets/Character/player_2_poster_choosing.png").convert_alpha()

    char1_img = pygame.transform.scale(char1_img, (240, 340))
    char2_img = pygame.transform.scale(char2_img, (240, 340))


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
    
    box_width = 180
    box_height = 32
    box_gap = 14

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
        "assets/Font/Attack_Of_Monster.ttf", 36
    )

    title_text = title_font.render(
        "CHOOSE YOUR CHARACTER", True, (255, 255, 255)
    )

    title_rect = title_text.get_rect(
        center=(screen_w * 0.25, screen_h * 0.25)
    )


        
    panel_padding = 25

    panel_left = char1_rect.left - panel_padding
    panel_top = title_rect.top - panel_padding
    panel_right = char2_rect.right + panel_padding
    panel_bottom = box1_rect.bottom + panel_padding

    panel_rect = pygame.Rect(
        panel_left,
        panel_top,
        panel_right - panel_left,
        panel_bottom - panel_top
    )





    error_message = ""
    error_font = pygame.font.Font("assets/Font/Kaijuz.ttf", 24)


    title_img_rect = title_img.get_rect(
     center=(right_x, 200)  ) 



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

        fade = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        fade.fill((0, 0, 0, 150)) 
        screen.blit(fade, (0, 0))





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
                    error_message = "Input your Name to play"
        else:
            screen.blit(start_img, start_rect)
        
      
             
        # panel_surface = pygame.Surface(panel_rect.size, pygame.SRCALPHA)
        # panel_surface.fill((20, 20, 20, 180)) 
        # screen.blit(panel_surface, panel_rect.topleft)

        
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



       
        panel_surface = pygame.Surface(panel_rect.size, pygame.SRCALPHA)

        pygame.draw.rect(
            panel_surface,
            (15, 15, 15, 220), 
            panel_surface.get_rect(),
            border_radius=60  
        )




        
        border_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        pygame.draw.rect(
        border_surface,
        (255, 255, 255, 200),  
        border_surface.get_rect(),20)

        pygame.draw.rect(
        screen,
        (255, 255, 255, 120),
        panel_rect,
        2,
        border_radius=30
)


        screen.blit(border_surface, (0, 0))

        if error_message != "":
          error_surf = error_font.render(error_message, True, (255, 80, 80))
          error_rect = error_surf.get_rect(center=(screen_w // 2, screen_h * 0.85))
        
          screen.blit(error_surf, error_rect)

        
        screen.blit(panel_surface, panel_rect.topleft)



        
        screen.blit(title_text, title_rect)

        screen.blit(char1_img, char1_rect)
        screen.blit(char2_img, char2_rect)


        pygame.display.flip()
        clock.tick(60)

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
