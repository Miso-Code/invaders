import random

import esper
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.constants import MAX_ENEMIES_PER_ROW
from src.engine.services.service_locator import ServiceLocator
from src.engine.wrapper import PyGameWrapper
from src.utils import get_relative_area

engine = PyGameWrapper().engine

image_service = ServiceLocator.images_service


def create_square(world: esper.World, surface, position, speed, tag, **kwargs):
    entity = world.create_entity()
    world.add_component(entity, surface)
    world.add_component(entity, position)
    world.add_component(entity, speed)
    world.add_component(entity, tag)

    for _, value in kwargs.items():
        world.add_component(entity, value)

    return entity


def create_sprite(world, sprite, position, **kwargs):
    entity = world.create_entity()
    world.add_component(entity, CSurface.from_surface(sprite))
    world.add_component(entity, CTransform(position))
    for _, value in kwargs.items():
        world.add_component(entity, value)
    return entity


def create_stars(world: esper.World, config, screen):
    stars_colors = [(star.r, star.g, star.b) for star in config.star_colors]
    number_of_stars = config.number_of_stars
    vertical_speed_range = [config.vertical_speed.min, config.vertical_speed.max]
    blink_rate_range = [config.blink_rate.min * 100, config.blink_rate.max * 100]
    star_size_range = [config.star_size.min, config.star_size.max]
    width = config.width
    for i in range(number_of_stars):
        speed = random.randint(*vertical_speed_range)
        blink_rate = random.randrange(*blink_rate_range) / 100
        y_size = random.randint(*star_size_range)
        x_size = width
        color = random.choice(stars_colors)
        x = random.randint(0, screen.get_width())
        y = random.randint(0, screen.get_height())
        speed_component = CSpeed(engine.Vector2(0, speed))
        surface_component = CSurface(engine.Vector2(x_size, y_size), engine.Color(*color))
        transform_component = CTransform(engine.Vector2(x, y))
        blink_component = CBlink(blink_rate)
        tag_component = CTagStar()
        star_metadata = CMetadata(
            {
                "type": "star",
            },
        )
        create_square(world, surface_component, transform_component, speed_component, tag_component, blink=blink_component, metadata=star_metadata)


def create_player(world, player_config, screen):
    player_surface = image_service.get(player_config.image)
    player_size = player_surface.get_rect().size
    screen_width, screen_height = screen.get_size()
    player_position = engine.Vector2(screen_width / 2 - (player_size[0] / 2), screen_height - player_size[1] - 10)
    player_speed = engine.Vector2(0, 0)
    player_metadata = CMetadata(
        {
            "type": "player",
            "is_killed": False,
            "is_respawning": True,
            "respawn_timer": player_config.respawn_time,
            "lives": player_config.life,
            "score": 0,
        },
    )
    return create_sprite(world, player_surface, player_position, speed=CSpeed(player_speed), tag=CTagPlayer(), metadata=player_metadata)


def create_player_bullet(world, player_cfg, player_position, player_surface):
    bullet_size = player_cfg.bullet.size
    bullet_color = player_cfg.bullet.color
    player_position = player_position.position
    bullet_surface = CSurface(engine.Vector2(bullet_size.width, bullet_size.height), engine.Color(bullet_color.r, bullet_color.g, bullet_color.b))
    bullet_speed = engine.Vector2(0, -player_cfg.bullet.speed)
    bullet_position = engine.Vector2(player_position.x + player_surface.area.width / 2 - bullet_size.width / 2, player_position.y)
    bullet_metadata = CMetadata(
        {
            "type": "player_bullet",
        },
    )
    return create_square(world, bullet_surface, CTransform(bullet_position), CSpeed(bullet_speed), CTagPlayerBullet(), metadata=bullet_metadata)


def create_enemy(world: esper.World, enemy_surface, position, speed, **kwargs):
    return create_sprite(world, enemy_surface, position, speed=CSpeed(speed), **kwargs)


