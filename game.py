import math
import os
import random

import pygame

from scripts import (
    Enemy,
    Fragment,
    LivesUI,
    OrbitingWeapons,
    Player,
    collide_player_and_fragments,
    collide_weapons_and_enemies,
    load_sound,
    player_hit_by_enemies,
)
from scripts.paths import BGM_VOLUME, IMAGE_DIR, init_bgm, play_bgm, stop_bgm

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720
FPS = 60
BACKGROUND_COLOR = (181, 214, 146)

GAME_DURATION_MS = 3 * 60 * 1000
FRAGMENTS_PER_WEAPON = 16
INITIAL_WEAPON_COUNT = 3
BASE_SPAWN_DELAY = 1000  # 강의: 1000ms 간격 스폰
MIN_SPAWN_DELAY = 400
SCORE_FAST_SPAWN = 500
SCORE_FASTER_SPAWN = 1000
MAX_LIVES = 3
INVINCIBLE_MS = 1500

STATE_TITLE = "TITLE"
STATE_PLAY = "PLAY"
STATE_CLEAR = "CLEAR"
STATE_GAMEOVER = "GAMEOVER"


def get_font(size: int) -> pygame.font.Font:
    for name in ("malgungothic", "Malgun Gothic", "nanumgothic", "arial"):
        try:
            return pygame.font.SysFont(name, size)
        except pygame.error:
            continue
    return pygame.font.Font(None, size)


