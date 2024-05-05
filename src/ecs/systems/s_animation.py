import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: float):
    components = world.get_components(CAnimation, CSurface)

    for _, (c_animation, c_surface) in components:
        c_animation.current_animation_time -= delta_time
        if c_animation.current_animation_time <= 0:
            c_animation.current_frame += 1
            c_animation.current_animation_time = c_animation.animation_list[c_animation.current_animation].framerate
            if c_animation.current_frame >= c_animation.animation_list[c_animation.current_animation].end:
                c_animation.current_frame = c_animation.animation_list[c_animation.current_animation].start
            rect_surface = c_surface.surface.get_rect()
            c_surface.area.w = rect_surface.w / c_animation.number_frames
            c_surface.area.x = c_surface.area.w * c_animation.current_frame
