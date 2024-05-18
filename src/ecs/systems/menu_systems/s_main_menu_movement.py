import esper
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.constants import BORDER_SIZE

border = BORDER_SIZE
any_touches_limit = False


def system_main_menu_movement(world: esper.World, delta_time, limit):
    components = world.get_components(CSpeed, CTransform, CSurface, CMetadata)
    global any_touches_limit

    if not any_touches_limit:
        for entity, (c_speed, c_transform, c_surface, c_metadata) in components:
            if hasattr(c_metadata, "scene") and c_metadata.scene == "main_menu":
                if c_transform.position.y <= limit:
                    any_touches_limit = True
                    break
                c_transform.position.y -= 50 * delta_time
    return any_touches_limit
