import pygame

from src.constants import EnemyChasingStatus
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.services.service_locator import ServiceLocator
from src.engine.wrapper import PyGameWrapper
from src.utils import set_animation

engine = PyGameWrapper().engine

image_service = ServiceLocator.images_service


def system_enemy_state(world, enemy_cfg):
    components = world.get_components(CTransform, CSurface, CMetadata, CTagEnemy)

    for entity, (c_transform, c_surface, c_metadata, c_tag) in components:
        try:
            c_animation = world.component_for_entity(entity, CAnimation)
        except KeyError:
            c_animation = None
        if c_metadata.is_chasing:
            current_enemy_cfg = getattr(enemy_cfg, c_tag.type)
            pivot_image = image_service.get(current_enemy_cfg.pivot_image)
            if c_animation is not None:
                set_animation(c_animation, 0)
            if c_metadata.chasing_data["chasing_status"] == EnemyChasingStatus.STOP:
                _do_stop_state(c_surface)
            elif c_metadata.chasing_data["chasing_status"] == EnemyChasingStatus.JUMPING:
                _do_rotate(c_surface, c_metadata, c_animation, pivot_image, -5, validator=lambda x: x >= -180)
            elif c_metadata.chasing_data["chasing_status"] == EnemyChasingStatus.RETURNING:
                _do_rotate(c_surface, c_metadata, c_animation, pivot_image, 5, validator=lambda x: x <= 0)
            _do_rotate_sprite(c_surface, c_metadata, c_tag, current_enemy_cfg, c_animation)


def _do_stop_state(c_surface: CSurface):
    c_surface.angle = 0


def _do_rotate(c_surface, c_metadata, c_animation, pivot_image, increment, validator):
    if c_metadata.chasing_data["chasing_status"] in [EnemyChasingStatus.JUMPING, EnemyChasingStatus.RETURNING]:
        angle = c_surface.angle + increment
        if validator(angle):
            c_surface.rotate(pivot_image, increment)
            if c_animation is not None:
                c_animation.is_enabled = False
        else:
            if c_animation is not None:
                c_animation.is_enabled = True


def _do_rotate_sprite(c_surface, c_metadata, c_tag, current_enemy_cfg, c_animation):
    if c_animation and c_animation.is_enabled or c_tag.type == "enemy_4":
        if c_surface.angle >= 0:
            c_surface.angle = 0
        elif c_surface.angle <= -180:
            c_surface.angle = -180
        already_rotated = c_metadata.chasing_data["sprites_rotated"].get(c_surface.angle)
        if not already_rotated:
            current_enemy_sprite = image_service.get(current_enemy_cfg.image)
            c_surface.rotate_sprite_surface(current_enemy_sprite, c_surface.angle)
            c_metadata.chasing_data["sprites_rotated"][c_surface.angle] = current_enemy_sprite
