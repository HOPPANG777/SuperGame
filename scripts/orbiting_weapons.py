"""OrbitingWeapons - 회전 무기 L/R 애니메이션."""
import math

import pygame

from scripts.paths import load_image
from scripts.sprite_anim import FrameAnimator, SpriteSheet, mirror_animator

WEAPON_FRAME_SIZE = 32
WEAPON_DISPLAY_SIZE = (56, 56)
WEAPON_ANIM_FPS = 12


class Weapon(pygame.sprite.Sprite):
    """플레이어 주변을 도는 무기 — 중심 기준 좌/우 스프라이트."""

    def __init__(self, anim_right: FrameAnimator, anim_left: FrameAnimator):
        super().__init__()
        self.anim_right = anim_right
        self.anim_left = anim_left
        self.facing_right = True
        self.angle = 0.0
        self._apply_image()

    def set_facing_from_angle(self) -> None:
        """cos(angle) >= 0 이면 오른쪽(플레이어 중심 지나 반대편에서 L/R 전환)."""
        facing_right = math.cos(self.angle) >= 0
        if facing_right != self.facing_right:
            self.facing_right = facing_right
        self._apply_image()

    def _apply_image(self) -> None:
        anim = self.anim_right if self.facing_right else self.anim_left
        self.image = anim.get_surface()
        if self.rect is not None:
            center = self.rect.center
            self.rect = self.image.get_rect(center=center)
        else:
            self.rect = self.image.get_rect()


class OrbitingWeapons:
    """360도 배치 + Cos/Sin, 무기마다 L/R 애니메이션."""

    def __init__(self, radius: int = 70):
        self.radius = radius
        self.angle = 0.0
        self.rotate_speed = 0.003
        self.count = 3
        self.group = pygame.sprite.Group()
        self._anim_right, self._anim_left = self._create_shared_anims()

    def _create_shared_anims(self) -> tuple[FrameAnimator, FrameAnimator]:
        def load_axe(path: str) -> FrameAnimator:
            sheet = load_image(path)
            frames = SpriteSheet(
                sheet, WEAPON_FRAME_SIZE, scale=WEAPON_DISPLAY_SIZE
            ).frames
            return FrameAnimator(frames, fps=WEAPON_ANIM_FPS, loop=True)

        anim_right = load_axe("Weapon/Axe_Thrown_R.png")
        anim_left = mirror_animator(anim_right)
        return anim_right, anim_left

    def set_count(self, count: int) -> None:
        self.count = max(1, count)

    def update(self, player_center: tuple[int, int], dt: float) -> None:
        self.angle += self.rotate_speed * dt
        self._anim_right.update(dt)
        self._anim_left.update(dt)
        self.group.empty()

        cx, cy = player_center
        for i in range(self.count):
            angle = self.angle + (math.pi * 2 / self.count) * i
            wx = cx + math.cos(angle) * self.radius
            wy = cy + math.sin(angle) * self.radius

            weapon = Weapon(self._anim_right, self._anim_left)
            weapon.angle = angle
            weapon.set_facing_from_angle()
            weapon.rect.center = (int(wx), int(wy))
            self.group.add(weapon)

    def draw(self, screen: pygame.Surface) -> None:
        self.group.draw(screen)
