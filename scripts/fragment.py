"""Fragment 클래스 - 적 처치 시 드롭, 근거리에서만 플레이어 쪽으로 흡입."""
import pygame

from scripts.paths import load_image

# 짧은 거리에서만 빨려 들어감 (범위 과하지 않게)
MAGNET_RANGE = 85
MAGNET_SPEED = 220
PICKUP_RADIUS = 22

FRAGMENT_LIFETIME_MS = 8000


class Fragment(pygame.sprite.Sprite):
    """적 처치 시 드롭되는 조각."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = load_image("Piece.png", (20, 20))
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()

    def update(self, player_center: tuple[int, int], dt: float) -> None:
        if pygame.time.get_ticks() - self.spawn_time > FRAGMENT_LIFETIME_MS:
            self.kill()
            return

        to_player = pygame.math.Vector2(player_center) - pygame.math.Vector2(
            self.rect.center
        )
        dist_sq = to_player.length_squared()

        if dist_sq <= PICKUP_RADIUS * PICKUP_RADIUS:
            return

        if dist_sq <= MAGNET_RANGE * MAGNET_RANGE and dist_sq > 4:
            direction = to_player.normalize()
            step = MAGNET_SPEED * (dt / 1000.0)
            self.rect.centerx += int(direction.x * step)
            self.rect.centery += int(direction.y * step)
