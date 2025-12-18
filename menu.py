import pygame
import sys

VIRTUAL_SIZE = (1920, 1080)
clock = pygame.time.Clock()


def startpage(screen, real):
    screen_w, screen_h = VIRTUAL_SIZE

    name1, name2 = "Player 1", "Player 2"
    active_box = None

    selected_bg_index = 0
    bg_files = [
        "assets/backgrounds/background1.png",
        "assets/backgrounds/background2.png",
        "assets/backgrounds/background3.png",
    ]

    input_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 24)
    # to use later
    title_font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 32)

    character_width, charcter_height = 400, 409
    char1_img = pygame.image.load(
        "assets/player_1/player_1_poster.png"
    ).convert_alpha()
    char2_img = pygame.image.load(
        "assets/player_2/player_2_poster.png"
    ).convert_alpha()
    char1_img = pygame.transform.smoothscale(
        char1_img, (character_width, charcter_height)
    )
    char2_img = pygame.transform.smoothscale(
        char2_img, (character_width, charcter_height)
    )

    character_between_gap = 650
    char1_rect = char1_img.get_rect(
        center=(screen_w // 2 - character_between_gap, screen_h // 2 + 100)
    )
    char2_rect = char2_img.get_rect(
        center=(screen_w // 2 + character_between_gap, screen_h // 2 + 100)
    )

    box1_rect = pygame.Rect(char1_rect.centerx - 150, char1_rect.bottom + 10, 300, 50)
    box2_rect = pygame.Rect(char2_rect.centerx - 150, char2_rect.bottom + 10, 300, 50)

    bg_thumbnails = []
    bg_rects = []
    spacing = 250 
    total_width = (len(bg_files) - 1) * spacing
    start_x = (screen_w // 2) - (total_width // 2)
    for i, path in enumerate(bg_files):
        img = pygame.image.load(path).convert_alpha()
        bg_thumbnails.append(pygame.transform.smoothscale(img, (200, 110)))
        rect = pygame.Rect(0, 0, 200, 110)
        rect.center = (start_x + (i * spacing), char1_rect.top + 450)
        bg_rects.append(rect)

    start_img = pygame.transform.scale(
        pygame.image.load("assets/button/start_game.png").convert_alpha(), (400, 150)
    )
    start_rect = start_img.get_rect(center=(screen_w // 2, char1_rect.top + 80))

    quit_img = pygame.transform.scale(
        pygame.image.load("assets/button/quit_game.png").convert_alpha(), (340, 150)
    )
    quit_rect = quit_img.get_rect(center=(screen_w // 2, char1_rect.top + 200))

    while True:
        mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), real)
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, r in enumerate(bg_rects):
                    if r.collidepoint(mouse_pos):
                        selected_bg_index = i

                if box1_rect.collidepoint(mouse_pos):
                    active_box = 1
                elif box2_rect.collidepoint(mouse_pos):
                    active_box = 2
                else:
                    active_box = None

            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_BACKSPACE:
                    if active_box == 1:
                        name1 = name1[:-1]
                    else:
                        name2 = name2[:-1]
                else:
                    if active_box == 1:
                        name1 += event.unicode
                    else:
                        name2 += event.unicode

        bg_preview = pygame.image.load(bg_files[selected_bg_index]).convert()
        bg_preview = pygame.transform.scale(bg_preview, VIRTUAL_SIZE)
        bg_preview.set_alpha(150)
        screen.blit(bg_preview, (0, 0))

        bg_choice_title = input_font.render("SELECT BACKGROUND", True, (255, 255, 255))
        screen.blit(
            bg_choice_title,
            bg_choice_title.get_rect(center=(screen_w // 2, char1_rect.top + 300)),
        )
        for i, r in enumerate(bg_rects):
            screen.blit(bg_thumbnails[i], r.topleft)
            if i == selected_bg_index:
                pygame.draw.rect(screen, (0, 255, 255), r, 4)

        screen.blit(char1_img, char1_rect)
        screen.blit(char2_img, char2_rect)

        n1_surf = input_font.render(
            name1, True, (0, 255, 255) if active_box == 1 else (255, 255, 255)
        )
        n2_surf = input_font.render(
            name2, True, (0, 255, 255) if active_box == 2 else (255, 255, 255)
        )
        screen.blit(
            n1_surf,
            n1_surf.get_rect(center=(char1_rect.centerx, char1_rect.bottom + 40)),
        )
        screen.blit(
            n2_surf,
            n2_surf.get_rect(center=(char2_rect.centerx, char2_rect.bottom + 40)),
        )

        screen.blit(start_img, start_rect)
        screen.blit(quit_img, quit_rect)

        if start_rect.collidepoint(mouse_pos) and mouse_click:
            return name1, name2, bg_files[selected_bg_index]
        
        if quit_rect.collidepoint(mouse_pos) and mouse_click:
            pygame.quit(); sys.exit()

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

