import esper
from src.constants import BORDER_SIZE
from src.constants import PlayerMovement
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer

border = BORDER_SIZE


def system_movement_player(world: esper.World, delta_time: float, screen, player_cfg) -> None:
    components = world.get_components(CSpeed, CTransform, CSurface, CMetadata, CTagPlayer)

    for entity, (player_speed, player_transform, c_surface, c_metadata, _) in components:
        player_speed.speed.x = player_cfg.speed
        player_transform.position.x += player_speed.speed.x * c_metadata.player_state.value * delta_time
        width, height = c_surface.area.size
        if player_transform.position.x < border:
            player_transform.position.x = border
        if player_transform.position.x > screen.get_width() - width - border:
            player_transform.position.x = screen.get_width() - width - border
