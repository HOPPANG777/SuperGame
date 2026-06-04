"""Hit.png 피격 이펙트 (5x6 시트, 30프레임 — 혈흔 스플래터)."""
import pygame

from scripts.paths import load_image
from scripts.sprite_anim import FrameAnimator, GridSpriteSheet

HIT_SHEET_PATH = "Hit.png"
HIT_COLS = 5
HIT_ROWS = 6
HIT_FRAME_COUNT = 30  # 5열 x 6행, 좌→우·위→아래 순서
HIT_DISPLAY_SIZE = (120, 120)
HIT_ANIM_FPS = 22
HIT_COLORKEY = (0, 0, 0)

_frames_cache: list[pygame.Surface] | None = None


def _load_hit_frames() -> list[pygame.Surface]:
    global _frames_cache
    if _frames_cache is None:
        sheet = load_image(HIT_SHEET_PATH)
        _frames_cache = GridSpriteSheet(
            sheet,
            HIT_COLS,
            HIT_ROWS,
            HIT_FRAME_COUNT,
            scale=HIT_DISPLAY_SIZE,
            colorkey=HIT_COLORKEY,
        ).frames
    return _frames_cache


def clear_hit_frame_cache() -> None:
    """Hit.png 교체 후 캐시 초기화용."""
    global _frames_cache
    _frames_cache = None


class HitEffect(pygame.sprite.Sprite):
    """한 번 재생 후 자동 삭제되는 피격 이펙트."""

    def __init__(self, pos: tuple[int, int], flip_x: bool = False):
        super().__init__()
        base_frames = _load_hit_frames()
        if flip_x:
            self._frames = [
                pygame.transform.flip(f, True, False) for f in base_frames
            ]
        else:
            self._frames = base_frames
        self.anim = FrameAnimator(self._frames, fps=HIT_ANIM_FPS, loop=False)
        self.image = self.anim.get_surface()
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt: float) -> None:
        self.anim.update(dt)
        if self.anim.finished:
            self.kill()
            return
        center = self.rect.center
        self.image = self.anim.get_surface()
        self.rect = self.image.get_rect(center=center)


class HitEffectManager:
    """피격 이펙트 그룹 관리."""

    def __init__(self) -> None:
        self.group = pygame.sprite.Group()

    def clear(self) -> None:
        self.group.empty()

    def spawn(self, pos: tuple[int, int], flip_x: bool = False) -> None:
        self.group.add(HitEffect(pos, flip_x=flip_x))

    def spawn_at_enemy_kill(
        self, enemy_center: tuple[int, int], player_center: tuple[int, int]
    ) -> None:
        """적 처치 위치에 혈흔 이펙트."""
        flip_x = enemy_center[0] < player_center[0]
        self.spawn(enemy_center, flip_x=flip_x)

    def spawn_at_player_hit(self, player_center: tuple[int, int]) -> None:
        """플레이어 피격 위치에 혈흔 이펙트."""
        self.spawn(player_center, flip_x=False)

    def update(self, dt: float) -> None:
        self.group.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.group.draw(screen)
