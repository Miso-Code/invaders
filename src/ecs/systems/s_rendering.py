from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.services.service_locator import ServiceLocator

level_service = ServiceLocator.level_service


def system_rendering(world, screen):
    for entity, (c_transform, c_surface, c_metadata) in world.get_components(CTransform, CSurface, CMetadata):
        if (hasattr(c_metadata, "type") and c_metadata.type == "enemy" and not c_metadata.is_spawned) or (
            hasattr(c_metadata, "type") and c_metadata.type == "player" and c_metadata.is_killed
        ):
            continue
        screen.blit(c_surface.surface, c_transform.position, area=c_surface.area)
