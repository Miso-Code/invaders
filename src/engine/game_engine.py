import esper
from src.create.prefabs import create_stars
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_star_blink import system_star_blink
from src.ecs.systems.s_stars_movement import system_stars_movement
from src.engine.wrapper import PyGameWrapper
from src.utils import FILE_PATH_MAP
from src.utils import read_json


class GameEngine:
    config_map = FILE_PATH_MAP

    def __init__(self) -> None:
        self.is_running = False
        self.wrapper = PyGameWrapper()
        self.clock = self.wrapper.engine.time.Clock()
        self.init_game()
        self.ecs_world = esper.World()
        self.delta_time = 0

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def init_game(self):
        self.wrapper.init()
        self._init_config()
        self._init_window()

    def _init_window(self):
        self.wrapper.set_caption(self.window_cfg.title)
        window_size = (self.window_cfg.size.w, self.window_cfg.size.h)
        self.screen = self.wrapper.display_set_mode(window_size)
        self.fps = self.window_cfg.framerate

    def _init_config(self):
        for key in self.config_map.keys():
            config = self.read_config(key)
            if config is not None:
                setattr(self, key, self.read_config(key))

    @staticmethod
    def read_config(config_name):
        try:
            return read_json(config_name)
        except FileNotFoundError:
            print(f"File {config_name} not found")
            return None

    def _create(self):
        create_stars(self.ecs_world, self.star_field_cfg, self.screen)

    def _calculate_time(self):
        self.clock.tick(self.fps)
        self.delta_time = self.clock.get_time() / 1000

    def _process_events(self):
        for event in self.wrapper.events():
            if event.type == self.wrapper.engine.QUIT:
                self.is_running = False

    def _update(self):
        system_stars_movement(self.ecs_world, self.screen, self.delta_time)
        system_star_blink(self.ecs_world, self.delta_time)

    def _draw(self):
        self.screen.fill((self.window_cfg.bg_color.r, self.window_cfg.bg_color.g, self.window_cfg.bg_color.b))
        system_rendering(self.ecs_world, self.screen)
        self.wrapper.display_flip()

    def _clean(self):
        self.ecs_world.clear_database()
        self.wrapper.quit()
