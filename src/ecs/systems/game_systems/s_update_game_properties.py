from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_text import CTagText


def system_update_game_properties(world, field, text, font, color):
    components = world.get_components(CSurface, CTagText, CMetadata)

    for entity, (c_surface, _, c_metadata) in components:
        if getattr(c_metadata, "is_editable", False) and c_metadata.field == field:
            c_surface.surface = CSurface.from_text(text, font, color).surface
            break
