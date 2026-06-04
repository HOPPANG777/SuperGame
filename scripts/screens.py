"""타이틀 / 클리어 / 사망 / 게임오버 화면."""
import pygame

from scripts.constants import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH
from scripts.fonts import GameFonts
from scripts.player import Player


class ScreenRenderer:
    """상태별 화면 그리기."""

    def _draw_dim_overlay(self, screen: pygame.Surface, alpha: int = 100) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

    def draw_title(self, screen: pygame.Surface, fonts: GameFonts) -> None:
        screen.fill(BACKGROUND_COLOR)
        title = fonts.lg.render("Super Game", True, (40, 60, 120))
        sub = fonts.md.render("화면 안 생존", True, (50, 50, 50))
        guide = fonts.sm.render(
            "WASD 이동 | 3분 생존 | 조각 16개마다 무기 추가", True, (60, 60, 60)
        )
        start = fonts.md.render("SPACE 또는 ENTER 로 시작", True, (0, 100, 0))
        cx = WINDOW_WIDTH // 2
        screen.blit(title, title.get_rect(center=(cx, 220)))
        screen.blit(sub, sub.get_rect(center=(cx, 300)))
        screen.blit(guide, guide.get_rect(center=(cx, 380)))
        screen.blit(start, start.get_rect(center=(cx, 480)))

    def draw_clear(
        self, screen: pygame.Surface, fonts: GameFonts, score: int
    ) -> None:
        screen.fill(BACKGROUND_COLOR)
        text = fonts.lg.render("CLEAR!", True, (0, 120, 0))
        sub = fonts.md.render(f"3분 생존 성공!  점수: {score}", True, (40, 40, 40))
        guide = fonts.sm.render("ENTER 로 종료", True, (80, 80, 80))
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        screen.blit(text, text.get_rect(center=(cx, cy - 40)))
        screen.blit(sub, sub.get_rect(center=(cx, cy + 20)))
        screen.blit(guide, guide.get_rect(center=(cx, cy + 80)))

    def draw_gameover(
        self,
        screen: pygame.Surface,
        fonts: GameFonts,
        player: Player,
        score: int,
        kills: int,
    ) -> None:
        """GAME OVER — 화면 정중앙."""
        if player.is_dying:
            player.draw(screen)

        self._draw_dim_overlay(screen)

        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        title = fonts.lg.render("GAME OVER", True, (220, 50, 50))
        sub = fonts.md.render(
            f"점수: {score}  처치: {kills}", True, (240, 240, 240)
        )
        guide = fonts.sm.render("R: 재시작  |  ESC: 종료", True, (200, 200, 200))

        screen.blit(title, title.get_rect(center=(cx, cy - 50)))
        screen.blit(sub, sub.get_rect(center=(cx, cy + 10)))
        screen.blit(guide, guide.get_rect(center=(cx, cy + 55)))
