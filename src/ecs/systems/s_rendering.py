from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_rendering(world, screen):
    for entity, (c_transform, c_surface, c_metadata) in world.get_components(CTransform, CSurface, CMetadata):
        if hasattr(c_metadata, "type") and c_metadata.type == "player" and c_metadata.is_respawning:
            continue
        screen.blit(c_surface.surface, c_transform.position, area=c_surface.area)
