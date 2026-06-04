"""적 생성 타이머 및 스폰 로직."""
import random

import pygame

from scripts.constants import (
    BASE_SPAWN_DELAY,
    GAME_DURATION_MS,
    MIN_SPAWN_DELAY,
    SCORE_FAST_SPAWN,
    SCORE_FASTER_SPAWN,
    SCREEN_SIZE,
)
from scripts.enemy import Enemy


class EnemySpawner:
    """시간·점수 기반 적 스폰."""

    def __init__(self, enemies: pygame.sprite.Group) -> None:
        self.enemies = enemies
        self.last_spawn_time = 0
        self.spawn_delay = BASE_SPAWN_DELAY

    def reset(self) -> None:
        self.enemies.empty()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = BASE_SPAWN_DELAY

    def update_delay(self, elapsed_ms: int, score: int) -> None:
        if elapsed_ms > 120000:
            delay = MIN_SPAWN_DELAY
        elif elapsed_ms > 60000:
            delay = 700
        else:
            progress = elapsed_ms / GAME_DURATION_MS
            delay = int(
                BASE_SPAWN_DELAY - (BASE_SPAWN_DELAY - MIN_SPAWN_DELAY) * progress * 0.6
            )
        if score > SCORE_FASTER_SPAWN:
            delay = min(delay, 400)
        elif score > SCORE_FAST_SPAWN:
            delay = min(delay, 500)
        self.spawn_delay = delay

    def spawn(self, player_pos: pygame.math.Vector2, elapsed_ms: int, score: int) -> None:
        base_speed = 0.15
        speed = base_speed + min(0.25, elapsed_ms / GAME_DURATION_MS * 0.2)
        if score > SCORE_FASTER_SPAWN:
            speed += 0.08
        speed *= random.uniform(0.85, 1.15)
        self.enemies.add(Enemy(player_pos, SCREEN_SIZE, speed))

    def try_spawn(self, player_pos: pygame.math.Vector2, elapsed_ms: int, score: int) -> None:
        now = pygame.time.get_ticks()
        self.update_delay(elapsed_ms, score)
        if now - self.last_spawn_time >= self.spawn_delay:
            self.spawn(player_pos, elapsed_ms, score)
            self.last_spawn_time = now
            if elapsed_ms > 90000 and random.random() < 0.35:
                self.spawn(player_pos, elapsed_ms, score)

    def cull_offscreen(self) -> None:
        for enemy in list(self.enemies):
            if enemy.is_off_screen(SCREEN_SIZE):
                enemy.kill()
