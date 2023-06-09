from .empty_hud import EmptyHud

class Text(EmptyHud):
    def __init__(self: object, x:int, y: int, text: str='', color: tuple=(0,0,0), font: object=None, split_newline=True) -> None:
        super().__init__(x, y)

        self.font = font
        self.text = text
        self.draw_text = text
        self.color = color
        self.split_newline = split_newline

        self.debug()

    def debug(self):
        font = self.font

        if font is not None:
            if self.split_newline:
                self.render = []
                for i, item in enumerate(self.draw_text.split('\n')):
                    actual = font.render(item, 0, self.color)
                    self.render.append((actual, actual.get_rect()))
            else:
                self.render = font.render(self.draw_text, 0, self.color)
                self.rect = self.render.get_rect()


    def set_text(self, text):
        self.text = text
        self.draw_text = text
        self.debug()

    def set_color(self, color):
        self.color = color
        self.debug()

    def set_font(self, font):
        self.font = font
        self.debug()

    def update(self, *args):
        pass

    def draw(self, screen):
        if self.font is not None:
            if self.split_newline:
                for i, item in enumerate(self.render):
                    render, rect = item
                    if (hasattr(self, "size_y") and hasattr(self, "temp_draw_y") and self.size_y != None and self.draw_y + i*12 > self.size_y + self.temp_draw_y - 12):
                        return
                    if (not hasattr(self, "temp_draw_y") or (self.draw_y + i * 12 + 12 > self.temp_draw_y)):
                        screen.blit(render, (self.draw_x, self.draw_y+i*12), rect)
            else:
                screen.blit(self.render, (self.draw_x, self.draw_y), self.rect)