from src.create.prefabs import create_enemies
from src.create.prefabs import create_inputs
from src.create.prefabs import create_player
from src.create.prefabs import create_player_bullet
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.s_input_player import system_input_player
from src.engine.scenes.base import Scene


class GameScene(Scene):
    def _do_create(self):
        self._all_enemies = create_enemies(self.ecs_world, self._game_engine.level_cfg, self._game_engine.enemies_cfg, self._game_engine.screen)
        player_entity = create_player(self.ecs_world, self._game_engine.player_cfg, self._game_engine.screen)
        self._player_surface = self.ecs_world.component_for_entity(player_entity, CSurface)
        self._player_transform = self.ecs_world.component_for_entity(player_entity, CTransform)
        self._player_speed = self.ecs_world.component_for_entity(player_entity, CSpeed)
        create_inputs(self.ecs_world)

    def do_process_events(self, event):
        system_input_player(self.ecs_world, event, self._do_action)

    def _do_action(self, command):
        player_speed = self._game_engine.player_cfg.speed
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
                    create_player_bullet(self.ecs_world, self._game_engine.player_cfg, self._player_transform, self._player_surface)
                    self._game_engine.sound_service.play(self._game_engine.player_cfg.bullet.sound)
            elif command.phase == CommandPhase.END:
                pass
