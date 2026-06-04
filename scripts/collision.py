"""충돌 처리 - pygame.sprite.collide API 사용."""
import pygame


def collide_weapons_and_enemies(
    weapons: pygame.sprite.Group,
    enemies: pygame.sprite.Group,
) -> list[pygame.sprite.Sprite]:
    """
    무기와 적 충돌 시 적 제거 (강의: groupcollide, dokill=True).
    반환: 이번 프레임에 처치된 Enemy 목록.
    """
    hits_map = pygame.sprite.groupcollide(weapons, enemies, False, True)
    killed: list[pygame.sprite.Sprite] = []
    for enemy_list in hits_map.values():
        killed.extend(enemy_list)
    return killed


def player_hit_by_enemies(
    player: pygame.sprite.Sprite,
    enemies: pygame.sprite.Group,
) -> int:
    """플레이어와 충돌한 적 제거 후 피격 횟수 반환."""
    hits = pygame.sprite.spritecollide(player, enemies, True)
    return len(hits)


def collide_player_and_fragments(
    player: pygame.sprite.Sprite,
    fragments: pygame.sprite.Group,
) -> int:
    """플레이어가 조각 획득 시 조각 제거 후 개수 반환."""
    collected = pygame.sprite.spritecollide(player, fragments, True)
    return len(collected)
