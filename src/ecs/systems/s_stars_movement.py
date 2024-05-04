import random

from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar


def system_stars_movement(world, screen, delta_time):
    components = world.get_components(CTransform, CSurface, CSpeed, CTagStar)
    for entity, (c_transform, c_surface, c_speed, _) in components:
        c_transform.position.y += c_speed.speed.y * delta_time
        if c_transform.position.y > screen.get_height():
            c_transform.position.y = 0
            c_transform.position.x = random.randint(0, screen.get_width())
