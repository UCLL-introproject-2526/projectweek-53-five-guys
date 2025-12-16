import pygame

BULLET_SPEED = 12
BULLET_RADIUS = 5
SHOOT_COOLDOWN_MS = 180


def rotate_image(base_img, direction):
    if direction == "RIGHT":
        return base_img
    if direction == "LEFT":
        return pygame.transform.flip(base_img, True, False)
    if direction == "UP":
        return pygame.transform.rotate(base_img, 90)
    if direction == "DOWN":
        return pygame.transform.rotate(base_img, -90)
    return base_img


def direction_to_vel(direction):
    if direction == "RIGHT":
        return (BULLET_SPEED, 0)
    if direction == "LEFT":
        return (-BULLET_SPEED, 0)
    if direction == "UP":
        return (0, -BULLET_SPEED)
    return (0, BULLET_SPEED)


class Bullet:
    def __init__(self, x, y, vx, vy, owner_id):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.owner_id = owner_id

    def update(self, scroll_v: float):
        self.x += self.vx
        self.y += self.vy + scroll_v

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, (255, 220, 0), (int(self.x), int(self.y)), BULLET_RADIUS)

    def offscreen(self, w: int, h: int) -> bool:
        return self.x < -50 or self.x > w + 50 or self.y < -50 or self.y > h + 50


class Car:
    def __init__(
        self,
        car_id: int,
        base_img: pygame.Surface,
        start_center: tuple[int, int],
        step: int,
        control: dict,
        shoot_key: int,
        restrict_horizontal_only: bool = False,
    ):
        self.id = car_id
        self.base_img = base_img
        self.step = step
        self.control = control
        self.shoot_key = shoot_key
        self.restrict_horizontal_only = restrict_horizontal_only

        self.direction = "UP"
        self.img = rotate_image(self.base_img, self.direction)
        self.rect = self.img.get_rect(center=start_center)

        self._last_shot_time = 0

    def try_move(self, dx, dy, is_on_road_func, bg_surface):
        old_center = self.rect.center

        candidate = self.rect.move(dx, dy)
        self.rect = self.img.get_rect(center=candidate.center)

        if not is_on_road_func(bg_surface, self.rect):
            self.rect.center = old_center
            return False
        return True

    def update(self, keys, is_on_road_func, bg_surface):
        dx = 0
        dy = 0

        if keys[self.control["left"]]:
            dx -= self.step
        if keys[self.control["right"]]:
            dx += self.step

        if not self.restrict_horizontal_only:
            if keys[self.control["up"]]:
                dy -= self.step
            if keys[self.control["down"]]:
                dy += self.step

        if dx != 0 or dy != 0:
            if abs(dx) > abs(dy):
                self.direction = "RIGHT" if dx > 0 else "LEFT"
            else:
                self.direction = "DOWN" if dy > 0 else "UP"

            if dx != 0 and dy != 0:
                dx = int(dx * 0.7071)
                dy = int(dy * 0.7071)

            self.img = rotate_image(self.base_img, self.direction)
            self.rect = self.img.get_rect(center=self.rect.center)
            self.try_move(dx, dy, is_on_road_func, bg_surface)
        else:
            self.img = rotate_image(self.base_img, self.direction)
            self.rect = self.img.get_rect(center=self.rect.center)

    def shoot(self, keys, now_ms: int):
        if not keys[self.shoot_key]:
            return None
        if now_ms - self._last_shot_time < SHOOT_COOLDOWN_MS:
            return None

        self._last_shot_time = now_ms
        vx, vy = direction_to_vel(self.direction)
        cx, cy = self.rect.center
        return Bullet(cx, cy, vx, vy, self.id)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.img, self.rect)
