from src.constants import TIMER


class LevelService:
    def __init__(self):
        self._level = 1
        self._enemy_spawning = False
        self._level_timer = TIMER - 0.5
        self._level_is_started = False

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def enemy_spawning(self):
        return self._enemy_spawning

    @enemy_spawning.setter
    def enemy_spawning(self, value):
        self._enemy_spawning = value

    @property
    def level_timer(self):
        return self._level_timer

    @level_timer.setter
    def level_timer(self, value):
        self._level_timer = value

    @property
    def level_is_started(self):
        return self._level_is_started

    @level_is_started.setter
    def level_is_started(self, value):
        self._level_is_started = value
