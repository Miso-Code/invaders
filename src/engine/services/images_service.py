import pygame

from src.engine.wrapper import PyGameWrapper

engine = PyGameWrapper().engine


class ImagesService:
    def __init__(self):
        self._images = {}

    def get(self, path):
        if path not in self._images:
            self._images[path] = engine.image.load(path).convert_alpha()
        return self._images[path]
