import pygame

from src.constants import EnemyChasingStatus
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.wrapper import PyGameWrapper

engine = PyGameWrapper().engine


def system_rotate_enemy(world, delta_time: float, player_position):
    components = world.get_components(CTransform, CSurface, CMetadata, CTagEnemy)
    for _, (c_transform, c_surface, c_metadata, _) in components:
        rotation_angle = c_metadata.chasing_data.get("rotation_angle", 0)
        if not rotation_angle:
            c_metadata.chasing_data["rotation_angle"] = 0
        chasing_status = c_metadata.chasing_data.get("chasing_status", None)
        if c_metadata.is_chasing and chasing_status == EnemyChasingStatus.JUMPING:
            # Calculate the rotation angle based on the direction to the player
            direction = 1 if c_transform.position.x < player_position.x else -1
            rotation_speed = 10  # Adjust the rotation speed as needed
            rotation_angle += rotation_speed * direction * delta_time  # Adjust by delta_time
            # Ensure rotation angle stays within 0 to 360 degrees
            rotation_angle %= 180
            # Update the rotation angle in the enemy's metadata
            c_metadata.chasing_data["rotation_angle"] = rotation_angle

            # Rotate the enemy sprite surface
            rotated_surface = engine.transform.rotate(c_surface.surface, -rotation_angle)
            rotated_rect = rotated_surface.get_rect(center=c_transform.position)  # Use the original position
            # Adjust the position to ensure the rotated sprite fits within the desired area
            if rotated_rect.width > c_surface.surface.get_width() or rotated_rect.height > c_surface.surface.get_height():
                # If the rotated sprite doesn't fit within the original area, move it back
                rotated_rect.center = c_transform.position
            c_surface.surface = rotated_surface
            c_transform.position = rotated_rect.center  # Update the position
