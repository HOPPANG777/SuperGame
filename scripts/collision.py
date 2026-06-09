"""충돌 처리 - 스프라이트 rect보다 작은 히트박스로 판정."""
import pygame

# 보이는 크기에 맞게 살짝 축소 (1.0 = 이미지 전체)
PLAYER_HITBOX_SCALE = 0.74
ENEMY_HITBOX_SCALE = 0.78
WEAPON_HITBOX_SCALE = 0.72


def hitbox_rect(sprite: pygame.sprite.Sprite, scale: float) -> pygame.Rect:
    """중심 유지, 가로·세로만 scale 비율로 줄인 충돌 영역."""
    base = sprite.rect
    w = max(4, int(base.width * scale))
    h = max(4, int(base.height * scale))
    hitbox = pygame.Rect(0, 0, w, h)
    hitbox.center = base.center
    return hitbox


def _collided_weapon_enemy(
    weapon: pygame.sprite.Sprite, enemy: pygame.sprite.Sprite
) -> bool:
    return hitbox_rect(weapon, WEAPON_HITBOX_SCALE).colliderect(
        hitbox_rect(enemy, ENEMY_HITBOX_SCALE)
    )


def _collided_player_enemy(
    player: pygame.sprite.Sprite, enemy: pygame.sprite.Sprite
) -> bool:
    return hitbox_rect(player, PLAYER_HITBOX_SCALE).colliderect(
        hitbox_rect(enemy, ENEMY_HITBOX_SCALE)
    )


def _collided_player_fragment(
    player: pygame.sprite.Sprite, fragment: pygame.sprite.Sprite
) -> bool:
    return hitbox_rect(player, PLAYER_HITBOX_SCALE).colliderect(fragment.rect)


def collide_weapons_and_enemies(
    weapons: pygame.sprite.Group,
    enemies: pygame.sprite.Group,
) -> list[pygame.sprite.Sprite]:
    """
    무기와 적 충돌 시 적 제거 (강의: groupcollide, dokill=True).
    반환: 이번 프레임에 처치된 Enemy 목록.
    """
    hits_map = pygame.sprite.groupcollide(
        weapons, enemies, False, True, collided=_collided_weapon_enemy
    )
    killed: list[pygame.sprite.Sprite] = []
    for enemy_list in hits_map.values():
        killed.extend(enemy_list)
    return killed


def player_hit_by_enemies(
    player: pygame.sprite.Sprite,
    enemies: pygame.sprite.Group,
) -> int:
    """플레이어와 충돌한 적 제거 후 피격 횟수 반환."""
    hits = pygame.sprite.spritecollide(
        player, enemies, True, collided=_collided_player_enemy
    )
    return len(hits)


def collide_player_and_fragments(
    player: pygame.sprite.Sprite,
    fragments: pygame.sprite.Group,
) -> int:
    """플레이어가 조각 획득 시 조각 제거 후 개수 반환."""
    collected = pygame.sprite.spritecollide(
        player, fragments, True, collided=_collided_player_fragment
    )
    return len(collected)
