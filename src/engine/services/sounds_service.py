import pygame


class SoundsService:
    def __init__(self):
        self._sounds = {}
        self.music = pygame.mixer.music

    def play(self, path):
        if path is None:
            return
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
        if not self.is_playing(path):
            self._sounds[path].play()

    def play_music(self, path):
        if path not in self._sounds:
            self.music.load(path)
            self.music.play(-1)
            self.music.set_volume(0.8)

    def is_music_playing(self):
        return self.music.get_busy()

    def pause_music(self):
        self.music.pause()

    def stop(self, path):
        if path in self._sounds:
            self._sounds[path].stop()

    def is_playing(self, path):
        if path in self._sounds:
            return self._sounds[path].get_num_channels() > 0
        return False
