"""플레이 중 HUD."""
import math

import pygame

from scripts.constants import FRAGMENTS_PER_WEAPON, WINDOW_WIDTH
from scripts.fonts import GameFonts
from scripts.lives_ui import LivesUI


class HUD:
    """점수·시간·목숨 UI."""

    def __init__(self, lives_ui: LivesUI) -> None:
        self.lives_ui = lives_ui

    def draw(
        self,
        screen: pygame.Surface,
        fonts: GameFonts,
        *,
        remaining_ms: int,
        score: int,
        kills: int,
        fragment_buffer: int,
        weapon_count: int,
        lives: int,
    ) -> None:
        remaining_sec = math.ceil(remaining_ms / 1000)
        mins, secs = divmod(remaining_sec, 60)
        time_text = fonts.sm.render(
            f"남은 시간: {mins:02d}:{secs:02d}", True, (30, 30, 30)
        )
        score_text = fonts.sm.render(
            f"점수: {score}  처치: {kills}  조각: {fragment_buffer}/{FRAGMENTS_PER_WEAPON}",
            True,
            (30, 30, 30),
        )
        weapon_text = fonts.sm.render(f"무기 수: {weapon_count}", True, (30, 30, 30))
        screen.blit(time_text, (16, 12))
        screen.blit(score_text, (16, 40))
        screen.blit(weapon_text, (16, 68))
        self.lives_ui.draw(screen, fonts.sm, lives, WINDOW_WIDTH)
