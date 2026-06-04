"""Player 클래스 - WASD 이동 + 방향별 스프라이트 애니메이션."""
import pygame

from scripts.paths import load_image
from scripts.sprite_anim import FrameAnimator, SpriteSheet, mirror_animator

# 뱀파이어 서바이벌 느낌: 초당 이동 픽셀
MOVE_SPEED = 200

PLAYER_FRAME_SIZE = 32
PLAYER_DISPLAY_SIZE = (80, 80)
PLAYER_ANIM_FPS = 10
DEATH_ANIM_FPS = 14


class Player(pygame.sprite.Sprite):
    """WASD로 일정 속도 이동하는 플레이어."""

    def __init__(self, screen_size: tuple[int, int]):
        super().__init__()
        self.screen_width, self.screen_height = screen_size
        self._load_animations()

        self.pos = pygame.math.Vector2(self.screen_width // 2, self.screen_height // 2)
        self.rect = self.image.get_rect(center=self.pos)

        self.facing_right = True
        self.is_dying = False
        self._current_anim: FrameAnimator = self._idle_anim

    def _load_sheet_anim(
        self, path: str, fps: float, loop: bool = True
    ) -> FrameAnimator:
        sheet = load_image(path)
        frames = SpriteSheet(
            sheet, PLAYER_FRAME_SIZE, scale=PLAYER_DISPLAY_SIZE
        ).frames
        return FrameAnimator(frames, fps=fps, loop=loop)

    def _load_animations(self) -> None:
        """R 시트 기준 재생, L은 mirror_animator로 동일 순서 유지."""
        base = "Player"
        self._idle_right = self._load_sheet_anim(
            f"{base}/Player_Idle_R.png", PLAYER_ANIM_FPS
        )
        self._idle_left = mirror_animator(self._idle_right)

        self._run_right = self._load_sheet_anim(
            f"{base}/Player_Run_R.png", PLAYER_ANIM_FPS + 4
        )
        self._run_left = mirror_animator(self._run_right)

        self._died_right = self._load_sheet_anim(
            f"{base}/Player_Died_R.png", DEATH_ANIM_FPS, loop=False
        )
        self._died_left = mirror_animator(self._died_right)

        self._idle_anim = self._idle_right
        self._current_anim = self._idle_anim
        self.image = self._current_anim.get_surface()

    def _pick_anim(self, moving: bool) -> FrameAnimator:
        if self.is_dying:
            facing = getattr(self, "_death_facing_right", self.facing_right)
            return self._died_right if facing else self._died_left
        if moving:
            return self._run_right if self.facing_right else self._run_left
        return self._idle_right if self.facing_right else self._idle_left

    def _read_move_input(self, keys: pygame.key.ScancodeWrapper) -> pygame.math.Vector2:
        move = pygame.math.Vector2(0, 0)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if move.length_squared() > 0:
            return move.normalize()
        return move

    def update(self, keys: pygame.key.ScancodeWrapper, dt: float) -> None:
        if self.is_dying:
            self._current_anim.update(dt)
            self.image = self._current_anim.get_surface()
            self.rect = self.image.get_rect(center=self.rect.center)
            return

        move_dir = self._read_move_input(keys)
        moving = move_dir.length_squared() > 0

        if moving:
            self.pos += move_dir * MOVE_SPEED * (dt / 1000.0)
            if move_dir.x != 0:
                self.facing_right = move_dir.x > 0

        new_anim = self._pick_anim(moving)
        if new_anim is not self._current_anim:
            new_anim.reset()
            self._current_anim = new_anim

        self._current_anim.update(dt)
        self.image = self._current_anim.get_surface()

        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))
        self.pos.update(self.rect.center)

    def start_death(self) -> None:
        self.is_dying = True
        self._death_facing_right = self.facing_right
        death_anim = self._died_right if self._death_facing_right else self._died_left
        death_anim.reset()
        self._current_anim = death_anim
        self.image = self._current_anim.get_surface()
        self.rect = self.image.get_rect(center=self.rect.center)

    def is_death_finished(self) -> bool:
        return self.is_dying and self._current_anim.finished

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def reset(self) -> None:
        self.is_dying = False
        self.pos.update(self.screen_width // 2, self.screen_height // 2)
        self.facing_right = True
        self._idle_right.reset()
        self._current_anim = self._idle_right
        self.image = self._current_anim.get_surface()
        self.rect = self.image.get_rect(center=self.pos)
