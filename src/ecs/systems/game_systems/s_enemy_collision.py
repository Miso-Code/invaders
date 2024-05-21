from src.constants import EnemyChasingStatus
from src.constants import PlayerMovement
from src.create.prefabs import create_explosion
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.game_systems.utils import remove_all_player_bullets
from src.engine.services.service_locator import ServiceLocator
from src.utils import get_relative_area

sound_service = ServiceLocator.sounds_service


def system_enemy_collision(world, explosion_cfg):
    components = world.get_components(CTransform, CSurface, CTagEnemy, CMetadata)

    for entity, (c_transform, c_surface, c_tag, c_metadata) in components:
        if c_metadata.is_chasing:
            enemy_rect = get_relative_area(c_surface.area, c_transform.position)
            player_components = world.get_components(CSurface, CTransform, CMetadata, CTagPlayer)
            for player_entity, (c_surface_player, c_transform_player, c_metadata_player, _) in player_components:
                player_rect = get_relative_area(c_surface_player.area, c_transform_player.position)
                if player_rect.colliderect(enemy_rect) and not c_metadata_player.is_respawning and not c_metadata_player.is_killed:
                    create_explosion(world, c_transform_player, c_surface_player, explosion_cfg)
                    sound_service.play(explosion_cfg.sound)
                    c_metadata_player.lives -= 1
                    c_metadata_player.is_respawning = True
                    c_metadata_player.is_killed = True
                    c_metadata_player.player_state = PlayerMovement.STOP
                    remove_all_player_bullets(world)
                    world.delete_entity(entity)
                    break


def system_enemy_collision_with_enemy(world):
    components = world.get_components(CTransform, CSurface, CTagEnemy, CMetadata)

    for entity, (c_transform, c_surface, c_tag, c_metadata) in components:
        if c_metadata.is_chasing and c_metadata.chasing_data["chasing_status"] == EnemyChasingStatus.JUMPING:
            enemy_rect = get_relative_area(c_surface.area, c_transform.position)
            other_enemy_components = world.get_components(CSurface, CTransform, CMetadata, CTagEnemy)
            for other_enemy_entity, (c_surface_enemy, c_transform_enemy, c_metadata_enemy, _) in other_enemy_components:
                if entity != other_enemy_entity and c_metadata_enemy.is_chasing and c_metadata_enemy.chasing_data["chasing_status"] == EnemyChasingStatus.JUMPING:
                    other_enemy_rect = get_relative_area(c_surface_enemy.area, c_transform_enemy.position)
                    if other_enemy_rect.colliderect(enemy_rect):
                        # make the enemies be one at the side of the other without overlapping
                        if c_transform.position.x < c_transform_enemy.position.x:
                            c_transform.position.x -= 1
                        else:
                            c_transform.position.x += 1
                        if c_transform.position.y < c_transform_enemy.position.y:
                            c_transform.position.y -= 1
                        else:
                            c_transform.position.y += 1
