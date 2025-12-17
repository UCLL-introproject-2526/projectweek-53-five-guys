import pygame
import sys

VIRTUAL_SIZE = (1920, 1080)
clock = pygame.time.Clock()

def startpage(screen, real):
    screen_w, screen_h = VIRTUAL_SIZE
    CHAR_W, CHAR_H = 400, 409  
    CHAR_SIDE_GAP = 650        
    
    # Names for the UI
    name1, name2 = "Player 1", "Player 2"
    active_box = None
    
    selected_bg_index = 0
    bg_files = ["assets/background.png", "assets/background2.png", "assets/background3.png"]
    
    # Just two character posters for display
    char_options = [
        "assets/character/player_1_poster_choosing.png",
        "assets/character/player_2_poster_choosing.png"
    ]
    p1_char_idx, p2_char_idx = 0, 1

    input_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 24)
    title_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 32)

    # Arrows
    arrow_left = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.polygon(arrow_left, (255, 255, 255), [(0, 20), (40, 0), (40, 40)])
    arrow_right = pygame.transform.flip(arrow_left, True, False)

    char1_center = (screen_w // 2 - CHAR_SIDE_GAP, screen_h // 2 + 100)
    char2_center = (screen_w // 2 + CHAR_SIDE_GAP, screen_h // 2 + 100)
    
    # Rects for clicking
    p1_l_arr = arrow_left.get_rect(center=(char1_center[0] - 250, char1_center[1]))
    p1_r_arr = arrow_right.get_rect(center=(char1_center[0] + 250, char1_center[1]))
    p2_l_arr = arrow_left.get_rect(center=(char2_center[0] - 250, char2_center[1]))
    p2_r_arr = arrow_right.get_rect(center=(char2_center[0] + 250, char2_center[1]))
    box1_rect = pygame.Rect(char1_center[0]-150, char1_center[1]+220, 300, 50)
    box2_rect = pygame.Rect(char2_center[0]-150, char2_center[1]+220, 300, 50)

    bg_thumbnails = []
    bg_rects = []
    for i, path in enumerate(bg_files):
        img = pygame.image.load(path).convert_alpha()
        bg_thumbnails.append(pygame.transform.smoothscale(img, (200, 110)))
        rect = pygame.Rect(0, 0, 200, 110)
        rect.center = (screen_w // 2, 450 + (i * 140))
        bg_rects.append(rect)

    start_img = pygame.transform.scale(pygame.image.load("assets/button/start_game.png").convert_alpha(), (360, 75))
    start_rect = start_img.get_rect(center=(screen_w // 2, 250))

    while True:
        mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), real)
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, r in enumerate(bg_rects):
                    if r.collidepoint(mouse_pos): selected_bg_index = i
                
                # Still let them click arrows for visuals
                if p1_l_arr.collidepoint(mouse_pos): p1_char_idx = (p1_char_idx - 1) % 2
                if p1_r_arr.collidepoint(mouse_pos): p1_char_idx = (p1_char_idx + 1) % 2
                if p2_l_arr.collidepoint(mouse_pos): p2_char_idx = (p2_char_idx - 1) % 2
                if p2_r_arr.collidepoint(mouse_pos): p2_char_idx = (p2_char_idx + 1) % 2

                if box1_rect.collidepoint(mouse_pos): active_box = 1
                elif box2_rect.collidepoint(mouse_pos): active_box = 2
                else: active_box = None

            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_BACKSPACE:
                    if active_box == 1: name1 = name1[:-1]
                    else: name2 = name2[:-1]
                else:
                    if active_box == 1: name1 += event.unicode
                    else: name2 += event.unicode

        # Drawing
        bg_prev = pygame.transform.scale(pygame.image.load(bg_files[selected_bg_index]), VIRTUAL_SIZE)
        bg_prev.set_alpha(150)
        screen.blit(bg_prev, (0, 0))
        
        bg_title = title_font.render("SELECT BACKGROUND", True, (255, 255, 255))
        screen.blit(bg_title, bg_title.get_rect(center=(screen_w // 2, 380)))
        for i, r in enumerate(bg_rects):
            screen.blit(bg_thumbnails[i], r.topleft)
            if i == selected_bg_index: pygame.draw.rect(screen, (0, 255, 255), r, 4)

        c1 = pygame.transform.smoothscale(pygame.image.load(char_options[p1_char_idx]).convert_alpha(), (CHAR_W, CHAR_H))
        c2 = pygame.transform.smoothscale(pygame.image.load(char_options[p2_char_idx]).convert_alpha(), (CHAR_W, CHAR_H))
        screen.blit(c1, c1.get_rect(center=char1_center))
        screen.blit(c2, c2.get_rect(center=char2_center))

        screen.blit(arrow_left, p1_l_arr); screen.blit(arrow_right, p1_r_arr)
        screen.blit(arrow_left, p2_l_arr); screen.blit(arrow_right, p2_r_arr)
        screen.blit(start_img, start_rect)

        # Names
        n1 = input_font.render(name1, True, (0, 255, 255) if active_box == 1 else (255, 255, 255))
        n2 = input_font.render(name2, True, (0, 255, 255) if active_box == 2 else (255, 255, 255))
        screen.blit(n1, n1.get_rect(center=(char1_center[0], char1_center[1] + 250)))
        screen.blit(n2, n2.get_rect(center=(char2_center[0], char2_center[1] + 250)))

        # --- GO BACK TO 3 ITEMS ---
        if start_rect.collidepoint(mouse_pos) and mouse_click:
            return name1, name2, bg_files[selected_bg_index]

        blit_scaled(real, screen)
        pygame.display.flip()

def blit_scaled(screen, virtual):
    win_w, win_h = screen.get_size()
    scale = min(win_w / VIRTUAL_SIZE[0], win_h / VIRTUAL_SIZE[1])
    scaled_w, scaled_h = int(VIRTUAL_SIZE[0] * scale), int(VIRTUAL_SIZE[1] * scale)
    scaled = pygame.transform.smoothscale(virtual, (scaled_w, scaled_h))
    x, y = (win_w - scaled_w) // 2, (win_h - scaled_h) // 2
    screen.fill((0, 0, 0))
    screen.blit(scaled, (x, y))

def screen_to_virtual(mouse_pos, screen):
    win_w, win_h = screen.get_size()
    scale = min(win_w / VIRTUAL_SIZE[0], win_h / VIRTUAL_SIZE[1])
    scaled_w, scaled_h = int(VIRTUAL_SIZE[0] * scale), int(VIRTUAL_SIZE[1] * scale)
    ox, oy = (win_w - scaled_w) // 2, (win_h - scaled_h) // 2
    return int((mouse_pos[0] - ox) / scale), int((mouse_pos[1] - oy) / scale)