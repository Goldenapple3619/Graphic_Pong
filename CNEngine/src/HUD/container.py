from .empty_hud import EmptyHud
from ..libs import transform

class Container(EmptyHud):
    def __init__(self, x, y, sprite=None):
        super().__init__(x,y)

        self.sprite = sprite

        if sprite is not None:
            self.size_x = sprite.get_width()
            self.size_y = sprite.get_height()

            self.draw_size_x = self.size_x
            self.draw_size_y = self.size_y

        self.contained = []

    def move(self, x, y):
        for hud in self.contained:
            hud.move(x + hud.draw_x - self.draw_x, y + hud.draw_y - self.draw_y)
        super().move(x, y)

    def add_hud(self, hud):
        hud.move(hud.draw_x + self.draw_x, hud.draw_y + self.draw_y)

        self.contained.append(hud)

    def event(self, event):
        for item in self.contained:
            item.event(event)

    def update(self, parent):
        for item in self.contained:
            item.update(parent)

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

        for item in self.contained:
            item.draw(screen)