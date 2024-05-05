import pygame


class TextService:
    def __init__(self):
        pygame.font.init()
        self._font = pygame.font.SysFont("Arial", 24)
        self._color = pygame.Color("white")

    def write(self, surface, text, position):
        text_surface = self.font.render(text, True, self.color)
        surface.blit(text_surface, position)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font_config):
        font = pygame.font.Font(font_config.font, font_config.size)
        self._font = font

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        color = pygame.Color(color)
        self._color = color
