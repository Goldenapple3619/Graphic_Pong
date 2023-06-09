from .libs import *
from .constants import *

class AnimateButton(Button):
    def __init__(self: object, x: int, y: int, size_x: int, size_y: int, callback=None) -> None:
        super().__init__(x, y, size_x, size_y, callback)
        self.hovered = False

    def update(self, parent):
        x,y = mouse.get_pos()
    
        if x >= self.draw_x and y >= self.draw_y and x <= self.draw_x + self.size_x and y <= self.draw_y + self.size_y:
            self.hovered = True
        else:
            self.hovered = False
        super().update(parent)

class StartButton(AnimateButton):
    def __init__(self: object, x: int, y: int, size_x: int, size_y: int, callback=None) -> None:
        super().__init__(x, y, size_x, size_y, callback)

    def draw(self, screen):
        draw.rect(GAME.screen, (100,100,100) if self.hovered else (200,200,200), Rect(self.draw_x, self.draw_y, self.size_x, self.size_y))
        super().draw(screen)

class ContainerSprites(Container):
    def __init__(self, x, y, size, prefabs):
        self.size_x, self.size_y = size
        self.draw_size_x, self.draw_size_y = size

        super().__init__(x, y, None)

        self.prefabs = prefabs
        self.prepare()
        self.actual = 0

    def go_up(self):
        if self.actual > 0:
            self.actual -= 1

    def go_down(self):
        if len(self.prefabs) - 1 > self.actual:
            self.actual += 1

    def prepare(self):
        add_hud_to_container(self, AnimateButton(-5, -35, self.size_x + 10, 30, lambda: self.go_up()))
        add_hud_to_container(self, AnimateButton(-5, self.size_y + 5, self.size_x + 10, 30, lambda: self.go_down()))

    def draw(self, screen: object):
        draw.rect(screen, (130, 130, 130), Rect(self.draw_x - 5, self.draw_y - 5, self.size_x + 10, self.size_y + 10))
        color = (200,200,200) if not self.contained[0].hovered else (100,100,100)
        draw.rect(screen, color if self.actual != 0 else (10,10,10), Rect(self.contained[0].draw_x, self.contained[0].draw_y, self.contained[0].size_x, self.contained[0].size_y))
        color = (200,200,200) if not self.contained[1].hovered else (100,100,100)
        draw.rect(screen, color if self.actual != len(self.prefabs) - 1 else (10,10,10), Rect(self.contained[1].draw_x, self.contained[1].draw_y, self.contained[1].size_x, self.contained[1].size_y))
        self.sprite = get_image(self.prefabs[self.actual][2])
        super().draw(screen)

class ContainerInt(Container):
    def __init__(self, x, y, size, max_value):
        self.size_x, self.size_y = size
        self.draw_size_x, self.draw_size_y = size

        super().__init__(x, y, None)

        self.max = max_value

        self.prepare()

        self.actual = 0

    def go_up(self):
        if self.actual > 0:
            self.actual -= 1
            self.contained[2].set_text(str(self.actual))

    def go_down(self):
        if self.max > self.actual:
            self.actual += 1
            self.contained[2].set_text(str(self.actual))

    def prepare(self):
        add_hud_to_container(self, AnimateButton(-5, -35, self.size_x + 10, 30, lambda: self.go_up()))
        add_hud_to_container(self, AnimateButton(-5, self.size_y + 5, self.size_x + 10, 30, lambda: self.go_down()))
        add_hud_to_container(self, Text(5,-5,"0", (0,0,0), font.Font("Tahoma.ttf", 38), False))

    def draw(self, screen: object):
        draw.rect(screen, (130, 130, 130), Rect(self.draw_x - 5, self.draw_y - 5, self.size_x + 10, self.size_y + 10))
        color = (200,200,200) if not self.contained[0].hovered else (100,100,100)
        draw.rect(screen, color if self.actual != 0 else (10,10,10), Rect(self.contained[0].draw_x, self.contained[0].draw_y, self.contained[0].size_x, self.contained[0].size_y))
        color = (200,200,200) if not self.contained[1].hovered else (100,100,100)
        draw.rect(screen, color if self.actual != self.max else (10,10,10), Rect(self.contained[1].draw_x, self.contained[1].draw_y, self.contained[1].size_x, self.contained[1].size_y))
        super().draw(screen)

class ContainerBool(Container):
    def __init__(self, x, y, size):
        self.size_x, self.size_y = size
        self.draw_size_x, self.draw_size_y = size

        super().__init__(x, y, None)

        add_hud_to_container(self, Button(5, 5, self.size_x, self.size_y, lambda: self.change()))

        self.actual = False

    def change(self):
        self.actual = not self.actual

    def draw(self, screen: object):
        draw.rect(screen, (5,170,10) if self.actual else (100,100,100), Rect(self.draw_x, self.draw_y, self.size_x / 2, self.size_y / 2))
        draw.rect(screen, (170,5,10) if not self.actual else (100,100,100), Rect(self.draw_x + self.size_x / 2, self.draw_y, self.size_x / 2, self.size_y / 2))
        super().draw(screen)

class Lawn(EmptyObject):
    def __init__(self: object, x: int, y: int, size_x: int, size_y: int, r: int, g: int, b: int) -> None:
        self.draw_x, self.draw_y = x, y
        self.size_x, self.size_y = size_x, size_y
        self.draw_size_x, self.draw_size_y = size_x, size_y
        self.z = 0
        self.components = []
        self.color = (r, g, b)

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        draw.rect(screen, self.color, Rect(self.draw_x - cam_x, self.draw_y - cam_y, self.size_x, self.size_y))