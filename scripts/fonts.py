"""폰트 로드."""
import pygame


def get_font(size: int) -> pygame.font.Font:
    for name in ("malgungothic", "Malgun Gothic", "nanumgothic", "arial"):
        try:
            return pygame.font.SysFont(name, size)
        except pygame.error:
            continue
    return pygame.font.Font(None, size)


class GameFonts:
    """자주 쓰는 폰트 크기 묶음."""

    def __init__(self) -> None:
        self.lg = get_font(56)
        self.md = get_font(32)
        self.sm = get_font(24)
