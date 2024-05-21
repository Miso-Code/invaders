from src.constants import PlayerMovement
from src.constants import TIMER
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.services.service_locator import ServiceLocator

level_service = ServiceLocator.level_service


def system_spawn(world, delta_time, screen, player_cfg):
    for entity, (c_metadata, c_transform, c_surface) in world.get_components(CMetadata, CTransform, CSurface):
        if hasattr(c_metadata, "type") and c_metadata.type == "player" and (c_metadata.is_killed or c_metadata.is_respawning):
            c_metadata.respawn_timer -= delta_time
            if c_metadata.respawn_timer <= 0 < c_metadata.lives:
                c_metadata.is_killed = False
                c_metadata.is_respawning = False
                c_metadata.respawn_timer = player_cfg.respawn_time
                c_metadata.player_state = PlayerMovement.STOP
                screen_width, screen_height = screen.get_size()
                player_size = c_surface.surface.get_size()
                c_transform.position.x = screen_width / 2 - (player_size[0] / 2)
                c_transform.position.y = screen_height - player_size[1] - 10
        elif hasattr(c_metadata, "type") and c_metadata.type == "enemy" and not c_metadata.is_spawned:
            if level_service.level > 1 and c_metadata.spawn_timer["current"] == c_metadata.spawn_timer["initial"]:
                c_metadata.spawn_timer["current"] = c_metadata.spawn_timer["initial"] - TIMER

            c_metadata.spawn_timer["current"] -= delta_time
            if c_metadata.spawn_timer["current"] <= 0:
                c_metadata.is_spawned = True
                c_metadata.spawn_timer["current"] = c_metadata.spawn_timer["initial"]
                level_service.enemy_spawning = False
