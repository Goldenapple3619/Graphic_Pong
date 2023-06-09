from .empty_object import EmptyObject
from ..libs import *

class Tile(EmptyObject):
    def __init__(self: object, x: int, y: int, sprite: object, grid_size: int=16, pixel_size: int=3, z: int=0) -> None:

        super().__init__(x,y,z)

        self.draw_x = (x * pixel_size) * grid_size
        self.draw_y = (y * pixel_size) * grid_size

        self.size_x = sprite.get_width()
        self.size_y = sprite.get_height()

        self.draw_size_x = self.size_x * pixel_size
        self.draw_size_y = self.size_y * pixel_size

        self.grid = grid_size

        self.pixel_size = pixel_size

        self.sprite = sprite

    def update(self: object, parent: object) -> None:
        super().update(parent)

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        screen.blit(
            transform.scale(
                self.sprite,
                (
                    self.draw_size_x,
                    self.draw_size_y
                )
            ),
            (
                self.draw_x-cam_x,self.draw_y-cam_y
            )
        )
