from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_player_respawn(world, delta_time, screen, player_cfg):
    for entity, (c_metadata, c_transform, c_surface) in world.get_components(CMetadata, CTransform, CSurface):
        if hasattr(c_metadata, "type") and c_metadata.type == "player" and (c_metadata.is_killed or c_metadata.is_respawning):
            c_metadata.respawn_timer -= delta_time
            if c_metadata.respawn_timer <= 0 < c_metadata.lives:
                c_metadata.is_killed = False
                c_metadata.is_respawning = False
                c_metadata.respawn_timer = player_cfg.respawn_time
                screen_width, screen_height = screen.get_size()
                player_size = c_surface.surface.get_size()
                c_transform.position.x = screen_width / 2 - (player_size[0] / 2)
                c_transform.position.y = screen_height - player_size[1] - 10
