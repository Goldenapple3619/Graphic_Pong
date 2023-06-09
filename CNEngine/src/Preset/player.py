from ..Objects.tile import Tile
from ..libs import get_pressed

class Player(Tile):
    def __init__(self: object, x: int, y: int, sprite: object, grid_size: int=16, pixel_size: int=3, z: int=0, force:int = 5): 
        super().__init__(x, y , sprite, grid_size, pixel_size, z)
        self.draw_x = x
        self.draw_y = y


        self.force = force

        self.actions = []

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def player_set_action(self, condition, action):
        self.actions.append((condition, action))

    def update(self, parent):
        k = get_pressed()

        for action in self.actions:
            if action[0](self, k): action[1](self)

        super().update(parent)