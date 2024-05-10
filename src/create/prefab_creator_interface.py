from enum import Enum

import esper
from src.create.prefabs import create_square
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_text import CTagText
from src.engine.services.service_locator import ServiceLocator
from src.engine.wrapper import PyGameWrapper

text_service = ServiceLocator.text_service
engine = PyGameWrapper().engine


class TextAlignment(Enum):
    LEFT = (0,)
    RIGHT = 1
    CENTER = 2


def create_text(world: esper.World, txt: str, size: int, color, position, interface_cfg, alignment=None, blink=None, metadata=None) -> int:
    font = text_service.get(interface_cfg.font, size)

    text_surface = CSurface.from_text(txt, font, color)
    origin = engine.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= text_surface.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= text_surface.area.centerx
    kwargs = {}
    if blink:
        kwargs.update({"blink": CBlink(1)})
    if metadata:
        kwargs.update({"metadata": metadata})
    speed = engine.Vector2(0, 0)
    entity = create_square(world, text_surface, CTransform(position=(position + origin)), CSpeed(speed), CTagText(), **kwargs)
    return entity
