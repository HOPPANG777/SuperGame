"""게임 상태 머신 및 메인 루프."""
import pygame

from scripts.audio_manager import AudioManager
from scripts.background import Background
from scripts.constants import (
    BACKGROUND_COLOR,
    FPS,
    INITIAL_WEAPON_COUNT,
    STATE_CLEAR,
    STATE_DYING,
    STATE_GAMEOVER,
    STATE_PLAY,
    STATE_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)
from scripts.enemy_spawner import EnemySpawner
from scripts.fonts import GameFonts
from scripts.hud import HUD
from scripts.lives_ui import LivesUI
from scripts.orbiting_weapons import OrbitingWeapons
from scripts.play_session import PlaySession
from scripts.player import Player
from scripts.screens import ScreenRenderer
from scripts.constants import MAX_LIVES, SCREEN_SIZE


class GameManager:
    """타이틀 → 플레이 → 클리어/사망 → 게임오버 흐름 총괄."""

    def __init__(self) -> None:
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption("Super Game")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.fonts = GameFonts()
        self.audio = AudioManager()
        self.background = Background()
        self.screens = ScreenRenderer()

        self.player = Player(SCREEN_SIZE)
        self.weapons = OrbitingWeapons()
        self.weapons.set_count(INITIAL_WEAPON_COUNT)
        self.enemies = pygame.sprite.Group()
        self.fragments = pygame.sprite.Group()
        self.spawner = EnemySpawner(self.enemies)
        self.hud = HUD(LivesUI(MAX_LIVES))

        self.session = PlaySession(
            self.player,
            self.weapons,
            self.spawner,
            self.fragments,
            self.hud,
            self.background,
            self.audio,
            self.screens,
            self.fonts,
        )

        self.state = STATE_TITLE
        self.running = True

    def start_play(self) -> None:
        self.state = STATE_PLAY
        self.session.reset()
        self.audio.play_sfx(self.audio.sfx_start)
        self.audio.start_bgm()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

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

            keys = pygame.key.get_pressed()
            if self.state == STATE_PLAY:
                next_state = self.session.update(keys, dt)
                if next_state:
                    self.state = next_state
                self.session.draw(self.screen)

            elif self.state == STATE_DYING:
                next_state = self.session.update_dying(dt)
                if next_state:
                    self.state = next_state
                self.session.draw_dying(self.screen)

            elif self.state == STATE_TITLE:
                self.screens.draw_title(self.screen, self.fonts)

            elif self.state == STATE_CLEAR:
                self.screens.draw_clear(self.screen, self.fonts, self.session.score)

            elif self.state == STATE_GAMEOVER:
                self.background.draw(self.screen, BACKGROUND_COLOR)
                self.screens.draw_gameover(
                    self.screen,
                    self.fonts,
                    self.player,
                    self.session.score,
                    self.session.kills,
                )

            pygame.display.flip()

        pygame.quit()
