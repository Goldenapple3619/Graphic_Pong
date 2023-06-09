from .empty_hud import EmptyHud
from ..libs import MOUSEBUTTONDOWN, MOUSEBUTTONUP, mouse

class Button(EmptyHud):
    def __init__(self: object, x: int, y: int, size_x: int, size_y: int, callback = None) -> None:
        super().__init__(x, y)

        self.size_x = size_x
        self.size_y = size_y

        self.draw_size_x = size_x
        self.draw_size_y = size_y

        self.press = False
        self.clicked = False

        self.callback = callback

    def event(self, event):
        m_x, m_y = mouse.get_pos()

        if (m_x < self.draw_x or m_x > self.draw_x+self.draw_size_x) or (m_y < self.draw_y or m_y > self.draw_y+self.draw_size_y):
            return
        
        if not self.press and event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.press = True

        if self.press and event.type == MOUSEBUTTONUP and event.button == 1:
            self.press = False
            self.clicked = True


    def update(self, parent):
        if self.clicked:
            if self.callback is not None:
                self.callback()

            self.clicked = False