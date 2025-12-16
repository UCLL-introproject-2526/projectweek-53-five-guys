import pygame
from entities import Car

SCREEN_W = 600
SCREEN_H = int(SCREEN_W * 0.8)

CAR_SIZE = (100, 100)
STEP = 5
SCROLL_SPEED = 5


def is_road_color(r, g, b):
    brightness = (r + g + b) / 3
    if brightness < 190 and abs(r - g) < 90 and abs(g - b) < 90:
        return True
    if brightness > 190 and g > 120 and r > 120:
        return True
    return False


def rect_is_on_road(bg_surface, rect):
    w, h = bg_surface.get_size()
    inset = max(8, rect.width // 5)

    points = [
        rect.center,
        (rect.centerx, rect.top + inset),
        (rect.centerx, rect.bottom - inset),
        (rect.left + inset, rect.centery),
        (rect.right - inset, rect.centery),
    ]

    ok = 0
    for x, y in points:
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        r, g, b, *_ = bg_surface.get_at((int(x), int(y)))
        if is_road_color(r, g, b):
            ok += 1

    return ok >= 3


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("2 Cars (classes) + Rolling Background + Shooting")

    background = pygame.image.load(r"src\img\seamless.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_W, SCREEN_H))
    bg_height = background.get_height()
    bg_y = 0

    # Two different images:
    car1_base = pygame.image.load(r"src\img\car1.png").convert_alpha()
    car2_base = pygame.image.load(r"src\img\car2.png").convert_alpha()
    car1_base = pygame.transform.scale(car1_base, CAR_SIZE)
    car2_base = pygame.transform.scale(car2_base, CAR_SIZE)

    car1 = Car(
        car_id=1,
        base_img=car1_base,
        start_center=(SCREEN_W // 2 + 80, SCREEN_H // 2),
        step=STEP,
        control={"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN},
        shoot_key=pygame.K_RCTRL,
        restrict_horizontal_only=True,  # car1 steers; UP/DOWN scrolls road
    )

    car2 = Car(
        car_id=2,
        base_img=car2_base,
        start_center=(SCREEN_W // 2 - 80, SCREEN_H // 2),
        step=STEP,
        control={"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s},
        shoot_key=pygame.K_SPACE,
        restrict_horizontal_only=False,
    )

    bullets = []

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

       
        scroll_v = 0
        if keys[pygame.K_UP]:
            bg_y += SCROLL_SPEED
            scroll_v = SCROLL_SPEED
            car1.direction = "UP"
        if keys[pygame.K_DOWN]:
            bg_y -= SCROLL_SPEED
            scroll_v = -SCROLL_SPEED
            car1.direction = "DOWN"

        bg_y %= bg_height

        car1.update(keys, rect_is_on_road, background)
        car2.update(keys, rect_is_on_road, background)

        b1 = car1.shoot(keys, now)
        if b1:
            bullets.append(b1)

        b2 = car2.shoot(keys, now)
        if b2:
            bullets.append(b2)

        for b in bullets:
            b.update(scroll_v)

        bullets = [b for b in bullets if not b.offscreen(SCREEN_W, SCREEN_H)]

        # draw
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - bg_height))

        for b in bullets:
            b.draw(screen)

        car1.draw(screen)
        car2.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
