from . import Tile
from ..libs import *

class CustomTile(Tile):
    def __init__(self: object, x: int, y: int, sprite: object, grid_size: int = 16, pixel_size: int = 3, z: int = 0) -> None:
        super().__init__(x, y, sprite, grid_size, pixel_size, z)

    def update(self: object, parent: object) -> None:
        for item in self.components:
            if type(item).__name__ == 'BoxCollider':
                self.t = item.collid_segments

        super().update(parent)

    def add_component(self, component):
        super().add_component(component)

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        super().draw(screen, cam_x, cam_y)
        for item in self.components:
            if type(item).__name__ == 'BoxCollider':
                draw.rect(screen, (0,0,255), Rect(item.x-cam_x, item.y-cam_y, item.end_x, item.end_y), 2)
                for item2 in self.t:
                    item2_2 = item.collid_segments[item2]
                    item2 = self.t[item2]
                    draw.line(screen, (255,0,0), (item2[0]-cam_x, item2[1]-cam_y), (item2_2[0]-cam_x, item2_2[1]-cam_y))