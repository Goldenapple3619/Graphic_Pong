from .empty_shader import EmptyShader

class ShadowZ(EmptyShader):
    def __init__(self: object, start_distance: int = 2) -> None:
        self.start_distance = start_distance

    def apply(self: object, game: object) -> None:
        camera_distance = game.camera.z
        start_distance = self.start_distance

        for item in game.objects:
            if not hasattr(item, 'sprite') or item.sprite is None or (hasattr(item, 'ShadowZ_apply') and item.ShadowZ_apply):
                continue

            distance = camera_distance - item.z

            if distance < start_distance:
                continue

            sprite = item.sprite
            sprite.set_alpha(int(255-((distance-start_distance)*255)/camera_distance))
            item.sprite.set_colorkey((0,0,0))
            item.sprite = sprite

            item.ShadowZ_apply = True