def create_enemies(world: esper.World, level_config, enemy_config, screen):
    enemies_organization = level_config.enemies_organization
    initial_offset = 6
    y_offset = 15
    x_offset = 0
    max_enemies_per_row = MAX_ENEMIES_PER_ROW
    enemies = [[None for _ in range(max_enemies_per_row)] for _ in range(len(enemies_organization))]
    all_enemies_width = 0
    x_initial_position = 0
    x_initial_offset = 0
    y_initial_offset = 50
    for row, enemies_row in enumerate(enemies_organization):
        enemies_in_current_row = enemies_row.count
        enemy = getattr(enemy_config, enemies_row.type)
        enemy_surface = image_service.get(enemy.image)
        enemy_size = enemy_surface.get_rect().size
        if not all_enemies_width:
            all_enemies_width = ((enemy_size[0] / 5) * enemies_in_current_row) + (initial_offset * enemies_in_current_row)
        if not x_initial_position:
            x_initial_position = abs(screen.get_width() - all_enemies_width) / 2
        x_position = x_initial_position
        y_position = y_offset * enemies_row.position + y_initial_offset
        loops_to_wait = 0
        if enemies_row.count < max_enemies_per_row:
            loops_to_wait = (max_enemies_per_row - enemies_in_current_row) // 2

        if enemies_row.type != "enemy_1":
            x_position -= initial_offset / 3

        for enemy_index in range(max_enemies_per_row):
            position = engine.Vector2(x_position + x_offset, y_position)
            speed = engine.Vector2(enemy.chasing_speed, 0)
            tag = CTagEnemy(type=enemies_row.type)
            if not x_initial_offset:
                x_initial_offset = enemy_size[0] / max_enemies_per_row + initial_offset

            x_offset += x_initial_offset + initial_offset
            enemy_metadata = CMetadata(
                {
                    "type": "enemy",
                    "bullet_cfg": enemy.bullet,
                    "chasing_speed": enemy.chasing_speed,
                    "is_chasing": False,
                    "is_killed": False,
                    "points": enemy.points,
                },
            )
            if hasattr(enemy, "animations") and loops_to_wait <= enemy_index < (enemies_in_current_row + loops_to_wait):
                animations = CAnimation(enemy.animations)
                enemies[row][enemy_index] = create_enemy(world, enemy_surface, position, speed, tag=tag, animations=animations, metadata=enemy_metadata)
            elif enemy_index == 3 or enemy_index == 6:
                position.x -= 1
                enemies[row][enemy_index] = create_enemy(world, enemy_surface, position, speed, tag=tag, metadata=enemy_metadata)
        x_offset = 0
    return enemies


def create_enemy_bullet(world, enemy_bullet_config, enemy_position, enemy_surface):
    bullet_size = enemy_bullet_config.size
    bullet_color = enemy_bullet_config.color
    enemy_position = enemy_position.position
    bullet_surface = CSurface(engine.Vector2(bullet_size.width, bullet_size.height), engine.Color(bullet_color.r, bullet_color.g, bullet_color.b))
    bullet_speed = engine.Vector2(0, enemy_bullet_config.speed)
    bullet_position = engine.Vector2(enemy_position.x + enemy_surface.area.width / 2 - bullet_size.width / 2, enemy_position.y)
    bullet_metadata = CMetadata(
        {
            "type": "enemy_bullet",
        },
    )
    return create_square(world, bullet_surface, CTransform(bullet_position), CSpeed(bullet_speed), CTagEnemyBullet(), metadata=bullet_metadata)


def create_explosion(world, position, surface, config):
    # ToDo: Check explosion animation
    explosion_size = get_relative_area(surface.area, position.position).size
    explosion_position = engine.Vector2(position.position.x + surface.area.width / 2 - explosion_size[0] / 2, position.position.y + surface.area.height / 2 - explosion_size[1] / 2)
    explosion_surface = image_service.get(config.image)
    animations = CAnimation(config.animations)
    explosion_metadata = CMetadata(
        {
            "type": "explosion",
        },
    )
    return create_sprite(world, explosion_surface, explosion_position, tag=CTagExplosion(), animations=animations, metadata=explosion_metadata)


def create_inputs(world: esper.World):
    # Keyboard inputs
    space_input = world.create_entity()
    left_input = world.create_entity()
    right_input = world.create_entity()
    a_input = world.create_entity()
    d_input = world.create_entity()
    p_input = world.create_entity()

    world.add_component(space_input, CInputCommand("PLAYER_FIRE", engine.K_SPACE))
    world.add_component(left_input, CInputCommand("PLAYER_LEFT", engine.K_LEFT))
    world.add_component(a_input, CInputCommand("PLAYER_LEFT", engine.K_a))
    world.add_component(right_input, CInputCommand("PLAYER_RIGHT", engine.K_RIGHT))
    world.add_component(d_input, CInputCommand("PLAYER_RIGHT", engine.K_d))
    world.add_component(p_input, CInputCommand("PAUSE", engine.K_p))


def create_main_menu_inputs(world: esper.World):
    # Keyboard inputs
    start_game_input = world.create_entity()
    world.add_component(start_game_input, CInputCommand("START_GAME", engine.K_SPACE))
