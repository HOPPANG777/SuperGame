"""타이틀 / 클리어 / 패배 화면 — 배경 이미지 + Panel 버튼."""
import pygame

from scripts.constants import (
    STATE_CLEAR,
    STATE_GAMEOVER,
    STATE_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from scripts.fonts import GameFonts, render_outlined
from scripts.paths import (
    IMAGE_CLEAR_BG,
    IMAGE_DEFEAT_BG,
    IMAGE_TITLE_BG,
    load_image,
)
from scripts.ui_button import MenuButton

# 타이틀 — 하늘 위에서 잘 보이게
TITLE_COLOR = (255, 238, 120)
TITLE_OUTLINE = (35, 45, 85)
SUBTITLE_COLOR = (255, 255, 255)
SUBTITLE_OUTLINE = (30, 50, 90)
SCORE_COLOR = (240, 240, 240)

COLOR_BTN_CLEAR = (25, 150, 55)
COLOR_BTN_DEFEAT = (200, 40, 45)

# 승리·패배 — 배경 큰 글자(중앙) / 점수 / 버튼 세로 분리
RESULT_STATS_Y = 500
RESULT_BTN_Y = 660
RESULT_BTN_SPREAD = 170

ACTION_START = "start"
ACTION_RESTART = "restart"
ACTION_TITLE = "title"
ACTION_QUIT = "quit"


class ScreenRenderer:
    """상태별 화면 그리기 및 버튼 클릭."""

    def __init__(self) -> None:
        self._title_bg = self._scaled_bg(load_image(IMAGE_TITLE_BG))
        self._defeat_bg = self._scaled_bg(load_image(IMAGE_DEFEAT_BG))
        self._clear_bg = self._scaled_bg(load_image(IMAGE_CLEAR_BG))

        self.title_buttons: list[MenuButton] = []
        self.clear_buttons: list[MenuButton] = []
        self.gameover_buttons: list[MenuButton] = []

    @staticmethod
    def _scaled_bg(image: pygame.Surface) -> pygame.Surface:
        if image.get_size() == (WINDOW_WIDTH, WINDOW_HEIGHT):
            return image
        return pygame.transform.smoothscale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def _layout_buttons(self, fonts: GameFonts) -> None:
        cx = WINDOW_WIDTH // 2
        btn_x = 920

        self.title_buttons = [
            MenuButton(
                "게임 시작",
                (btn_x, 400),
                fonts.btn,
                (50, 90, 50),
                ACTION_START,
            ),
        ]

        half = RESULT_BTN_SPREAD // 2
        self.clear_buttons = [
            MenuButton(
                "타이틀로",
                (cx - half, RESULT_BTN_Y),
                fonts.btn,
                COLOR_BTN_CLEAR,
                ACTION_TITLE,
            ),
            MenuButton(
                "종료",
                (cx + half, RESULT_BTN_Y),
                fonts.btn,
                COLOR_BTN_CLEAR,
                ACTION_QUIT,
            ),
        ]

        self.gameover_buttons = [
            MenuButton(
                "다시하기",
                (cx - half, RESULT_BTN_Y),
                fonts.btn,
                COLOR_BTN_DEFEAT,
                ACTION_RESTART,
            ),
            MenuButton(
                "타이틀로",
                (cx + half, RESULT_BTN_Y),
                fonts.btn,
                COLOR_BTN_DEFEAT,
                ACTION_TITLE,
            ),
        ]

    def ensure_layout(self, fonts: GameFonts) -> None:
        if not self.title_buttons:
            self._layout_buttons(fonts)

    def _buttons_for(self, state: str) -> list[MenuButton]:
        if state == STATE_TITLE:
            return self.title_buttons
        if state == STATE_CLEAR:
            return self.clear_buttons
        if state == STATE_GAMEOVER:
            return self.gameover_buttons
        return []

    def update_hover(self, state: str, mouse_pos: tuple[int, int]) -> None:
        for btn in self._buttons_for(state):
            btn.set_hovered(btn.contains(mouse_pos))

    def _draw_buttons(self, screen: pygame.Surface, buttons: list[MenuButton]) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            btn.set_hovered(btn.contains(mouse_pos))
            btn.draw(screen)

    def handle_click(self, state: str, pos: tuple[int, int]) -> str | None:
        for btn in self._buttons_for(state):
            if btn.contains(pos):
                return btn.action
        return None

    def draw_title(self, screen: pygame.Surface, fonts: GameFonts) -> None:
        self.ensure_layout(fonts)
        screen.blit(self._title_bg, (0, 0))

        title = render_outlined(
            fonts.title, "Super Game", TITLE_COLOR, TITLE_OUTLINE, width=3
        )
        sub = render_outlined(
            fonts.sm,
            "WASD 이동 · 3분 생존 · 조각 16개마다 무기 추가",
            SUBTITLE_COLOR,
            SUBTITLE_OUTLINE,
            width=2,
        )
        screen.blit(title, title.get_rect(midtop=(WINDOW_WIDTH // 2, 48)))
        screen.blit(sub, sub.get_rect(midtop=(WINDOW_WIDTH // 2, 132)))

        self._draw_buttons(screen, self.title_buttons)

    def draw_clear(
        self, screen: pygame.Surface, fonts: GameFonts, score: int
    ) -> None:
        self.ensure_layout(fonts)
        screen.blit(self._clear_bg, (0, 0))

        score_surf = fonts.sm.render(f"점수: {score}", True, SCORE_COLOR)
        screen.blit(
            score_surf,
            score_surf.get_rect(center=(WINDOW_WIDTH // 2, RESULT_STATS_Y)),
        )

        self._draw_buttons(screen, self.clear_buttons)

    def draw_gameover(
        self,
        screen: pygame.Surface,
        fonts: GameFonts,
        score: int,
        kills: int,
    ) -> None:
        """패배 화면 — 막혔다2 배경 + 빨간 버튼."""
        self.ensure_layout(fonts)
        screen.blit(self._defeat_bg, (0, 0))

        stats = fonts.sm.render(
            f"점수: {score}  ·  처치: {kills}", True, SCORE_COLOR
        )
        screen.blit(
            stats,
            stats.get_rect(center=(WINDOW_WIDTH // 2, RESULT_STATS_Y)),
        )

        self._draw_buttons(screen, self.gameover_buttons)
