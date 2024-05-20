from typing import Callable

import esper
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_input_command import CommandPhase
from src.engine.wrapper import PyGameWrapper

engine = PyGameWrapper().engine


def system_input_player(world: esper.World, event: engine.event.Event, do_action: Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)

    for _, command in components:
        if event.type == engine.KEYDOWN:
            if event.key == command.key:
                command.phase = CommandPhase.START
                do_action(command)
                return
        elif event.type == engine.KEYUP:
            if event.key == command.key:
                command.phase = CommandPhase.END
                do_action(command)
                return
