from src.engine.wrapper import PyGameWrapper


class CSurface:
    engine = PyGameWrapper().engine

    def __init__(self, size, color) -> None:
        self.surface = self.engine.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()

    @classmethod
    def from_surface(cls, surface):
        instance = cls(cls.engine.Vector2(0, 0), cls.engine.Color(0, 0, 0))
        instance.surface = surface
        instance.area = instance.surface.get_rect()
        return instance
