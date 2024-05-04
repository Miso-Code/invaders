import random

import esper
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.wrapper import PyGameWrapper

engine = PyGameWrapper().engine


def create_stars(world: esper.World, config, screen):
    stars_colors = [(star.r, star.g, star.b) for star in config.star_colors]
    number_of_stars = config.number_of_stars
    vertical_speed_range = [config.vertical_speed.min, config.vertical_speed.max]
    blink_rate_range = [config.blink_rate.min * 100, config.blink_rate.max * 100]
    star_size_range = [config.star_size.min, config.star_size.max]
    for i in range(number_of_stars):
        speed = random.randint(*vertical_speed_range)
        blink_rate = random.randrange(*blink_rate_range) / 100
        y_size = random.randint(*star_size_range)
        x_size = 3
        color = random.choice(stars_colors)
        x = random.randint(0, screen.get_width())
        y = -10
        speed_component = CSpeed(engine.Vector2(0, speed))
        surface_component = CSurface(engine.Vector2(x_size, y_size), engine.Color(*color))
        transform_component = CTransform(engine.Vector2(x, y))
        blink_component = CBlink(blink_rate)
        tag_component = CTagStar()

        entity = world.create_entity()
        world.add_component(entity, speed_component)
        world.add_component(entity, surface_component)
        world.add_component(entity, transform_component)
        world.add_component(entity, blink_component)
        world.add_component(entity, tag_component)
