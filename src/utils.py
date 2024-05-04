import json

import pygame

FILE_PATH_MAP = {
    "window_cfg": "./assets/cfg/window.json",
    "level_cfg": "./assets/cfg/level_01.json",
    "enemies_cfg": "./assets/cfg/enemies.json",
    "player_cfg": "./assets/cfg/player.json",
    "bullet_cfg": "./assets/cfg/bullet.json",
    "explosion_cfg": "./assets/cfg/explosion.json",
    "interface_cfg": "./assets/cfg/interface.json",
    "star_field_cfg": "./assets/cfg/starfield.json",
}


class JSONObject(object):
    def __init__(self, d):
        self.__dict__ = d
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                self.__dict__[key] = JSONObject(value)
            elif isinstance(value, list):
                self.__dict__[key] = [JSONObject(item) for item in value]


def read_json(config_name):
    file_path = FILE_PATH_MAP[config_name]
    with open(file_path, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            return [JSONObject(item) for item in data]
        return JSONObject(data)


def get_relative_area(area: pygame.Rect, pos_topleft: pygame.Vector2):
    new_rect = area.copy()
    new_rect.topleft = pos_topleft
    return new_rect
