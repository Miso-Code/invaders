import pygame


class PyGameWrapper:
    instance = pygame

    @property
    def engine(self):
        return self.instance

    def init(self):
        self.instance.init()

    def quit(self):
        self.instance.quit()

    def display_set_mode(self, size):
        return self.instance.display.set_mode(size)

    def set_caption(self, caption):
        self.instance.display.set_caption(caption)

    def display_flip(self):
        self.instance.display.flip()

    def clock(self):
        return self.instance.time.Clock()

    def events(self):
        return self.instance.event.get()
