"""Player 클래스 - 화면에 캐릭터 표시 및 이동."""
import pygame

from scripts.paths import load_image

# 값이 작을수록 마우스를 더 천천히 따라감 (시간차)
FOLLOW_LERP = 0.004


class Player(pygame.sprite.Sprite):
    """마우스를 시간차를 두고 따라가는 플레이어(구슬)."""

    def __init__(self, screen_size: tuple[int, int]):
        super().__init__()
        self.screen_width, self.screen_height = screen_size
        self.image = load_image("Player.png", (40, 40))
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(self.screen_width // 2, self.screen_height // 2)
        self.rect.center = self.pos

    def update(self, mouse_pos: tuple[int, int], dt: float) -> None:
        target = pygame.math.Vector2(mouse_pos)
        blend = min(1.0, FOLLOW_LERP * dt)
        self.pos = self.pos.lerp(target, blend)

        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))
        self.pos.update(self.rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def reset(self) -> None:
        """게임 시작 시에만 중앙 배치."""
        self.pos.update(self.screen_width // 2, self.screen_height // 2)
        self.rect.center = self.pos
