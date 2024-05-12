from src.create.prefab_creator_interface import create_life_icon
from src.create.prefab_creator_interface import create_text
from src.create.prefabs import create_enemies
from src.create.prefabs import create_inputs
from src.create.prefabs import create_player
from src.create.prefabs import create_player_bullet
from src.create.prefabs import create_sprite
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.game_systems.s_bullet_movement import system_enemy_bullet_movement
from src.ecs.systems.game_systems.s_bullet_movement import system_player_bullet_movement
from src.ecs.systems.game_systems.s_draw_life import system_remove_life_icon
from src.ecs.systems.game_systems.s_enemies_movement import system_enemies_movement
from src.ecs.systems.game_systems.s_enemy_bullet_player_collision import system_enemy_bullet_player_collision
from src.ecs.systems.game_systems.s_enemy_shoot import system_enemy_shoot
from src.ecs.systems.game_systems.s_explosions_removal import system_explosion_removal
from src.ecs.systems.game_systems.s_input_player import system_input_player
from src.ecs.systems.game_systems.s_player_bullet_enemy_collision import system_player_bullet_enemy_collision
from src.ecs.systems.game_systems.s_player_respawn import system_player_respawn
from src.ecs.systems.game_systems.s_update_game_properties import system_update_game_properties
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_movement import system_movement_player
from src.engine.scenes.base import Scene


