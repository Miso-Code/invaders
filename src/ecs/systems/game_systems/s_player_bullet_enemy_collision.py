from src.create.prefabs import create_explosion
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.engine.services.service_locator import ServiceLocator
from src.utils import get_relative_area

sound_service = ServiceLocator.sounds_service


def system_player_bullet_enemy_collision(world, explosion_cfg):
    components = world.get_components(CSurface, CTransform, CTagPlayerBullet, CMetadata)
    score = 0
    for entity, (bullet_surface, bullet_transform, _, bullet_metadata) in components:
        bullet_rect = bullet_surface.surface.get_rect(topleft=bullet_transform.position)
        enemies_components = world.get_components(CSurface, CTransform, CMetadata, CTagEnemy)
        for enemy_entity, (enemy_surface, enemy_transform, c_metadata, _) in enemies_components:
            enemy_rect = get_relative_area(enemy_surface.area, enemy_transform.position)
            if enemy_rect.colliderect(bullet_rect) and c_metadata.is_spawned and bullet_metadata.is_fired:
                sound_service.play(explosion_cfg.sound)
                score = c_metadata.points
                world.delete_entity(entity)
                world.delete_entity(enemy_entity)
                create_explosion(world, enemy_transform, enemy_surface, explosion_cfg)
                break
    return score
