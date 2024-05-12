import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explosion_removal(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)
    for entity, (c_animation, _) in components:
        if c_animation.current_frame >= c_animation.animation_list[c_animation.current_animation].end - 1:
            world.delete_entity(entity)
