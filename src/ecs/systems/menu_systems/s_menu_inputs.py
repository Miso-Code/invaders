from src.ecs.components.c_input_command import CInputCommand
from src.engine.wrapper import PyGameWrapper

engine = PyGameWrapper().engine


def system_menu_inputs(world, event, do_action):
    for ent, (input_command,) in world.get_components(CInputCommand):
        if event.type == engine.KEYDOWN:
            if event.key == engine.K_SPACE:
                do_action(input_command)
                return
