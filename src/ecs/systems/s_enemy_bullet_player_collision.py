from src.create.prefabs import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.services.service_locator import ServiceLocator
from src.utils import get_relative_area

sound_service = ServiceLocator.sounds_service


def system_enemy_bullet_player_collision(world, explosion_cfg):
    components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    player_killed = False
    for entity, (bullet_surface, bullet_transform, _) in components:
        bullet_rect = bullet_surface.surface.get_rect(topleft=bullet_transform.position)
        player_components = world.get_components(CSurface, CTransform, CTagPlayer)
        for player_entity, (c_surface, c_transform, _) in player_components:
            player_rect = get_relative_area(c_surface.area, c_transform.position)
            if player_rect.colliderect(bullet_rect):
                create_explosion(world, c_transform, c_surface, explosion_cfg)
                sound_service.play(explosion_cfg.sound)

                world.delete_entity(entity)
                world.delete_entity(player_entity)
                player_killed = True
                break
    return player_killed
