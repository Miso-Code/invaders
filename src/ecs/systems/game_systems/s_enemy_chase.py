from math import sqrt

import esper
from src.constants import EnemyChasingStatus
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.systems.game_systems.s_enemies_chaser_selector import system_enemy_chasers_selector
from src.engine.services.service_locator import ServiceLocator

sound_service = ServiceLocator.sounds_service


def system_enemy_jump(world, delta_time, enemy_transform, enemy_metadata, player_entity, screen):
    stop_jump = enemy_metadata.chasing_data.get("stop_jump", False)
    chase_speed = enemy_metadata.chasing_speed

    player_transform = world.component_for_entity(player_entity, CTransform)
    player_metadata = world.component_for_entity(player_entity, CMetadata)

    if enemy_transform.position.x < player_transform.position.x:
        direction = 1
    else:
        direction = -1
    position_x = (abs(enemy_transform.position.x - player_transform.position.x)) * delta_time * direction * 0.7
    enemy_transform.position.x += position_x
    if not stop_jump:
        min_jump_height = 1
        enemy_transform.position.y -= (2 * chase_speed) * delta_time + min_jump_height

        enemy_metadata.chasing_data["stop_jump"] = False

        if enemy_transform.position.y < enemy_metadata.ghost_position[1] - 30:
            enemy_metadata.chasing_data["stop_jump"] = True
    else:
        enemy_transform.position.y += chase_speed * delta_time

        distance = sqrt((player_transform.position.x - enemy_transform.position.x) ** 2 + (player_transform.position.y - enemy_transform.position.y) ** 2)

        if distance > 50 and enemy_transform.position.y >= screen.height - 30 or player_metadata.is_killed:
            if enemy_transform.position.x < player_transform.position.x:
                direction = -1
            else:
                direction = 1
            enemy_transform.position.x += direction * chase_speed * delta_time
            enemy_transform.position.y += chase_speed * delta_time

        if enemy_transform.position.y >= screen.height:
            enemy_transform.position.y = 0
            enemy_metadata.chasing_data["chasing_status"] = EnemyChasingStatus.RETURNING


def system_enemy_return(world, delta_time, enemy_transform, enemy_metadata, player_entity, screen):
    chase_speed = enemy_metadata.chasing_speed
    if enemy_transform.position.x < enemy_metadata.ghost_position[0]:
        direction = 1
    else:
        direction = -1
    enemy_transform.position.x += (chase_speed + abs(enemy_transform.position.x - enemy_metadata.ghost_position[0])) * direction * delta_time
    offset = 1
    x_diff = abs(enemy_transform.position.x - enemy_metadata.ghost_position[0])
    y_diff = abs(enemy_transform.position.y - enemy_metadata.ghost_position[1])

    enemy_transform.position.y += chase_speed * delta_time * 0.5

    enemy_metadata.chasing_data["sprite_is_rotated"] = False

    if x_diff <= offset and y_diff <= offset:
        enemy_transform.position.x = enemy_metadata.ghost_position[0]
        enemy_transform.position.y = enemy_metadata.ghost_position[1]
        enemy_metadata.is_chasing = False
        enemy_metadata.chasing_data["is_playing_sound"] = False
        enemy_metadata.chasing_data["chasing_status"] = EnemyChasingStatus.STOP


def system_enemy_chase(world: esper.World, delta_time: float, player_entity, screen, enemy_cfg, player_is_alive) -> None:
    if player_is_alive:
        system_enemy_chasers_selector(world, delta_time)

    components = world.get_components(CTransform, CSpeed, CSurface, CMetadata, CTagEnemy)
    system_selector = {
        EnemyChasingStatus.JUMPING: system_enemy_jump,
        EnemyChasingStatus.RETURNING: system_enemy_return,
    }
    for entity, (c_transform, c_speed, c_surface, c_metadata, _) in components:
        if c_metadata.is_chasing:
            is_playing_sound = c_metadata.chasing_data.get("is_playing_sound", False)
            if not is_playing_sound:
                sound_service.play(enemy_cfg.launch_sound)
                c_metadata.chasing_data["is_playing_sound"] = True
            system_selector[c_metadata.chasing_data["chasing_status"]](world, delta_time, c_transform, c_metadata, player_entity, screen.get_rect())
