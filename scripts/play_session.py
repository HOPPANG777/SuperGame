"""플레이 중 업데이트·충돌·렌더."""
import pygame

from scripts.collision import (
    collide_player_and_fragments,
    collide_weapons_and_enemies,
    player_hit_by_enemies,
)
from scripts.constants import (
    BACKGROUND_COLOR,
    FRAGMENTS_PER_WEAPON,
    GAME_DURATION_MS,
    INITIAL_WEAPON_COUNT,
    INVINCIBLE_MS,
    MAX_LIVES,
    STATE_CLEAR,
    STATE_DYING,
    STATE_GAMEOVER,
)
from scripts.enemy_spawner import EnemySpawner
from scripts.fragment import Fragment
from scripts.fonts import GameFonts
from scripts.hud import HUD
from scripts.player import Player
from scripts.orbiting_weapons import OrbitingWeapons
from scripts.background import Background
from scripts.audio_manager import AudioManager
from scripts.hit_effect import HitEffectManager
from scripts.screens import ScreenRenderer


class PlaySession:
    """플레이 상태 로직 (이동, 스폰, 충돌, HUD)."""

    def __init__(
        self,
        player: Player,
        weapons: OrbitingWeapons,
        spawner: EnemySpawner,
        fragments: pygame.sprite.Group,
        hud: HUD,
        background: Background,
        audio: AudioManager,
        screens: ScreenRenderer,
        fonts: GameFonts,
    ) -> None:
        self.player = player
        self.weapons = weapons
        self.spawner = spawner
        self.fragments = fragments
        self.hud = hud
        self.background = background
        self.audio = audio
        self.screens = screens
        self.fonts = fonts
        self.hit_effects = HitEffectManager()

        self.score = 0
        self.kills = 0
        self.fragment_buffer = 0
        self.lives = MAX_LIVES
        self.invincible_until = 0
        self.play_start_time = 0

    def reset(self) -> None:
        self.player.reset()
        self.spawner.reset()
        self.fragments.empty()
        self.hit_effects.clear()
        self.weapons.set_count(INITIAL_WEAPON_COUNT)
        self.weapons.angle = 0
        self.score = 0
        self.kills = 0
        self.fragment_buffer = 0
        self.lives = MAX_LIVES
        self.invincible_until = 0
        self.play_start_time = pygame.time.get_ticks()

    def elapsed_ms(self) -> int:
        return pygame.time.get_ticks() - self.play_start_time

    def remaining_ms(self) -> int:
        return max(0, GAME_DURATION_MS - self.elapsed_ms())

    def is_invincible(self) -> bool:
        return pygame.time.get_ticks() < self.invincible_until

    def handle_collisions(self) -> str | None:
        """충돌 처리. 상태 변경이 필요하면 새 state 반환."""
        killed = collide_weapons_and_enemies(self.weapons.group, self.spawner.enemies)
        player_center = self.player.rect.center
        for enemy in killed:
            self.kills += 1
            self.score += 10
            self.hit_effects.spawn_at_enemy_kill(enemy.rect.center, player_center)
            self.fragments.add(Fragment(enemy.rect.center))
            self.audio.play_sfx(self.audio.sfx_hit)

        collected = collide_player_and_fragments(self.player, self.fragments)
        for _ in range(collected):
            self.fragment_buffer += 1
            self.audio.play_sfx(self.audio.sfx_pickup)
            while self.fragment_buffer >= FRAGMENTS_PER_WEAPON:
                self.fragment_buffer -= FRAGMENTS_PER_WEAPON
                self.weapons.set_count(self.weapons.count + 1)
                self.audio.play_sfx(self.audio.sfx_levelup)

        if not self.is_invincible():
            hits = player_hit_by_enemies(self.player, self.spawner.enemies)
            if hits > 0:
                self.lives -= 1
                self.hit_effects.spawn_at_player_hit(self.player.rect.center)
                self.invincible_until = pygame.time.get_ticks() + INVINCIBLE_MS
                self.audio.play_sfx(self.audio.sfx_hurt)
                if self.lives <= 0:
                    self.audio.stop_bgm()
                    self.player.start_death()
                    self.audio.play_sfx(self.audio.sfx_die)
                    return STATE_DYING
        return None

    def update(self, keys: pygame.key.ScancodeWrapper, dt: float) -> str | None:
        """플레이 업데이트. CLEAR/DYING 전환 시 state 반환."""
        if self.remaining_ms() <= 0:
            self.audio.stop_bgm()
            self.audio.play_sfx(self.audio.sfx_clear)
            return STATE_CLEAR

        self.player.update(keys, dt)
        self.weapons.update(self.player.rect.center, dt)
        self.spawner.try_spawn(self.player.pos, self.elapsed_ms(), self.score)

        for enemy in self.spawner.enemies:
            enemy.update(self.player.pos, dt)
        self.spawner.cull_offscreen()
        self.fragments.update(dt)
        next_state = self.handle_collisions()
        self.hit_effects.update(dt)
        return next_state

    def draw(self, screen: pygame.Surface) -> None:
        self.background.draw(screen, BACKGROUND_COLOR)

        if self.player.is_dying:
            self.player.draw(screen)
        elif self.is_invincible():
            if (pygame.time.get_ticks() // 120) % 2 == 0:
                self.player.draw(screen)
        else:
            self.player.draw(screen)
        self.weapons.draw(screen)
        self.spawner.enemies.draw(screen)
        self.hit_effects.draw(screen)
        self.fragments.draw(screen)
        self.hud.draw(
            screen,
            self.fonts,
            remaining_ms=self.remaining_ms(),
            score=self.score,
            kills=self.kills,
            fragment_buffer=self.fragment_buffer,
            weapon_count=self.weapons.count,
            lives=self.lives,
        )

    def update_dying(self, dt: float) -> str | None:
        self.player.update(pygame.key.get_pressed(), dt)
        if self.player.is_death_finished():
            return STATE_GAMEOVER
        return None

    def draw_dying(self, screen: pygame.Surface) -> None:
        self.background.draw(screen, BACKGROUND_COLOR)
        self.spawner.enemies.draw(screen)
        self.player.draw(screen)
