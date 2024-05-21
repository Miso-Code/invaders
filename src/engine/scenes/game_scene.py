from src.constants import BLINK
from src.constants import PlayerMovement
from src.constants import TIMER
from src.create.prefab_creator_interface import create_life_icon
from src.create.prefab_creator_interface import create_text
from src.create.prefab_creator_interface import TextAlignment
from src.create.prefabs import create_enemies
from src.create.prefabs import create_inputs
from src.create.prefabs import create_player
from src.create.prefabs import create_player_bullet
from src.create.prefabs import create_sprite
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_bullet import CTagPlayerBullet
from src.ecs.systems.game_systems.s_bullet_movement import system_enemy_bullet_movement
from src.ecs.systems.game_systems.s_bullet_movement import system_player_bullet_movement
from src.ecs.systems.game_systems.s_draw_life import system_remove_life_icon
from src.ecs.systems.game_systems.s_enemies_movement import system_enemies_movement
from src.ecs.systems.game_systems.s_enemy_bullet_player_collision import system_enemy_bullet_player_collision
from src.ecs.systems.game_systems.s_enemy_chase import system_enemy_chase
from src.ecs.systems.game_systems.s_enemy_collision import system_enemy_collision
from src.ecs.systems.game_systems.s_enemy_collision import system_enemy_collision_with_enemy
from src.ecs.systems.game_systems.s_enemy_shoot import system_enemy_shoot
from src.ecs.systems.game_systems.s_enemy_state import system_enemy_state
from src.ecs.systems.game_systems.s_explosions_removal import system_explosion_removal
from src.ecs.systems.game_systems.s_input_player import system_input_player
from src.ecs.systems.game_systems.s_player_bullet_enemy_collision import system_player_bullet_enemy_collision
from src.ecs.systems.game_systems.s_remove_texts import system_remove_texts
from src.ecs.systems.game_systems.s_spawn import system_spawn
from src.ecs.systems.game_systems.s_update_game_properties import system_update_game_properties
from src.ecs.systems.game_systems.utils import check_chasers_in_level
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_movement import system_movement_player
from src.engine.scenes.base import Scene


