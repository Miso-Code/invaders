from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_transform import CTransform


def system_accelerate_menu_position(world, limit):
    components = world.get_components(CTransform, CMetadata)

    for _, (c_transform, c_metadata) in components:
        c_transform.position.y = limit + c_metadata.offset
