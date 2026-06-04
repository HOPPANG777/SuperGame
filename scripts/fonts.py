"""폰트 로드 — Maplestory Bold / Light."""
import pygame

from scripts.paths import FONT_MAPLE_BOLD, FONT_MAPLE_LIGHT, load_font


def render_outlined(
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    outline_color: tuple[int, int, int],
    width: int = 2,
) -> pygame.Surface:
    """밝은 하늘 배경에서도 읽히도록 외곽선 텍스트."""
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)
    pad = width * 2
    surface = pygame.Surface(
        (base.get_width() + pad, base.get_height() + pad), pygame.SRCALPHA
    )
    ox, oy = width, width
    for dx in range(-width, width + 1):
        for dy in range(-width, width + 1):
            if dx == 0 and dy == 0:
                continue
            surface.blit(outline, (ox + dx, oy + dy))
    surface.blit(base, (ox, oy))
    return surface


class GameFonts:
    """자주 쓰는 폰트 크기 묶음."""

    def __init__(self) -> None:
        self.title = load_font(FONT_MAPLE_BOLD, 72)
        self.lg = load_font(FONT_MAPLE_BOLD, 48)
        self.md = load_font(FONT_MAPLE_BOLD, 30)
        self.sm = load_font(FONT_MAPLE_LIGHT, 22)
        self.btn = load_font(FONT_MAPLE_BOLD, 28)
