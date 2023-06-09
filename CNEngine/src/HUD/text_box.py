from .text import Text
from ..libs import transform, MOUSEBUTTONDOWN


class TextBox(Text):
    def __init__(self, x, y, background=None, text='', color=(0,0,0), font=None, text_margin=(0,0,0,0), split_newline = True, size_x=None, size_y=None, scrollable = False):
        while len(text_margin) < 4:
            text_margin = text_margin + (0,)

        self.text_margin = text_margin
        self.scrollable = scrollable
        self.scroll = 0

        if background is not None:
            self.size_x = background.get_width()
            self.size_y = background.get_height()

            self.draw_size_x = self.size_x
            self.draw_size_y = self.size_y
        else:
            self.size_x, self.draw_size_x = size_x, size_x
            self.size_y, self.draw_size_y = size_y, size_y

        self.sprite = background

        super().__init__(x + text_margin[0] - text_margin[2], y + text_margin[1] - text_margin[3], text, color, font, split_newline)

        self.temp_draw_y = self.draw_y

    def event(self, event):
        if self.scrollable and event.type == MOUSEBUTTONDOWN:
            button = event.button
            if button == 4: self.scroll = min(self.scroll + 15, 0)
            if button == 5: self.scroll = max(self.scroll - 15, -len(self.draw_text.split('\n')*12))

    def debug(self):
        draw_size_x = self.draw_size_x

        if draw_size_x is not None and self.split_newline:

            splitted = self.draw_text.split('\n')

            for index, item in enumerate(splitted):
                while len(item.split('\n')[-1]) * 12 > draw_size_x:
                    item = '\n'.join(item.split('\n')[:-1] + [item.split('\n')[-1][:(int(draw_size_x/7))] + '\n' + item.split('\n')[-1][int(draw_size_x/7):]])
                    splitted[index] = item

            self.draw_text = '\n'.join(splitted)

        super().debug()

    def draw(self, screen):
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

        if self.scrollable:
            draw_y = self.draw_y
            self.temp_draw_y = draw_y
            self.draw_y += self.scroll

        super().draw(screen)

        if self.scrollable:
            self.draw_y = draw_y