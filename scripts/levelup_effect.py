"""Levelup.png — 레벨업 링 이펙트 (하단 7프레임)."""
import pygame

from scripts.paths import load_image
from scripts.sprite_anim import FrameAnimator

LEVELUP_PATH = "Levelup.png"
LEVELUP_COLS = 5
LEVELUP_ROWS = 4
RING_START_INDEX = 10  # 3·4행: 픽셀 링 시퀀스
RING_FRAME_COUNT = 7
RING_DISPLAY_SIZE = (130, 130)
RING_ANIM_FPS = 8
RING_HOLD_MS = 550
RING_FOOT_OFFSET_Y = 12
RING_COLORKEY = (0, 0, 0)

_ring_frames_cache: list[pygame.Surface] | None = None


def _load_ring_frames() -> list[pygame.Surface]:
    global _ring_frames_cache
    if _ring_frames_cache is not None:
        return _ring_frames_cache

    sheet = load_image(LEVELUP_PATH)
    fw = sheet.get_width() // LEVELUP_COLS
    fh = sheet.get_height() // LEVELUP_ROWS
    frames: list[pygame.Surface] = []

    for n in range(RING_FRAME_COUNT):
        index = RING_START_INDEX + n
        col = index % LEVELUP_COLS
        row = index // LEVELUP_COLS
        frame = sheet.subsurface((col * fw, row * fh, fw, fh)).copy()
        frame = pygame.transform.scale(frame, RING_DISPLAY_SIZE)
        frame.set_colorkey(RING_COLORKEY)
        frames.append(frame)

    _ring_frames_cache = frames
    return _ring_frames_cache


class LevelUpEffect(pygame.sprite.Sprite):
    """플레이어 발밑 링 애니메이션 — 한 번 재생 후 삭제."""

    def __init__(self, player_center: tuple[int, int]):
        super().__init__()
        frames = _load_ring_frames()
        self.anim = FrameAnimator(frames, fps=RING_ANIM_FPS, loop=False)
        self._hold_ms = 0.0
        self.image = self.anim.get_surface()
        cx, cy = player_center
        self.rect = self.image.get_rect(center=(cx, cy + RING_FOOT_OFFSET_Y))

    def update(self, player_center: tuple[int, int], dt: float) -> None:
        if not self.anim.finished:
            self.anim.update(dt)
        else:
            self._hold_ms += dt
            if self._hold_ms >= RING_HOLD_MS:
                self.kill()
                return

        cx, cy = player_center
        self.image = self.anim.get_surface()
        self.rect = self.image.get_rect(center=(cx, cy + RING_FOOT_OFFSET_Y))


class LevelUpEffectManager:
    def __init__(self) -> None:
        self.group = pygame.sprite.Group()

    def clear(self) -> None:
        self.group.empty()

    def spawn(self, player_center: tuple[int, int]) -> None:
        self.group.add(LevelUpEffect(player_center))

    def update(self, player_center: tuple[int, int], dt: float) -> None:
        for effect in list(self.group):
            effect.update(player_center, dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.group.draw(screen)