class GameScene(Scene):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self._player_entity = None
        self.next_scene = "main_menu"
        self._player_metadata = None
        self._player_transform = None
        self._player_surface = None
        self._all_enemies = None
        self._high_score = self._game_engine.interface_cfg.high_score_max_value
        self._score = 0
        self._lives = self._game_engine.player_cfg.life
        self._level = 1
        self._is_level_up = False
        self._is_game_over = False
        self._game_over_timer = TIMER * 3
        self._level_up_sound_played = False
        self._level_up_timer = TIMER
        self._game_over_sound_played = False
        self._is_paused = False
        self._pause_text = None
        self._bullet_entity = None
        self._compensate = False
        self._is_paused_sound_played = False
        self._init_font_config()

    def do_create(self):
        super().do_create()
        self._reset_game_properties()
        create_inputs(self.ecs_world)
        self._all_enemies = create_enemies(self.ecs_world, self._game_engine.level_cfg, self._game_engine.enemies_cfg, self._game_engine.screen)
        self._player_entity = create_player(self.ecs_world, self._game_engine.player_cfg, self._game_engine.screen)
        self._player_surface = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        self._player_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_metadata = self.ecs_world.component_for_entity(self._player_entity, CMetadata)
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
        sixth_text = "GAME START"

        screen_width = self._game_engine.screen.get_width()
        screen_height = self._game_engine.screen.get_height()

        positions = [
            self._game_engine.engine.Vector2(screen_width // 6, self.top_position),
            self._game_engine.engine.Vector2(2 * screen_width // 6, self.top_position),
            self._game_engine.engine.Vector2(3 * screen_width // 14, self.top_position + 10),
            self._game_engine.engine.Vector2(5 * screen_width // 12, self.top_position + 10),
            self._game_engine.engine.Vector2(3 * screen_width // 4, self.top_position + 10),
            self._game_engine.engine.Vector2(screen_width // 2, screen_height // 2),
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
            (sixth_text, self._title_font_size, self._normal_color, positions[5], self._game_engine.interface_cfg, CMetadata({"type": "text", "is_removable": True})),
        ]
        for text in menu_texts[:-1]:
            metadata = text[-1]
            create_text(self.ecs_world, *text[:-1], metadata=metadata)

        create_text(self.ecs_world, *menu_texts[-1][:-1], metadata=menu_texts[-1][-1], alignment=TextAlignment.CENTER)

    def do_update(self, delta_time: float):
        self._start_level()
        if not self._is_paused:
            system_remove_texts(self.ecs_world)
            if not self._player_metadata.is_respawning and not self._is_game_over:
                system_movement_player(self.ecs_world, self._game_engine.delta_time, self._game_engine.screen, self._game_engine.player_cfg)
                self._score += system_player_bullet_enemy_collision(self.ecs_world, self._game_engine.enemies_cfg.explosion)
                system_enemy_collision(self.ecs_world, self._game_engine.player_cfg.explosion)
                system_player_bullet_movement(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time, (self._player_transform, self._player_surface))
                system_enemy_shoot(self.ecs_world, self._game_engine.delta_time)
            system_enemy_bullet_movement(self.ecs_world, self._game_engine.screen, self._game_engine.delta_time)
            system_enemy_chase(
                self.ecs_world,
                self._game_engine.delta_time,
                self._player_entity,
                self._game_engine.screen,
                self._game_engine.enemies_cfg,
                not self._player_metadata.is_respawning,
            )
            system_enemy_collision_with_enemy(self.ecs_world)
            system_enemy_bullet_player_collision(self.ecs_world, self._game_engine.player_cfg.explosion)
            system_enemy_state(self.ecs_world, self._game_engine.enemies_cfg)
            system_enemies_movement(self.ecs_world, self._game_engine.delta_time, self._game_engine.screen)
            system_animation(self.ecs_world, self._game_engine.delta_time)
            system_explosion_removal(self.ecs_world)
            system_spawn(self.ecs_world, self._game_engine.delta_time, self._game_engine.screen, self._game_engine.player_cfg)
            system_remove_life_icon(self.ecs_world, self._lives)
            self._create_player_bullet()

            self._update_player_scene_properties()
            self._level_up()
        self._pause_game()
        self._game_over()

    def _update_player_scene_properties(self):
        player = self.ecs_world.get_components(CTagPlayer)
        if player:
            player_metadata = self.ecs_world.component_for_entity(player[0][0], CMetadata)
            self._lives = player_metadata.lives
            self._game_engine.score_service.score = self._score
            self._game_engine.score_service.high_score = self._high_score
            if self._score > self._high_score:
                self._high_score = self._score
            if self._lives == 0:
                self._is_game_over = True
            enemies = self.ecs_world.get_components(CTagEnemy)
            if not enemies:
                self._is_level_up = True

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
        system_input_player(self.ecs_world, event, self._do_action)

    def _do_action(self, command):
        if not self._player_metadata.is_respawning and not self._is_game_over and not self._is_paused:
            if self._compensate:
                self._player_metadata.player_state = PlayerMovement.STOP
                self._compensate = False
            if command.name == "PLAYER_RIGHT":
                if command.phase == CommandPhase.START:
                    self._player_metadata.player_state = PlayerMovement.RIGHT if self._player_metadata.player_state != PlayerMovement.LEFT else PlayerMovement.STOP
                elif command.phase == CommandPhase.END:
                    self._player_metadata.player_state = PlayerMovement.LEFT if self._player_metadata.player_state == PlayerMovement.STOP else PlayerMovement.STOP
            elif command.name == "PLAYER_LEFT":
                if command.phase == CommandPhase.START:
                    self._player_metadata.player_state = PlayerMovement.LEFT if self._player_metadata.player_state != PlayerMovement.RIGHT else PlayerMovement.STOP
                elif command.phase == CommandPhase.END:
                    self._player_metadata.player_state = PlayerMovement.RIGHT if self._player_metadata.player_state == PlayerMovement.STOP else PlayerMovement.STOP
            if command.name == "PLAYER_FIRE":
                if command.phase == CommandPhase.START:
                    if self._bullet_entity is not None:
                        try:
                            bullet_metadata = self.ecs_world.component_for_entity(self._bullet_entity, CMetadata)
                            if not bullet_metadata.is_fired:
                                self._game_engine.sound_service.play(self._game_engine.player_cfg.bullet.sound)
                            bullet_metadata.is_fired = True
                        except:
                            pass
                elif command.phase == CommandPhase.END:
                    pass
        elif self._player_metadata.is_respawning or self._player_metadata.is_killed:
            self._compensate = True

        if command.name == "PAUSE":
            if command.phase == CommandPhase.START:
                self._is_paused = not self._is_paused
            elif command.phase == CommandPhase.END:
                pass

    def _start_level(self):
        if not self._game_engine.level_service.level_is_started:
            self._game_engine.level_service.level_timer -= self._game_engine.delta_time
            if self._game_engine.level_service.level_timer <= 0:
                self._game_engine.level_service.level_is_started = True
                self._game_engine.level_service.level_timer = TIMER
                self._game_engine.level_service.enemy_spawning = True

    def _pause_game(self):
        if self._is_paused and not self._pause_text:
            self._game_engine.sound_service.play(self._game_engine.level_cfg.pause_sound)
            self._pause_text = create_text(
                self.ecs_world,
                "PAUSED",
                self._title_font_size,
                self._title_color,
                self._game_engine.engine.Vector2(self._game_engine.screen.get_width() // 2, self._game_engine.screen.get_height() // 2),
                self._game_engine.interface_cfg,
                alignment=TextAlignment.CENTER,
                metadata=CMetadata({"type": "text", "is_removable": True}),
                blink=CBlink(BLINK),
            )
            self._is_paused_sound_played = True
        elif not self._is_paused:
            self._pause_text = None
            self._is_paused_sound_played = False

    def _game_over(self):
        if self._is_game_over:
            if not self._game_over_sound_played:
                self._game_engine.sound_service.play(self._game_engine.level_cfg.game_over_sound)
                self._game_over_sound_played = True
            self._game_over_timer -= self._game_engine.delta_time
            if self._game_over_timer <= 0:
                self.switch_scene(self.next_scene)
            else:
                create_text(
                    self.ecs_world,
                    "GAME OVER",
                    self._title_font_size,
                    self._normal_color,
                    self._game_engine.engine.Vector2(self._game_engine.screen.get_width() // 2, self._game_engine.screen.get_height() // 2),
                    self._game_engine.interface_cfg,
                    alignment=TextAlignment.CENTER,
                    metadata=CMetadata({"type": "text", "is_removable": True}),
                )

    def _level_up(self):
        if self._is_level_up and not self._is_game_over:
            self._level_up_timer -= self._game_engine.delta_time

            create_text(
                self.ecs_world,
                "LEVEL COMPLETED!",
                self._title_font_size,
                self._normal_color,
                self._game_engine.engine.Vector2(self._game_engine.screen.get_width() // 2, self._game_engine.screen.get_height() // 2 - 30),
                self._game_engine.interface_cfg,
                alignment=TextAlignment.CENTER,
                metadata=CMetadata({"type": "text", "is_removable": True}),
            )

            create_text(
                self.ecs_world,
                "Get ready for the next level!",
                self._title_font_size,
                self._title_color,
                self._game_engine.engine.Vector2(self._game_engine.screen.get_width() // 2, self._game_engine.screen.get_height() // 2),
                self._game_engine.interface_cfg,
                alignment=TextAlignment.CENTER,
                metadata=CMetadata({"type": "text", "is_removable": True}),
            )
            if not self._level_up_sound_played:
                self._game_engine.sound_service.play(self._game_engine.level_cfg.sound)
                self._level_up_sound_played = True
            if self._level_up_timer <= 0:
                system_remove_texts(self.ecs_world)
                self._level_up_timer = TIMER
                self._level += 1
                self._game_engine.level_service.level = self._level
                self._game_engine.level_service.enemy_spawning = True
                self._is_level_up = False
                self._level_up_sound_played = False
                self._compensate = False

                self._all_enemies = create_enemies(self.ecs_world, self._game_engine.level_cfg, self._game_engine.enemies_cfg, self._game_engine.screen)

    def _create_player_bullet(self):
        # check if there is not a bullet already on the screen
        bullets = self.ecs_world.get_components(CSurface, CTagPlayerBullet)
        player = self.ecs_world.get_components(CTagPlayer)
        if not bullets and player and not self._player_metadata.is_respawning and not self._is_game_over:
            self._bullet_entity = create_player_bullet(self.ecs_world, self._game_engine.player_cfg, self._player_transform, self._player_surface)

    def _reset_game_properties(self):
        try:
            if not self._is_level_up:
                self._is_game_over = False
                self._game_over_timer = TIMER * 3
                self._game_over_sound_played = False
                self._score = 0
                self._lives = self._game_engine.player_cfg.life
                self._level = 1
                self._is_level_up = False
                self._level_up_timer = TIMER
                self._level_up_sound_played = False
                self._game_engine.score_service.score = self._score
                self._game_engine.level_service.level_timer = TIMER - 0.5
                self._game_engine.level_service.level_is_started = False
                self._game_engine.level_service.enemy_spawning = False
                self._player_metadata.lives = self._lives
                self._player_metadata.is_respawning = False
                self._pause_text = None
                self._is_paused_sound_played = False
                self._compensate = False
                self._bullet_entity = None
        except:
            pass
