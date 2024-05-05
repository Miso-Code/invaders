import esper
from src.create.prefabs import create_enemies
from src.create.prefabs import create_inputs
from src.create.prefabs import create_player
from src.create.prefabs import create_player_bullet
from src.create.prefabs import create_stars
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_movement import system_enemy_bullet_movement
from src.ecs.systems.s_bullet_movement import system_player_bullet_movement
from src.ecs.systems.s_enemies_movement import system_enemies_movement
from src.ecs.systems.s_enemy_bullet_player_collision import system_enemy_bullet_player_collision
from src.ecs.systems.s_enemy_shoot import system_enemy_shoot
from src.ecs.systems.s_explosions_removal import system_explosion_removal
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement_player
from src.ecs.systems.s_player_bullet_enemy_collision import system_player_bullet_enemy_collision
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_star_blink import system_star_blink
from src.ecs.systems.s_stars_movement import system_stars_movement
from src.engine.services.service_locator import ServiceLocator
from src.engine.wrapper import PyGameWrapper
from src.utils import FILE_PATH_MAP
from src.utils import read_json


class GameEngine:
    config_map = FILE_PATH_MAP
    sound_service = ServiceLocator.sounds_service

    def __init__(self) -> None:
        self.is_running = False
        self.wrapper = PyGameWrapper()
        self.clock = self.wrapper.engine.time.Clock()
        self.init_game()
        self.ecs_world = esper.World()
        self.delta_time = 0
        self._respawn_timer = 2
        self._player_is_killed = False

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
        self._init_music()

    def _init_window(self):
        self.wrapper.set_caption(self.window_cfg.title)
        window_size = (self.window_cfg.size.w, self.window_cfg.size.h)
        self.screen = self.wrapper.display_set_mode(window_size, self.wrapper.engine.SCALED)
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
        create_stars(self.ecs_world, self.star_field_cfg, self.screen)
        self._all_enemies = create_enemies(self.ecs_world, self.level_cfg, self.enemies_cfg, self.screen)
        player_entity = create_player(self.ecs_world, self.player_cfg, self.screen)
        self._player_surface = self.ecs_world.component_for_entity(player_entity, CSurface)
        self._player_transform = self.ecs_world.component_for_entity(player_entity, CTransform)
        self._player_speed = self.ecs_world.component_for_entity(player_entity, CSpeed)
        create_inputs(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.fps)
        self.delta_time = self.clock.get_time() / 1000

    def _process_events(self):
        for event in self.wrapper.events():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == self.wrapper.engine.QUIT:
                self.is_running = False

    def _update(self):
        system_animation(self.ecs_world, self.delta_time)
        system_stars_movement(self.ecs_world, self.screen, self.delta_time)
        system_star_blink(self.ecs_world, self.delta_time)
        system_movement_player(self.ecs_world, self.delta_time, self.screen)
        system_enemies_movement(self.ecs_world, self.delta_time, self.screen)
        system_player_bullet_enemy_collision(self.ecs_world, self.enemy_explosion_cfg)
        system_explosion_removal(self.ecs_world)
        system_enemy_bullet_movement(self.ecs_world, self.screen, self.delta_time)
        system_player_bullet_movement(self.ecs_world, self.screen, self.delta_time)
        system_enemy_shoot(self.ecs_world, self.delta_time, self.enemies_cfg)
        player_is_killed = system_enemy_bullet_player_collision(self.ecs_world, self.player_explosion_cfg)
        if player_is_killed:
            self._player_is_killed = player_is_killed
        self._respawn_player()
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill((self.window_cfg.bg_color.r, self.window_cfg.bg_color.g, self.window_cfg.bg_color.b))
        system_rendering(self.ecs_world, self.screen)
        self.wrapper.display_flip()

    def _clean(self):
        self.ecs_world.clear_database()
        self.wrapper.quit()

    def _do_action(self, command):
        player_speed = self.player_cfg.speed
        if command.name == "PLAYER_RIGHT":
            if command.phase == CommandPhase.START:
                self._player_speed.speed.x += player_speed
            elif command.phase == CommandPhase.END:
                self._player_speed.speed.x -= player_speed
        elif command.name == "PLAYER_LEFT":
            if command.phase == CommandPhase.START:
                self._player_speed.speed.x -= player_speed
            elif command.phase == CommandPhase.END:
                self._player_speed.speed.x += player_speed
        elif command.name == "PLAYER_FIRE":
            if command.phase == CommandPhase.START:
                # check if there is not a bullet already on the screen
                bullets = self.ecs_world.get_components(CSurface, CTagPlayerBullet)
                player = self.ecs_world.get_components(CTagPlayer)
                if not bullets and player:
                    create_player_bullet(self.ecs_world, self.player_cfg, self._player_transform, self._player_surface)
                    self.sound_service.play(self.player_cfg.bullet.sound)
            elif command.phase == CommandPhase.END:
                pass

    def _respawn_player(self):
        if self._player_is_killed:
            self._respawn_timer -= self.delta_time
            print(self._respawn_timer)
            if self._respawn_timer <= 0:
                player_entity = create_player(self.ecs_world, self.player_cfg, self.screen)
                self._player_surface = self.ecs_world.component_for_entity(player_entity, CSurface)
                self._player_transform = self.ecs_world.component_for_entity(player_entity, CTransform)
                self._player_speed = self.ecs_world.component_for_entity(player_entity, CSpeed)
                self._respawn_timer = 2
                self._player_is_killed = False
