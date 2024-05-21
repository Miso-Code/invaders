from src.constants import PlayerMovement
from src.create.prefabs import create_explosion
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.game_systems.utils import remove_all_player_bullets
from src.engine.services.service_locator import ServiceLocator
from src.utils import get_relative_area

sound_service = ServiceLocator.sounds_service


def system_enemy_bullet_player_collision(world, explosion_cfg):
    components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    for entity, (bullet_surface, bullet_transform, _) in components:
        bullet_rect = bullet_surface.surface.get_rect(topleft=bullet_transform.position)
        player_components = world.get_components(CSurface, CTransform, CTagPlayer, CMetadata)
        for player_entity, (c_surface, c_transform, _, c_metadata) in player_components:
            player_rect = get_relative_area(c_surface.area, c_transform.position)
            if player_rect.colliderect(bullet_rect) and not c_metadata.is_respawning and not c_metadata.is_killed:
                create_explosion(world, c_transform, c_surface, explosion_cfg)
                sound_service.play(explosion_cfg.sound)
                c_metadata.is_killed = True
                c_metadata.is_respawning = True
                c_metadata.lives -= 1
                c_metadata.player_state = PlayerMovement.STOP
                remove_all_player_bullets(world)
                break
