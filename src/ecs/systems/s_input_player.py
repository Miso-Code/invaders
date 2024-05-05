from typing import Callable

import pygame.event

import esper
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_input_command import CommandPhase
from src.engine.wrapper import PyGameWrapper

engine = PyGameWrapper().engine


def system_input_player(world: esper.World, event: pygame.event.Event, do_action: Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)

    for _, command in components:
        if event.type == engine.KEYDOWN and event.key == command.key:
            command.phase = CommandPhase.START
            do_action(command)
        elif event.type == engine.KEYUP and event.key == command.key:
            command.phase = CommandPhase.END
            do_action(command)
        elif event.type == engine.KEYDOWN and event.key == engine.K_SPACE:
            command.phase = CommandPhase.START
            do_action(command)
