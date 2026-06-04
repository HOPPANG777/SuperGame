"""목숨(라이프) HUD UI."""
import pygame


class LivesUI:
    """우측 상단 하트 형태 목숨 표시."""

    def __init__(self, max_lives: int = 3) -> None:
        self.max_lives = max_lives
        self.heart_size = 22
        self.spacing = 8
        self.margin_right = 20
        self.margin_top = 14
        self.color_full = (220, 50, 60)
        self.color_empty = (120, 120, 120)
        self.color_border = (40, 40, 40)
        self.color_label = (30, 30, 30)

    def draw(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        lives: int,
        screen_width: int,
    ) -> None:
        label = font.render("LIFE", True, self.color_label)
        label_rect = label.get_rect(topright=(screen_width - self.margin_right, self.margin_top))
        screen.blit(label, label_rect)

        total_width = self.max_lives * self.heart_size + (self.max_lives - 1) * self.spacing
        start_x = screen_width - self.margin_right - total_width
        heart_y = self.margin_top + label_rect.height + 6

        for i in range(self.max_lives):
            cx = start_x + i * (self.heart_size + self.spacing) + self.heart_size // 2
            cy = heart_y + self.heart_size // 2
            if i < lives:
                self._draw_heart(screen, cx, cy, self.color_full, filled=True)
            else:
                self._draw_heart(screen, cx, cy, self.color_empty, filled=False)

    def _draw_heart(
        self,
        screen: pygame.Surface,
        cx: int,
        cy: int,
        color: tuple[int, int, int],
        filled: bool,
    ) -> None:
        r = self.heart_size // 2
        left = (cx - r // 2, cy - r // 3)
        right = (cx + r // 2, cy - r // 3)
        pygame.draw.circle(screen, color if filled else self.color_border, left, r // 2)
        pygame.draw.circle(screen, color if filled else self.color_border, right, r // 2)
        points = [
            (cx, cy + r),
            (cx - r, cy - r // 4),
            (cx + r, cy - r // 4),
        ]
        if filled:
            pygame.draw.polygon(screen, color, points)
        else:
            pygame.draw.polygon(screen, self.color_border, points, 2)