class Game:
    def __init__(self) -> None:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption("Super Game")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_lg = get_font(56)
        self.font_md = get_font(32)
        self.font_sm = get_font(24)

        self._load_assets()
        self._init_sound()
        self.reset_all()

    def _load_assets(self) -> None:
        bg_path = os.path.join(IMAGE_DIR, "background")
        try:
            bg = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except (FileNotFoundError, pygame.error):
            self.background = None

        self.weapons = OrbitingWeapons()
        self.lives_ui = LivesUI(MAX_LIVES)

    def _init_sound(self) -> None:
        self.bgm_ready = init_bgm(volume=BGM_VOLUME)
        self.sfx_start = load_sound("80_Start_01.wav", volume=0.55)
        self.sfx_clear = load_sound("25_Clear_01.wav", volume=0.6)
        self.sfx_defeat = load_sound("44_Defeat_01.wav", volume=0.6)
        self.sfx_hit = load_sound("59_Hit_01.wav", volume=0.45)
        self.sfx_pickup = load_sound("87_exp_up_1_short.wav", volume=0.45)
        self.sfx_levelup = load_sound("73_Lvl_up_01.wav", volume=0.55)
        self.sfx_hurt = load_sound("68_Die_01.wav", volume=0.45)

    def _play_sfx(self, sound: pygame.mixer.Sound | None) -> None:
        if sound:
            sound.play()

    def _start_bgm(self) -> None:
        if self.bgm_ready:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(BGM_VOLUME)
            play_bgm(loop=True, fade_ms=2500)

    def _stop_bgm(self) -> None:
        stop_bgm(fade_ms=1000)

    def reset_all(self) -> None:
        self.state = STATE_TITLE
        self.running = True
        self.player = Player((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.enemies = pygame.sprite.Group()
        self.fragments = pygame.sprite.Group()
        self.weapons.set_count(INITIAL_WEAPON_COUNT)
        self.score = 0
        self.kills = 0
        self.fragment_buffer = 0
        self.last_spawn_time = 0
        self.play_start_time = 0
        self.spawn_delay = BASE_SPAWN_DELAY
        self.lives = MAX_LIVES
        self.invincible_until = 0

    def is_invincible(self) -> bool:
        return pygame.time.get_ticks() < self.invincible_until

    def start_play(self) -> None:
        self.state = STATE_PLAY
        self.player.reset()
        self.enemies.empty()
        self.fragments.empty()
        self.weapons.set_count(INITIAL_WEAPON_COUNT)
        self.weapons.angle = 0
        self.score = 0
        self.kills = 0
        self.fragment_buffer = 0
        self.lives = MAX_LIVES
        self.invincible_until = 0
        now = pygame.time.get_ticks()
        self.play_start_time = now
        self.last_spawn_time = now
        self.spawn_delay = BASE_SPAWN_DELAY
        self._play_sfx(self.sfx_start)
        self._start_bgm()

    def elapsed_play_ms(self) -> int:
        return pygame.time.get_ticks() - self.play_start_time

    def remaining_ms(self) -> int:
        return max(0, GAME_DURATION_MS - self.elapsed_play_ms())

    def update_spawn_delay(self) -> None:
        elapsed = self.elapsed_play_ms()
        if elapsed > 120000:
            delay = MIN_SPAWN_DELAY
        elif elapsed > 60000:
            delay = 700
        else:
            progress = elapsed / GAME_DURATION_MS
            delay = int(
                BASE_SPAWN_DELAY - (BASE_SPAWN_DELAY - MIN_SPAWN_DELAY) * progress * 0.6
            )
        if self.score > SCORE_FASTER_SPAWN:
            delay = min(delay, 400)
        elif self.score > SCORE_FAST_SPAWN:
            delay = min(delay, 500)
        self.spawn_delay = delay

    def spawn_enemy(self) -> None:
        elapsed = self.elapsed_play_ms()
        base_speed = 0.15
        speed = base_speed + min(0.25, elapsed / GAME_DURATION_MS * 0.2)
        if self.score > SCORE_FASTER_SPAWN:
            speed += 0.08
        speed *= random.uniform(0.85, 1.15)
        self.enemies.add(Enemy(self.player.pos, (WINDOW_WIDTH, WINDOW_HEIGHT), speed))

    def cull_offscreen_enemies(self) -> None:
        screen = (WINDOW_WIDTH, WINDOW_HEIGHT)
        for enemy in list(self.enemies):
            if enemy.is_off_screen(screen):
                enemy.kill()

    def try_spawn_enemies(self) -> None:
        now = pygame.time.get_ticks()
        self.update_spawn_delay()
        if now - self.last_spawn_time >= self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn_time = now
            if self.elapsed_play_ms() > 90000 and random.random() < 0.35:
                self.spawn_enemy()

    def handle_collisions(self) -> None:
        killed = collide_weapons_and_enemies(self.weapons.group, self.enemies)
        for enemy in killed:
            self.kills += 1
            self.score += 10
            self.fragments.add(Fragment(enemy.rect.center))
            self._play_sfx(self.sfx_hit)

        collected = collide_player_and_fragments(self.player, self.fragments)
        for _ in range(collected):
            self.fragment_buffer += 1
            self._play_sfx(self.sfx_pickup)
            while self.fragment_buffer >= FRAGMENTS_PER_WEAPON:
                self.fragment_buffer -= FRAGMENTS_PER_WEAPON
                self.weapons.set_count(self.weapons.count + 1)
                self._play_sfx(self.sfx_levelup)

        if not self.is_invincible():
            hits = player_hit_by_enemies(self.player, self.enemies)
            if hits > 0:
                self.lives -= 1
                self.invincible_until = pygame.time.get_ticks() + INVINCIBLE_MS
                self._play_sfx(self.sfx_hurt)
                if self.lives <= 0:
                    self._stop_bgm()
                    self._play_sfx(self.sfx_defeat)
                    self.state = STATE_GAMEOVER

    def update_play(self, mouse_pos: tuple[int, int], dt: float) -> None:
        if self.remaining_ms() <= 0:
            if self.state == STATE_PLAY:
                self._stop_bgm()
                self._play_sfx(self.sfx_clear)
            self.state = STATE_CLEAR
            return

        self.player.update(mouse_pos, dt)
        self.weapons.update(self.player.rect.center, dt)
        self.try_spawn_enemies()

        for enemy in self.enemies:
            enemy.update(self.player.pos, dt)
        self.cull_offscreen_enemies()
        self.fragments.update(dt)

        self.handle_collisions()

    def draw_hud(self) -> None:
        remaining_sec = math.ceil(self.remaining_ms() / 1000)
        mins, secs = divmod(remaining_sec, 60)
        time_text = self.font_sm.render(
            f"남은 시간: {mins:02d}:{secs:02d}", True, (30, 30, 30)
        )
        score_text = self.font_sm.render(
            f"점수: {self.score}  처치: {self.kills}  조각: {self.fragment_buffer}/{FRAGMENTS_PER_WEAPON}",
            True,
            (30, 30, 30),
        )
        weapon_text = self.font_sm.render(
            f"무기 수: {self.weapons.count}", True, (30, 30, 30)
        )
        self.screen.blit(time_text, (16, 12))
        self.screen.blit(score_text, (16, 40))
        self.screen.blit(weapon_text, (16, 68))
        self.lives_ui.draw(self.screen, self.font_sm, self.lives, WINDOW_WIDTH)

    def draw_title(self) -> None:
        title = self.font_lg.render("Super Game", True, (40, 60, 120))
        sub = self.font_md.render("화면 안 생존", True, (50, 50, 50))
        guide = self.font_sm.render(
            "마우스 이동 | 3분 생존 | 조각 16개마다 무기 추가", True, (60, 60, 60)
        )
        start = self.font_md.render("SPACE 또는 ENTER 로 시작", True, (0, 100, 0))
        cx = WINDOW_WIDTH // 2
        self.screen.blit(title, title.get_rect(center=(cx, 220)))
        self.screen.blit(sub, sub.get_rect(center=(cx, 300)))
        self.screen.blit(guide, guide.get_rect(center=(cx, 380)))
        self.screen.blit(start, start.get_rect(center=(cx, 480)))

    def draw_clear(self) -> None:
        text = self.font_lg.render("CLEAR!", True, (0, 120, 0))
        sub = self.font_md.render(
            f"3분 생존 성공!  점수: {self.score}", True, (40, 40, 40)
        )
        guide = self.font_sm.render("ENTER 로 종료", True, (80, 80, 80))
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.screen.blit(text, text.get_rect(center=(cx, cy - 40)))
        self.screen.blit(sub, sub.get_rect(center=(cx, cy + 20)))
        self.screen.blit(guide, guide.get_rect(center=(cx, cy + 80)))

    def draw_gameover(self) -> None:
        text = self.font_lg.render("GAME OVER", True, (200, 0, 0))
        sub = self.font_md.render(
            f"점수: {self.score}  처치: {self.kills}", True, (40, 40, 40)
        )
        lives_line = self.font_sm.render("목숨을 모두 잃었습니다", True, (120, 40, 40))
        guide = self.font_sm.render("R: 재시작  |  ESC: 종료", True, (80, 80, 80))
        cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.screen.blit(text, text.get_rect(center=(cx, cy - 30)))
        self.screen.blit(sub, sub.get_rect(center=(cx, cy + 20)))
        self.screen.blit(lives_line, lives_line.get_rect(center=(cx, cy + 55)))
        self.screen.blit(guide, guide.get_rect(center=(cx, cy + 95)))

    def draw_play(self) -> None:
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BACKGROUND_COLOR)

        if not self.is_invincible() or (pygame.time.get_ticks() // 120) % 2 == 0:
            self.player.draw(self.screen)
        self.weapons.draw(self.screen)
        self.enemies.draw(self.screen)
        self.fragments.draw(self.screen)
        self.draw_hud()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if self.state == STATE_TITLE:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_play()
                elif self.state == STATE_CLEAR:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.running = False
                elif self.state == STATE_GAMEOVER:
                    if event.key == pygame.K_r:
                        self.start_play()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    def run(self) -> None:
        while self.running:
            self.handle_events()
            dt = self.clock.tick(FPS)
            if self.state == STATE_PLAY:
                self.update_play(pygame.mouse.get_pos(), dt)
                self.draw_play()
            elif self.state == STATE_TITLE:
                self.screen.fill(BACKGROUND_COLOR)
                self.draw_title()
            elif self.state == STATE_CLEAR:
                self.screen.fill(BACKGROUND_COLOR)
                self.draw_clear()
            elif self.state == STATE_GAMEOVER:
                self.screen.fill(BACKGROUND_COLOR)
                self.draw_gameover()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()
