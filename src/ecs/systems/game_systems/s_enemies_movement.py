import esper
from src.ecs.components.c_enemy_metadata import CEnemyMetadata
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.constants import BORDER_SIZE

border = BORDER_SIZE * 3
speed_direction = -1


def system_enemies_movement(world: esper.World, delta_time: float, screen) -> None:
    global speed_direction
    components = world.get_components(CTransform, CSurface, CTagEnemy, CMetadata)
    most_left_enemy = None
    most_right_enemy = None
    for entity, (c_transform, c_surface, c_tag, c_metadata) in components:
        if most_left_enemy is None or c_transform.position.x < most_left_enemy[0]:
            most_left_enemy = c_transform.position
        if most_right_enemy is None or c_transform.position.x > most_right_enemy[0]:
            most_right_enemy = c_transform.position

    if most_left_enemy is not None and most_left_enemy.x < border:
        speed_direction = 1
    if most_right_enemy is not None and most_right_enemy.x > screen.get_width() - border:
        speed_direction = -1

    components = world.get_components(CTransform, CTagEnemy, CSpeed)
    for _, (c_transform, _, c_speed) in components:
        c_transform.position.x += c_speed.speed.x * delta_time * speed_direction
