import random

import esper
from src.constants import EnemyChasingStatus
from src.constants import MAX_CHASERS
from src.constants import MIN_CHASERS
from src.constants import TIMER
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.systems.game_systems.utils import get_chasers
from src.engine.services.service_locator import ServiceLocator
from src.utils import randomize_elements

wait_time = TIMER

level_service = ServiceLocator.level_service


def system_enemy_chasers_selector(world: esper.World, delta_time) -> None:
    global wait_time
    min_chasers = MIN_CHASERS
    wait_time -= delta_time
    if wait_time > 0:
        return
    components = randomize_elements(world.get_components(CTagEnemy, CMetadata))
    wait_time = TIMER * 0.5
    chase_probability = 5 + level_service.level
    # limit the chase probability to 15
    if chase_probability >= 15:
        chase_probability = 15

    # increase the number of chasers if the level is higher
    max_chasers = level_service.level // 2 + min_chasers
    if max_chasers >= MAX_CHASERS:
        max_chasers = MAX_CHASERS
    chasers = get_chasers(components)
    if len(chasers) >= max_chasers:
        return
    current_chasers_count = 0
    for index, (_, (_, c_metadata)) in enumerate(components):
        current_probability = random.randint(0, 100)
        if current_chasers_count >= max_chasers:
            break
        if current_probability < chase_probability and c_metadata.is_spawned:
            c_metadata.is_chasing = True
            current_chasers_count += 1
            c_metadata.chasing_data["chasing_status"] = EnemyChasingStatus.JUMPING
            c_metadata.chasing_data["sprites_rotated"] = {}
