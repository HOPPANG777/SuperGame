"""배경 이미지 로드."""
import os

import pygame

from scripts.constants import SCREEN_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from scripts.paths import IMAGE_DIR


class Background:
    """플레이 화면 배경."""

    def __init__(self) -> None:
        self.surface: pygame.Surface | None = None
        path = os.path.join(IMAGE_DIR, "background") # 백그라운드 이미지 없는편이 나을듯
        try:
            bg = pygame.image.load(path).convert()
            self.surface = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except (FileNotFoundError, pygame.error):
            pass

    def draw(self, screen: pygame.Surface, fill_color: tuple[int, int, int]) -> None:
        if self.surface:
            screen.blit(self.surface, (0, 0))
        else:
            screen.fill(fill_color)
