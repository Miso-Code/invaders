from src.engine.wrapper import PyGameWrapper
from src.utils import rotate_sprite

engine = PyGameWrapper().engine


class CSurface:
    def __init__(self, size, color) -> None:
        self.angle = 0
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

    def rotate(self, pivot_image, angle_increment):
        self.angle += angle_increment
        self.surface = engine.transform.rotate(pivot_image, self.angle)
        self.area = self.surface.get_rect()

    def rotate_sprite_surface(self, sprite_image, angle):
        self.surface = rotate_sprite(sprite_image, angle)
        self.angle = angle
