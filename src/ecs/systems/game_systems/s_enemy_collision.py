from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.utils import get_relative_area


def system_enemy_collision(world, delta_time: float):
    components = world.get_components(CTransform, CSurface, CTagEnemy, CMetadata)

    for entity, (c_transform, c_surface, c_tag, c_metadata) in components:
        if c_metadata.is_chasing:
            enemy_rect = get_relative_area(c_surface.area, c_transform.position)

            for entity_2, (e2_transform, e2_surface, e2_tag, e2_metadata) in components:
                # ToDo: fix collision bug. Sometimes some enemies not collide over player
                if e2_metadata.is_chasing and entity != entity_2:
                    enemy2_rect = get_relative_area(e2_surface.area, e2_transform.position)
                    if enemy_rect.colliderect(enemy2_rect):
                        c_transform.position.x = e2_transform.position.x
