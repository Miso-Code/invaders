from typing import Any

from src.constants import EnemyChasingStatus
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def get_chasers(components: list) -> list[Any]:
    return list(filter(lambda c: c[1][-1].is_chasing and c[1][-1].chasing_data["chasing_status"] == EnemyChasingStatus.JUMPING, components))


def check_chasers_in_level(world: Any) -> bool:
    components = world.get_components(CMetadata, CTagEnemy)
    chasers = any([c[1][0].is_chasing for c in components])
    return chasers


def remove_all_player_bullets(world: Any) -> None:
    for entity, (c_metadata, _) in world.get_components(CMetadata, CTagPlayerBullet):
        world.delete_entity(entity)
