"""Panel1.png 기반 메뉴 버튼."""
import pygame

from scripts.paths import IMAGE_PANEL, load_image

PANEL_COLORKEY = (0, 0, 0)
PANEL_SIZE = (300, 72)
HOVER_DARKEN = 0.55


def _deepen_color(color: tuple[int, int, int], factor: float = HOVER_DARKEN) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(c * factor))) for c in color)


class MenuButton:
    """클릭 가능한 패널 버튼 — 호버 시 글자색 진하게."""

    def __init__(
        self,
        label: str,
        center: tuple[int, int],
        font: pygame.font.Font,
        text_color: tuple[int, int, int],
        action: str,
        panel_size: tuple[int, int] = PANEL_SIZE,
    ) -> None:
        self.label = label
        self.action = action
        self._normal_color = text_color
        self._hover_color = _deepen_color(text_color)
        self.font = font
        self._hovered = False

        panel = load_image(IMAGE_PANEL)
        panel.set_colorkey(PANEL_COLORKEY)
        self._panel = pygame.transform.smoothscale(panel, panel_size)
        self.rect = self._panel.get_rect(center=center)

        self._refresh_label()

    def _refresh_label(self) -> None:
        color = self._hover_color if self._hovered else self._normal_color
        self._label_surf = self.font.render(self.label, True, color)
        self._label_rect = self._label_surf.get_rect(center=self.rect.center)

    def set_hovered(self, hovered: bool) -> None:
        if hovered == self._hovered:
            return
        self._hovered = hovered
        self._refresh_label()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self._panel, self.rect)
        screen.blit(self._label_surf, self._label_rect)

    def contains(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)
