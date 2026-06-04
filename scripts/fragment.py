"""Fragment 클래스 - 적 처치 시 드롭되는 조각."""
import pygame

from scripts.paths import load_image


class Fragment(pygame.sprite.Sprite):
    """적 처치 시 드롭되는 조각."""

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = load_image("Piece.png", (20, 20))
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = 8000
        self.spawn_time = pygame.time.get_ticks()

    def update(self, _dt: float) -> None:
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
