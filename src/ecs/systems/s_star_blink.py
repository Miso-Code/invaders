from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar


def system_star_blink(world, delta_time):
    components = world.get_components(CTransform, CSurface, CBlink, CTagStar)

    for entity, (c_transform, c_surface, c_blink, _) in components:
        c_blink.blink_timer += delta_time
        if c_blink.blink_timer >= c_blink.blink_rate:
            c_blink.blink_timer = 0
            c_surface.surface.set_alpha(0 if c_surface.surface.get_alpha() == 255 else 255)