class GameScene(Scene):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.next_scene = "game_over"
        self._player_metadata = None
        self._player_speed = None
        self._player_transform = None
        self._player_surface = None
        self._all_enemies = None
        self._high_score = self._game_engine.interface_cfg.high_score_max_value
        self._score = 0
        self._lives = self._game_engine.player_cfg.life
        self._level = 1
        self._init_font_config()

    def do_create(self):
        super().do_create()
        create_inputs(self.ecs_world)
        self._all_enemies = create_enemies(self.ecs_world, self._game_engine.level_cfg, self._game_engine.enemies_cfg, self._game_engine.screen)
        player_entity = create_player(self.ecs_world, self._game_engine.player_cfg, self._game_engine.screen)
        self._player_surface = self.ecs_world.component_for_entity(player_entity, CSurface)
        self._player_transform = self.ecs_world.component_for_entity(player_entity, CTransform)
        self._player_speed = self.ecs_world.component_for_entity(player_entity, CSpeed)
        self._player_metadata = self.ecs_world.component_for_entity(player_entity, CMetadata)
        self._game_engine.sound_service.play(self._game_engine.level_cfg.sound)
        self._render_texts()
        self._render_life_icon()
        self._render_level_icon()

    def _render_life_icon(self):
        screen_width = self._game_engine.screen.get_width()
        create_life_icon(self.ecs_world, (2 * screen_width // 3, self.top_position), self._game_engine.player_cfg)

    def _render_level_icon(self):
        screen_width = self._game_engine.screen.get_width()
        icon_surface = self._game_engine.image_service.get(self._game_engine.level_cfg.icon)
        icon_width = icon_surface.get_width()
        icon_position = self._game_engine.engine.Vector2(3 * screen_width // 4 - icon_width, self.top_position + 5)
        icon_speed = CSpeed(self._game_engine.engine.Vector2(0, 0))
        create_sprite(self.ecs_world, icon_surface, icon_position, speed=icon_speed, metadata=CMetadata({"type": "icon"}))

    def _init_font_config(self):
        title_text_color = self._game_engine.interface_cfg.title_text_color
        normal_text_color = self._game_engine.interface_cfg.normal_text_color
        high_score_text_color = self._game_engine.interface_cfg.high_score_color

        self._title_color = self._game_engine.engine.Color(title_text_color.r, title_text_color.g, title_text_color.b)

        self._normal_color = self._game_engine.engine.Color(normal_text_color.r, normal_text_color.g, normal_text_color.b)

        self._high_score_color = self._game_engine.engine.Color(high_score_text_color.r, high_score_text_color.g, high_score_text_color.b)

        self._title_font_size = self._game_engine.interface_cfg.title_font_size
        self._high_score_font_size = self._game_engine.interface_cfg.high_score_font_size

    def _render_texts(self):
        first_text = "1UP"
        second_text = "HI-SCORE"
        third_text = f"{self._score:06}"
        fourth_text = f"{self._high_score}"
        fifth_text = f"{self._level:02}"
        screen_width = self._game_engine.screen.get_width()

        positions = [
            self._game_engine.engine.Vector2(screen_width // 6, self.top_position),
            self._game_engine.engine.Vector2(2 * screen_width // 6, self.top_position),
            self._game_engine.engine.Vector2(3 * screen_width // 14, self.top_position + 10),
            self._game_engine.engine.Vector2(5 * screen_width // 12, self.top_position + 10),
            self._game_engine.engine.Vector2(3 * screen_width // 4, self.top_position + 10),
        ]
        menu_texts = [
            (first_text, self._title_font_size, self._title_color, positions[0], self._game_engine.interface_cfg, CMetadata({"type": "text"})),
            (second_text, self._title_font_size, self._title_color, positions[1], self._game_engine.interface_cfg, CMetadata({"type": "text"})),
            (
                third_text,
                self._high_score_font_size,
                self._normal_color,
                positions[2],
                self._game_engine.interface_cfg,
                CMetadata({"type": "text", "is_editable": True, "field": "score"}),
            ),
            (
                fourth_text,
                self._high_score_font_size,
                self._high_score_color,
                positions[3],
                self._game_engine.interface_cfg,
                CMetadata({"type": "text", "is_editable": True, "field": "high_score"}),
            ),
            (
                fifth_text,
                self._high_score_font_size,
                self._normal_color,
                positions[4],
                self._game_engine.interface_cfg,
                CMetadata({"type": "text", "is_editable": True, "field": "lives"}),
            ),
        ]
        for text in menu_texts:
            metadata = text[-1]
            create_text(self.ecs_world, *text[:-1], metadata=metadata)

    def do_update(self, delta_time: float):
        if not self._player_metadata.is_respawning:
            system_movement_player(self.ecs_world, self._game_engine.delta_time, self._game_engine.screen)
            self._score += system_player_bullet_enemy_collision(self.ecs_world, self._game_engine.enemies_cfg.explosion)
            system_enemy_shoot(self.ecs_world)
            system_enemy_bullet_player_collision(self.ecs_world, self._game_engine.player_cfg.explosion)
        system_player_bullet_movement(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time)
        system_enemy_bullet_movement(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time)
        system_enemies_movement(self.ecs_world, self._game_engine.delta_time, self._game_engine.screen)
        system_animation(self.ecs_world, self._game_engine.delta_time)
        system_explosion_removal(self.ecs_world)
        system_player_respawn(self.ecs_world, self._game_engine.delta_time, self._game_engine.screen, self._game_engine.player_cfg)
        system_remove_life_icon(self.ecs_world, self._lives)
        self._update_player_scene_properties()

    def _update_player_scene_properties(self):
        player = self.ecs_world.get_components(CTagPlayer)
        if player:
            player_metadata = self.ecs_world.component_for_entity(player[0][0], CMetadata)
            self._lives = player_metadata.lives
            if self._score > self._high_score:
                self._high_score = self._score

            fields = [
                ["score", f"{self._score:02}", self._high_score_font_size, self._normal_color],
                ["high_score", f"{self._high_score}", self._high_score_font_size, self._high_score_color],
                ["lives", f"{self._level:02}", self._high_score_font_size, self._normal_color],
            ]
            for field_cfg in fields:
                font = self._game_engine.text_service.get(self._game_engine.interface_cfg.font, field_cfg[2])
                field_cfg[2] = font
                system_update_game_properties(self.ecs_world, *field_cfg)

    def do_process_events(self, event):
        if not self._player_metadata.is_respawning:
            # ToDo: fix bug with player moving without pressing any key
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
