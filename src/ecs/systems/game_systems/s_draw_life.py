from src.ecs.components.tags.c_tag_life_icon import CTagLifeIcon


def system_remove_life_icon(world, life):
    components = list(reversed(world.get_components(CTagLifeIcon)))
    components_to_delete = len(components) - life
    for i in range(components_to_delete):
        entity, _ = components[i]
        world.delete_entity(entity)
