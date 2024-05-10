from src.create.prefab_creator_interface import create_text
from src.create.prefab_creator_interface import TextAlignment
from src.create.prefabs import create_main_menu_inputs
from src.create.prefabs import create_sprite
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.systems.menu_systems.s_accelerate_menu_position import system_accelerate_menu_position
from src.ecs.systems.menu_systems.s_main_menu_movement import system_main_menu_movement
from src.ecs.systems.menu_systems.s_menu_inputs import system_menu_inputs
from src.engine.scenes.base import Scene
from src.engine.services.service_locator import ServiceLocator
from src.engine.wrapper import PyGameWrapper

text_service = ServiceLocator.text_service

engine = PyGameWrapper().engine


class MenuScene(Scene):
    next_scene = "game"
    TOP_LIMIT = 20

    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.top_position = self._game_engine.screen.get_height() + self.TOP_LIMIT
        self._interface_cfg = game_engine.interface_cfg
        self._init_texts()
        self._ready_to_start = False

    def _init_texts(self):
        first_text = "1UP"
        second_text = "HI-SCORE"
        third_text = "00"
        fourth_text = str(self._game_engine.interface_cfg.high_score_max_value)

        fifth_text = "Press SPACE to start the game"

        title_text_color = self._game_engine.interface_cfg.title_text_color
        normal_text_color = self._game_engine.interface_cfg.normal_text_color
        high_score_text_color = self._game_engine.interface_cfg.high_score_color

        title_color = self._game_engine.engine.Color(title_text_color.r, title_text_color.g, title_text_color.b)

        normal_color = self._game_engine.engine.Color(normal_text_color.r, normal_text_color.g, normal_text_color.b)

        high_score_color = self._game_engine.engine.Color(high_score_text_color.r, high_score_text_color.g, high_score_text_color.b)

        positions = [
            self._game_engine.engine.Vector2(50, self.top_position),
            self._game_engine.engine.Vector2(130, self.top_position),
            self._game_engine.engine.Vector2(70, self.top_position + 10),
            self._game_engine.engine.Vector2(155, self.top_position + 10),
            self._game_engine.engine.Vector2(200, self.top_position + 180),
        ]
        align_center = TextAlignment.CENTER
        self._menu_texts = [
            (first_text, self._interface_cfg.title_font_size, title_color, positions[0], self._interface_cfg),
            (second_text, self._interface_cfg.title_font_size, title_color, positions[1], self._interface_cfg),
            (third_text, self._interface_cfg.high_score_font_size, normal_color, positions[2], self._interface_cfg),
            (fourth_text, self._interface_cfg.high_score_font_size, high_score_color, positions[3], self._interface_cfg),
            (fifth_text, self._interface_cfg.normal_font_size, title_color, positions[4], self._interface_cfg, align_center, CBlink(1)),
        ]

    def do_create(self):
        super().do_create()
        create_main_menu_inputs(self.ecs_world)
        for text in self._menu_texts:
            create_text(self.ecs_world, *text, metadata=CMetadata({"scene": "main_menu", "offset": text[3].y - self.top_position}))

        self._create_bg_img()

    def _create_bg_img(self):
        logo_surface = self._game_engine.image_service.get(self._game_engine.window_cfg.invaders_img)
        logo_position = engine.Vector2(self._game_engine.screen.get_width() / 2 - logo_surface.get_width() / 2, self.top_position + 80)
        logo_speed = CSpeed(engine.Vector2(0, 0))
        create_sprite(self.ecs_world, logo_surface, logo_position, speed=logo_speed, metadata=CMetadata({"scene": "main_menu", "offset": 80}))

    def do_update(self, delta_time: float):
        self._ready_to_start = system_main_menu_movement(self.ecs_world, delta_time, self.TOP_LIMIT)

    def do_process_events(self, event):
        system_menu_inputs(self.ecs_world, event, self._do_action)

    def _do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            if not self._ready_to_start:
                system_accelerate_menu_position(self.ecs_world, self.TOP_LIMIT)
                self._ready_to_start = True
            else:
                self.switch_scene(self.next_scene)
