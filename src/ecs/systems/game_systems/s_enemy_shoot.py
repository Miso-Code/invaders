import random

import esper
from src.create.prefabs import create_enemy_bullet
from src.ecs.components.c_enemy_metadata import CEnemyMetadata
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet

max_bullets_on_screen = 5


def system_enemy_shoot(world: esper.World) -> None:
    components = world.get_components(CTransform, CSurface, CMetadata, CTagEnemy)
    random_threshold = 0.99
    bullets_in_screen = len(world.get_component(CTagEnemyBullet))
    for entity, (c_transform, c_surface, c_metadata, _) in components:
        random_number = random.random()
        if c_metadata.is_chasing:
            random_threshold = 0.80
            bullets_in_screen -= 1
        if random_number > random_threshold and bullets_in_screen < max_bullets_on_screen:
            for _ in range(c_metadata.bullet_cfg.number):
                create_enemy_bullet(world, c_metadata.bullet_cfg, c_transform, c_surface)
