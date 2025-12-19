import pygame


def round_corners(surf: pygame.Surface, radius: int) -> pygame.Surface:
    w, h = surf.get_size()
    radius = max(0, min(radius, min(w, h) // 2))

    mask = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=radius)

    rounded = surf.copy()
    rounded.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return rounded


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


def manual_page(virtual, real, VIRTUAL_SIZE, blit_scaled, screen_to_virtual):
 

    popup_img = pygame.image.load("assets/Manual/manual_page.png").convert_alpha()
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

    clock = pygame.time.Clock()

    while True:
        mouse_pos = screen_to_virtual(pygame.mouse.get_pos(), real)
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        # Draw manual page
        virtual.fill((0, 0, 0))  
        should_close = draw_image_popup(
            virtual, popup_img, popup_rect, close_img, close_rect, mouse_pos, mouse_click
        )
        if should_close:
            return

        blit_scaled(real, virtual)
        pygame.display.flip()
        clock.tick(60)
