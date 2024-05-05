from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def system_bullet_movement(components, screen, direction, delta_time):
    _, screen_height = screen.get_size()
    entities_to_delete = []
    for entity, component in components:
        bullet_speed, bullet_transform, _ = component
        bullet_transform.position.y += bullet_speed.speed.y * delta_time * direction

        if bullet_transform.position.y < 0 or bullet_transform.position.y > screen_height:
            entities_to_delete.append(entity)

    return entities_to_delete


def system_player_bullet_movement(world, screen, delta_time):
    components = world.get_components(CSpeed, CTransform, CTagPlayerBullet)
    entities_to_delete = system_bullet_movement(components, screen, 1, delta_time)
    for entity in entities_to_delete:
        world.delete_entity(entity)


def system_enemy_bullet_movement(world, screen, delta_time):
    components = world.get_components(CSpeed, CTransform, CTagEnemyBullet)
    entities_to_delete = system_bullet_movement(components, screen, 1, delta_time)
    for entity in entities_to_delete:
        world.delete_entity(entity)
