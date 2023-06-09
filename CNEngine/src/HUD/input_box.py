from .text_box import TextBox

from ..libs import *
from ..constants import *

class InputBox(TextBox):
    def __init__(self, x, y, background, text, color, font, text_margin=(0,0,0), size_x = None, size_y= None):
        super().__init__(x, y, background, text, color, font, text_margin, False, size_x, size_y)

        self.active = True

        self.pointer_pos = -1

        self.caps = False
        self.caps_lock = False
        self.alt = False

        self.counter = 0

    def reset_counter(self):
        self.counter = 30

    def reset(self):
        self.set_text('')
        self.pointer_pos = -1
        self.active = True
        self.caps = False
        self.alt = False

    def update(self, *args):
        if self.counter == 0:
            self.reset_counter()

        self.counter -= 1

        super().update(*args)

    def event(self, event):
        if not self.active:
            return

        if event.type == KEYUP:
            k = event.key

            if k == K_LSHIFT:
                self.caps = False

            elif k == K_RALT:
                self.alt = False

        if event.type == KEYDOWN:
            k = event.key

            if k == K_CAPSLOCK:
                self.caps_lock = not self.caps_lock
            elif k == K_LSHIFT:
                self.caps = True
            elif k == K_RALT:
                self.alt = True

            if not k in INPUT_LIST:
                return

            if self.alt:
                item = ALT_INPUT_LIST[k]
            elif (self.caps or self.caps_lock) and not (self.caps_lock and self.caps):
                item = MAJ_INPUT_LIST[k]
            else:
                item = INPUT_LIST[k]

            if item == "LDEL":
                if self.pointer_pos > -1:
                    self.set_text(self.text[:self.pointer_pos] + self.text[self.pointer_pos+1:])

                    self.pointer_pos -= 1

            elif item == "RDEL":
                if self.pointer_pos < len(self.text) - 1:
                    self.set_text(self.text[:self.pointer_pos+1] + self.text[self.pointer_pos+2:])

            elif item == "LEFT":
                if self.pointer_pos > -1:
                    self.pointer_pos -= 1

            elif item == "RIGHT":
                if self.pointer_pos < len(self.text) - 1:
                    self.pointer_pos += 1

            else:
                self.set_text(self.text[:self.pointer_pos+1] + item + self.text[self.pointer_pos+1:])
                self.pointer_pos += 1

    def draw(self, screen):
        text = self.text

        if self.pointer_pos == len(self.text) - 1:
            if self.counter > 10:
                    self.set_text(self.text[:self.pointer_pos+1] + '_' + self.text[self.pointer_pos+1:])
        else:
            self.set_text(self.text[:self.pointer_pos+1] + '_' + self.text[self.pointer_pos+1:])

        super().draw(screen)

        if self.counter > 10 or self.pointer_pos < len(self.text) - 1:
            self.set_text(text)