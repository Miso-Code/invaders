import random

import esper
from src.constants import TIMER
from src.create.prefabs import create_enemy_bullet
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.systems.game_systems.utils import get_chasers
from src.utils import randomize_elements

max_bullets_on_screen = 5
bullets_timer = TIMER * 0.5
random_threshold = 95


def system_enemy_shoot(world: esper.World, delta_time) -> None:
    global bullets_timer
    global random_threshold
    global max_bullets_on_screen
    bullets_timer -= delta_time
    if bullets_timer > 0:
        return
    bullets_timer = TIMER
    components = randomize_elements(world.get_components(CTransform, CSurface, CTagEnemy, CMetadata))
    bullets_in_screen = len(world.get_component(CTagEnemyBullet))
    bullets_count = 0

    chasers = get_chasers(components)

    for entity, (c_transform, c_surface, _, c_metadata) in chasers:
        random_number = random.randint(0, 100)
        if random_number > (random_threshold - 40) and bullets_in_screen <= max_bullets_on_screen + 5 and c_metadata.is_spawned:
            bullets = random.randint(1, c_metadata.bullet_cfg.number)
            for _ in range(bullets):
                create_enemy_bullet(world, c_metadata.bullet_cfg, c_transform, c_surface)
                bullets_count += 1

    chasers_entities = [entity for entity, _ in chasers]

    for entity, (c_transform, c_surface, _, c_metadata) in components:
        random_number = random.randint(0, 100)
        if random_number > random_threshold and bullets_in_screen <= max_bullets_on_screen and entity not in chasers_entities:
            for _ in range(c_metadata.bullet_cfg.number):
                if bullets_count >= max_bullets_on_screen or not c_metadata.is_spawned:
                    break
                bullets = random.randint(1, c_metadata.bullet_cfg.number)
                for _ in range(bullets):
                    create_enemy_bullet(world, c_metadata.bullet_cfg, c_transform, c_surface)
                    bullets_count += 1
