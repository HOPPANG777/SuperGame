"""OrbitingWeapons - Cos/Sin 원운동 무기 (Sprite Group)."""
import math

import pygame

from scripts.paths import load_image


class Weapon(pygame.sprite.Sprite):
    """플레이어 주변을 도는 단일 무기 스프라이트."""

    def __init__(self, image: pygame.Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()


class OrbitingWeapons:
    """360도 균등 배치 + Cos/Sin 좌표 갱신."""

    def __init__(self, radius: int = 70):
        self.image = load_image("Weapon.png", (30, 30))
        self.radius = radius
        self.angle = 0.0
        self.rotate_speed = 0.003
        self.count = 3
        self.group = pygame.sprite.Group()

    def set_count(self, count: int) -> None:
        self.count = max(1, count)

    def update(self, player_center: tuple[int, int], dt: float) -> None:
        self.angle += self.rotate_speed * dt
        self.group.empty()

        cx, cy = player_center
        for i in range(self.count):
            angle = self.angle + (math.pi * 2 / self.count) * i
            wx = cx + math.cos(angle) * self.radius
            wy = cy + math.sin(angle) * self.radius
            weapon = Weapon(self.image)
            weapon.rect.center = (int(wx), int(wy))
            self.group.add(weapon)

    def draw(self, screen: pygame.Surface) -> None:
        self.group.draw(screen)
