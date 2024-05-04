from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_rendering(world, screen):
    for entity, (c_transform, c_surface) in world.get_components(CTransform, CSurface):
        screen.blit(c_surface.surface, c_transform.position, area=c_surface.area)
