"""Enemy 클래스 - Cos/Sin 원형 스폰 및 화면 표시."""
import math
import random

import pygame

from scripts.paths import load_image


class Enemy(pygame.sprite.Sprite):
    """플레이어 주변 원형 경계 밖에서 Cos/Sin으로 스폰되는 적."""

    def __init__(
        self,
        player_pos: pygame.math.Vector2,
        screen_size: tuple[int, int],
        speed: float,
    ):
        super().__init__()
        self.image = load_image("Enemy.png", (32, 32))
        self.rect = self.image.get_rect()
        self.speed = speed

        width, height = screen_size
        spawn_radius = max(width, height) * 0.55
        angle = random.uniform(0, math.pi * 2)
        spawn_x = player_pos.x + math.cos(angle) * spawn_radius
        spawn_y = player_pos.y + math.sin(angle) * spawn_radius
        self.rect.center = (int(spawn_x), int(spawn_y))

        direction = pygame.math.Vector2(player_pos) - pygame.math.Vector2(self.rect.center)
        if direction.length_squared() == 0:
            direction = pygame.math.Vector2(1, 0)
        self.velocity = direction.normalize() * self.speed

    def update(self, player_pos: pygame.math.Vector2, dt: float) -> None:
        self.rect.centerx += int(self.velocity.x * dt)
        self.rect.centery += int(self.velocity.y * dt)

        direction = pygame.math.Vector2(player_pos) - pygame.math.Vector2(self.rect.center)
        if direction.length_squared() > 0:
            self.velocity = direction.normalize() * self.speed

    def is_off_screen(self, screen_size: tuple[int, int], margin: int = 80) -> bool:
        """화면 밖으로 벗어난 적은 kill() 대상 (강의: 메모리 청소)."""
        width, height = screen_size
        return (
            self.rect.right < -margin
            or self.rect.left > width + margin
            or self.rect.bottom < -margin
            or self.rect.top > height + margin
        )
