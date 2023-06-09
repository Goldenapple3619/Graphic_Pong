from .empty_hud import *
from ..libs import *

class ImageHud(EmptyHud):
    def __init__(self, x, y, sprite=None):
        super().__init__(x,y)

        self.sprite = sprite

        if sprite is not None:
            self.size_x = sprite.get_width()
            self.size_y = sprite.get_height()

            self.draw_size_x = self.size_x
            self.draw_size_y = self.size_y



    def draw(self, screen: object):
        if self.sprite is not None:
            screen.blit(
                transform.scale(
                    self.sprite,
                    (
                        self.draw_size_x,
                        self.draw_size_y
                    )
                ),
                (
                    self.draw_x,self.draw_y
                )
            )