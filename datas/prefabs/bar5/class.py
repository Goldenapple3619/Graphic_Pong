from CNEngine import *
from pygame import key
from math import cos, pi, sin

class Bar(EmptyObject):
    def __init__(self: object, x: int, y: int, sprite: object, pixel_size: int = 3, z: int = 0, force: int = 0.4, size: int = 3) -> None:
        super().__init__(x, y, z)

        self.sprite = sprite

        self.size = size

        self.size_x = 7 * pixel_size
        self.size_y = (7 * pixel_size) * 2 + (5 * pixel_size) * size

        self.draw_size_x = self.size_x
        self.draw_size_y = self.size_y

        self.pixel_size = pixel_size
        
        self.top = Surface((7, 7), SRCALPHA).convert_alpha()
        self.top.blit(sprite.convert_alpha(), (0,0))

        self.middle = Surface((7, 5), SRCALPHA).convert_alpha()
        self.middle.blit(sprite.convert_alpha(), (0,-7))

        self.bottom = Surface((7, 7), SRCALPHA).convert_alpha()
        self.bottom.blit(sprite.convert_alpha(), (0,-12))

        self.force = force

        self.move_to = None

        self.angle = 0

        self.reverse = False

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def event(self, event):
        if event.type == KEYDOWN:
            if (event.key == (K_o if self.reverse else K_z)):
                self.move_to = "up"
            if (event.key == (K_l if self.reverse else K_s)):
                self.move_to = "down"
            #if (event.key == K_LEFT):
            #    self.move_to = "left"
            #if (event.key == K_RIGHT):
            #    self.move_to = "right"

        if event.type == KEYUP:
            if (event.key == (K_o if self.reverse else K_z) and self.move_to == "up"):
                self.move_to = None
            if (event.key == (K_l if self.reverse else K_s) and self.move_to == "down"):
                self.move_to = None
            #if (event.key == K_LEFT and self.move_to == "left"):
            #    self.move_to = None
            #if (event.key == K_RIGHT and self.move_to == "right"):
            #    self.move_to = None

    def set_size(self, size):
        self.size = size
        self.size_y = (7 * self.pixel_size) * 2 + (5 * self.pixel_size) * size

    def update(self, parent):
        if self.move_to == "up":
            self.move(self.x, self.y - self.force, self.z)
            if not self.reverse:
                if self.angle < 10: self.angle += 0.5
            else:
                if self.angle > -10: self.angle -= 0.5
        elif self.move_to == "down":
            self.move(self.x, self.y + self.force, self.z)
            if not self.reverse:
                if self.angle > -10: self.angle -= 0.5
            else:
                if self.angle < 10: self.angle += 0.5
        else:
            if self.angle > 0: self.angle -= 0.5
            if self.angle < 0: self.angle += 0.5
        #elif self.move_to == "left":
        #    self.angle += 1
        #elif self.move_to == "right":
        #    self.angle -= 1
        if self.draw_y < 0:
            self.move(self.draw_x, 0, self.z)
        if self.draw_y + self.size_y > parent.size[1]:
            self.move(self.draw_x, self.draw_y - (self.draw_y + self.size_y - parent.size[1]), self.z)
        super().update(parent)

    def copy(self):
        temp = Bar(self.x, self.y, self.sprite, self.pixel_size, self.z, self.force, self.size)
        return temp

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        screen.blit(
            transform.rotate(
                transform.scale(
                    self.top,
                    (
                        self.draw_size_x,
                        (7 * self.pixel_size)
                    )
                ),
                self.angle
            ),
            (
                self.draw_x-cam_x,self.draw_y-cam_y
            )
        )

        for i in range(self.size):
            screen.blit(
                transform.rotate(
                    transform.scale(
                        self.middle,
                        (
                            self.draw_size_x,
                            (5 * self.pixel_size)
                        )
                    ),
                    self.angle
                ),
                (self.draw_x + (5 * self.pixel_size * i + 7 * self.pixel_size) * cos((self.angle - 90) * pi/180) - cam_x,(self.draw_y - ((5 * self.pixel_size) * i + 7 * self.pixel_size) * sin((self.angle - 90) * pi / 180))-cam_y) if sin((self.angle - 90) * pi / 180) < 0 and cos((self.angle - 90) * pi/180) > 0 else (self.draw_x + ((5 * self.pixel_size) * i + 5 * self.pixel_size) * cos((self.angle - 90) * pi/180) - cam_x,(self.draw_y - ((5 * self.pixel_size) * i + 5 * self.pixel_size) * sin((self.angle - 90) * pi / 180))-cam_y)
    
            )

        screen.blit(
            transform.rotate(
                transform.scale(
                    self.bottom,
                    (
                        self.draw_size_x,
                        (7 * self.pixel_size)
                    )
                ),
                self.angle
            ),
            (
                (self.draw_x + (5 * self.pixel_size * self.size + 7 * self.pixel_size) * cos((self.angle - 90) * pi/180) - cam_x,(self.draw_y - ((5 * self.pixel_size) * self.size + 7 * self.pixel_size) * sin((self.angle - 90) * pi / 180))-cam_y) if sin((self.angle - 90) * pi / 180) < 0 and cos((self.angle - 90) * pi/180) > 0 else (self.draw_x + ((5 * self.pixel_size) * self.size + 5 * self.pixel_size) * cos((self.angle - 90) * pi/180) - cam_x,(self.draw_y - ((5 * self.pixel_size) * self.size + 5 * self.pixel_size) * sin((self.angle - 90) * pi / 180))-cam_y)
            )
        )

call = "Bar"