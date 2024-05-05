import esper
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.constants import BORDER_SIZE

border = BORDER_SIZE


def system_movement_player(world: esper.World, delta_time: float, screen):
    components = world.get_components(CSpeed, CTransform, CSurface, CTagPlayer)

    for entity, (player_speed, player_transform, surface, _) in components:
        player_transform.position.x += player_speed.speed.x * delta_time
        player_transform.position.y += player_speed.speed.y * delta_time
        width, height = surface.area.size
        if player_transform.position.x < border:
            player_transform.position.x = border
        if player_transform.position.x > screen.get_width() - width - border:
            player_transform.position.x = screen.get_width() - width - border
