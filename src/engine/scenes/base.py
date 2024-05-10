import pygame

import esper
import src.engine.game_engine
from src.create.prefabs import create_stars
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_star_blink import system_blink
from src.ecs.systems.s_stars_movement import system_stars_movement


class Scene:
    def __init__(self, game_engine):
        self.ecs_world = esper.World()
        self._game_engine: src.engine.game_engine.GameEngine = game_engine
        self.screen_rect = self._game_engine.screen.get_rect()

    def do_process_events(self, event: pygame.event):
        pass

    def simulate(self, delta_time):
        system_stars_movement(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time)
        system_blink(self.ecs_world, delta_time)
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()

    def switch_scene(self, new_scene_name: str):
        self._game_engine.switch_scene(new_scene_name)

    def do_create(self):
        create_stars(self.ecs_world, self._game_engine.star_field_cfg, self._game_engine.screen)

    def do_update(self, delta_time: float):
        pass

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)

    def do_action(self, action: CInputCommand):
        pass

    def do_clean(self):
        pass
