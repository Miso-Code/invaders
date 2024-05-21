import asyncio

from src.engine.scenes.game_scene import GameScene
from src.engine.scenes.menu_scene import MenuScene
from src.engine.services.service_locator import ServiceLocator
from src.engine.wrapper import PyGameWrapper
from src.utils import FILE_PATH_MAP
from src.utils import read_json


class GameEngine:
    config_map = FILE_PATH_MAP
    sound_service = ServiceLocator.sounds_service
    image_service = ServiceLocator.images_service
    text_service = ServiceLocator.text_service
    score_service = ServiceLocator.score_service
    level_service = ServiceLocator.level_service

    def __init__(self) -> None:
        self._current_scene = None
        self._scene_name_to_switch = None
        self.wrapper = PyGameWrapper()
        self.wrapper.init()
        self.is_running = False
        self.clock = self.wrapper.engine.time.Clock()
        self.delta_time = 0
        self.init_game()

    async def run(self, start_scene) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._do_clean()

    @property
    def engine(self):
        return self.wrapper.engine

    def init_game(self):
        self._init_config()
        self._init_window()
        self._init_music()
        self._config_scenes()

    def _config_scenes(self):
        self._scenes = {
            "main_menu": MenuScene(self),
            "game": GameScene(self),
        }
        self._current_scene = None
        self._scene_name_to_switch = None

    def _init_window(self):
        self.wrapper.set_caption(self.window_cfg.title)
        window_size = (self.window_cfg.size.w, self.window_cfg.size.h)
        self.screen = self.wrapper.display_set_mode(window_size, 0)
        self.fps = self.window_cfg.framerate

    def _init_music(self):
        self.sound_service.play_music(self.music_cfg.loop)

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
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self.fps)
        self.delta_time = self.clock.get_time() / 1000

    def _process_events(self):
        for event in self.wrapper.events():
            self._current_scene.do_process_events(event)
            if event.type == self.wrapper.engine.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self.delta_time)

    def _draw(self):
        self.screen.fill((self.window_cfg.bg_color.r, self.window_cfg.bg_color.g, self.window_cfg.bg_color.b))
        self._current_scene.do_draw(self.screen)
        self.wrapper.display_flip()

    def _do_clean(self):
        if self._current_scene:
            self._current_scene.clean()
        self.wrapper.quit()

    def _do_action(self, command):
        self._current_scene.do_action(command)

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def switch_scene(self, new_scene_name: str):
        self._scene_name_to_switch = new_scene_name
