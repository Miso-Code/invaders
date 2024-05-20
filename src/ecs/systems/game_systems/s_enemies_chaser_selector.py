import random
from typing import Any

import esper
from src.constants import EnemyChasingStatus
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def check_chasers(components: list) -> list[Any]:
    return list(filter(lambda c: c[1][0].is_chasing, components))


wait_time = 3


def system_enemy_chasers_selector(world: esper.World, delta_time) -> None:
    global wait_time

    wait_time -= delta_time
    if wait_time > 0:
        return
    components = world.get_components(CMetadata, CTagEnemy)
    chase_probability = 5
    max_chasers = 5
    wait_time = 4
    chasers = check_chasers(components)

    if len(chasers) >= max_chasers:
        return
    current_chasers_count = 0
    for index, (_, (c_metadata, _)) in enumerate(components):
        current_probability = random.randint(0, 100)
        if current_probability < chase_probability:
            c_metadata.is_chasing = True
            current_chasers_count += 1
            c_metadata.chasing_data["chasing_status"] = EnemyChasingStatus.JUMPING
            c_metadata.chasing_data["sprites_rotated"] = {}
            c_metadata.chasing_data["sync_animation"] = False
        if current_chasers_count >= max_chasers:
            break
