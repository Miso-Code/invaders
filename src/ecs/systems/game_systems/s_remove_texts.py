from src.ecs.components.c_metadata import CMetadata
from src.ecs.components.tags.c_tag_text import CTagText


def system_remove_texts(world):
    components = world.get_components(CTagText, CMetadata)
    for entity, (c_tag, c_metadata) in components:
        if getattr(c_metadata, "is_removable", False):
            world.delete_entity(entity)
