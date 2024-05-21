from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet


def system_bullet_movement(components, screen, direction, delta_time, check_firing=False, player_components=(None, None)):
    _, screen_height = screen.get_size()
    entities_to_delete = []

    player_transform, player_surface = player_components

    for entity, component in components:
        bullet_speed, bullet_transform, bullet_surface, _, bullet_metadata = component
        if check_firing and player_components:
            bullet_width = bullet_surface.surface.get_width()
            if not bullet_metadata.is_fired:
                bullet_transform.position.x = player_transform.position.x + (player_surface.surface.get_width() / 2) - (bullet_width / 2)
        if check_firing and not bullet_metadata.is_fired:
            continue
        bullet_transform.position.y += bullet_speed.speed.y * delta_time * direction

        if bullet_transform.position.y < 0 or bullet_transform.position.y > screen_height:
            entities_to_delete.append(entity)

    return entities_to_delete


def system_player_bullet_movement(world, screen, delta_time, player_components):
    components = world.get_components(CSpeed, CTransform, CSurface, CTagPlayerBullet, CMetadata)

    entities_to_delete = system_bullet_movement(components, screen, 1, delta_time, check_firing=True, player_components=player_components)
    for entity in entities_to_delete:
        world.delete_entity(entity)


def system_enemy_bullet_movement(world, screen, delta_time):
    components = world.get_components(CSpeed, CTransform, CSurface, CTagEnemyBullet, CMetadata)
    entities_to_delete = system_bullet_movement(components, screen, 1, delta_time)
    for entity in entities_to_delete:
        world.delete_entity(entity)
