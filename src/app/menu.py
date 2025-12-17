import pygame
import sys

VIRTUAL_SIZE = (1920, 1080)

GAME_PLAYING = "playing"
GAME_END = "end"

game_state = GAME_PLAYING
clock = pygame.time.Clock()


def startpage(screen, real):
    clock.tick(120)
    screen_w, screen_h = (1920, 1080)

    name1 = "Player 1"
    name2 = "Player 2"
    active_box = None

    input_font = pygame.font.Font("assets/font/Kaijuz.ttf", 24)

    # background only (logo removed)fa
    menu_bg = pygame.image.load("assets/background.png").convert_alpha()
    menu_bg = pygame.transform.scale(menu_bg, screen.get_size())
    menu_bg.set_alpha(200)

    start_img = pygame.image.load("assets/button/start_game.png").convert_alpha()
    quit_img = pygame.image.load("assets/button/quit_game.png").convert_alpha()

    start_img = pygame.transform.scale(start_img, (360, 75))
    quit_img = pygame.transform.scale(quit_img, (360, 75))

    # ============================================================
    # CHARACTER CHOOSER (center-ish)
    char1_img = pygame.image.load(
        "assets/character/player_1_poster_choosing.png"
    ).convert_alpha()
    char2_img = pygame.image.load(
        "assets/character/player_2_poster_choosing.png"
    ).convert_alpha()

    char1_img = pygame.transform.scale(char1_img, (240, 340))
    char2_img = pygame.transform.scale(char2_img, (240, 340))

    choose_center_x = screen_w * 0.50
    choose_center_y = screen_h * 0.62
    char_gap = 60

    char1_rect = char1_img.get_rect(
        center=(
            choose_center_x - char1_img.get_width() // 2 - char_gap // 2,
            choose_center_y,
        )
    )
    char2_rect = char2_img.get_rect(
        center=(
            choose_center_x + char2_img.get_width() // 2 + char_gap // 2,
            choose_center_y,
        )
    )

    box_width = 180
    box_height = 32
    box_gap = 14

    box1_rect = pygame.Rect(
        char1_rect.centerx - box_width // 2,
        char1_rect.bottom + box_gap,
        box_width,
        box_height,
    )
    box2_rect = pygame.Rect(
        char2_rect.centerx - box_width // 2,
        char2_rect.bottom + box_gap,
        box_width,
        box_height,
    )
    # ============================================================

    # ============================================================
    # START + QUIT (placed ABOVE the chooser)
    buttons_center_x = choose_center_x
    buttons_y = char1_rect.top - 220  # position above characters
    gap = 110

    start_rect = start_img.get_rect(center=(buttons_center_x, buttons_y))
    quit_rect = quit_img.get_rect(center=(buttons_center_x, buttons_y + gap))
    # ============================================================

    error_message = ""
    error_font = pygame.font.Font("assets/font/Kaijuz.ttf", 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), real)
                if box1_rect.collidepoint(mouse_pos):
                    active_box = 1
                elif box2_rect.collidepoint(mouse_pos):
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

        mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), real)
        mouse_click = pygame.mouse.get_pressed()[0]

        # ---------------- START + QUIT (above chooser) ----------------
        if start_rect.collidepoint(mouse_pos):
            hover_img = pygame.transform.scale(
                start_img, (int(start_rect.width * 1.1), int(start_rect.height * 1.1))
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

        if quit_rect.collidepoint(mouse_pos):
            hover_img = pygame.transform.scale(
                quit_img, (int(quit_rect.width * 1.1), int(quit_rect.height * 1.1))
            )
            hover_rect = hover_img.get_rect(center=quit_rect.center)
            screen.blit(hover_img, hover_rect)

            if mouse_click:
                pygame.quit()
                sys.exit()
        else:
            screen.blit(quit_img, quit_rect)

        # ---------------- CHARACTER CHOOSER ----------------
        screen.blit(char1_img, char1_rect)
        screen.blit(char2_img, char2_rect)

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

        if error_message != "":
            error_surf = error_font.render(error_message, True, (255, 80, 80))
            error_rect = error_surf.get_rect(center=(screen_w // 2, screen_h * 0.5))
            screen.blit(error_surf, error_rect)

        blit_scaled(real, screen)
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
