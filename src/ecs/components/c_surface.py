from src.engine.wrapper import PyGameWrapper

engine = PyGameWrapper().engine


class CSurface:
    def __init__(self, size, color) -> None:
        self.surface = engine.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()

    @classmethod
    def from_surface(cls, surface: engine.Surface) -> "CSurface":
        instance = cls(engine.Vector2(0, 0), engine.Color(0, 0, 0))
        instance.surface = surface
        instance.area = instance.surface.get_rect()
        return instance

    @classmethod
    def from_text(cls, text: str, font, color):
        text_surface = font.render(text, True, color)
        return cls.from_surface(text_surface)
