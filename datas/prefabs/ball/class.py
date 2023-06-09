from CNEngine import *
from math import tan
from pygame import mixer
mixer.init()

class Particle(EmptyObject):
    def __init__(self: object, x: int, y: int, z: int, angle: int) -> None:
        super().__init__(x, y, z)
        self.size_x, self.size_y = (30, 30)
        self.rect = Surface((30, 30), SRCALPHA)
        self.rect.fill((240,240,240, 100))
        self.transparency = 100
        self.angle = angle
    
    def update(self: object, parent: object) -> None:
        self.rect = Surface((30, 30), SRCALPHA)
        self.rect.fill((240,240,240, self.transparency))
        if self.transparency - 5 >= 0:
            self.transparency -= 5
        elif self.transparency - 1 >= 0:
            self.transparency -= 1
    
    def draw(self: object, screen: int, cam_x: int, cam_y: int) -> None:
        screen.blit(transform.rotate(self.rect, self.angle), (self.draw_x - cam_x, self.draw_y - cam_y, self.size_x, self.size_y))

class Ball(Tile):
    def __init__(self: object, x: int, y: int, sprite: object, grid_size: int = 16, pixel_size: int = 3, z: int = 0, force: int = 0.4) -> None:
        super().__init__(x, y, sprite, grid_size, pixel_size, z)

        self.draw_x = x
        self.draw_y = y

        self.sound = mixer.Sound("ball-bounce.wav")

        self.force = force

        self.vectors = [-2,0]

        self.particles = []

        self.max_particles = 30

    def play_bounce_sound(self, volume):
        mixer.Channel(0).set_volume(volume)
        mixer.Channel(0).play(self.sound, 0)

    def check_wall_collision(self, parent):
        if (self.draw_y + self.draw_size_y) >= parent.size[1]:
            self.vectors[1] = -1

        if (self.draw_y) <= 0:
            self.vectors[1] = 1

        #if (self.draw_x + self.draw_size_x) >= parent.size[0]:
        #    self.vectors[0] = -1

        #if (self.draw_x) <= 0:
        #    self.vectors[0] = 1

        for item in parent.objects:
            if type(item).__name__ == "Bar":
                if ((self.draw_x >= item.draw_x and self.draw_x <= item.draw_x + item.size_x) or (self.draw_x + self.draw_size_x >= item.draw_x and self.draw_x + self.draw_size_x <= item.draw_x + item.size_x)) and ((self.draw_y >= item.draw_y and self.draw_y <= item.draw_y + item.size_y) or (self.draw_y + self.draw_size_y >= item.draw_y and self.draw_y + self.draw_size_y <= item.draw_y + item.size_y)):
                    self.play_bounce_sound((0.3 + abs(item.angle) / 10))
                    self.vectors[0] = (1 + abs(item.angle) / 5) * -1 if self.vectors[0] >= 0 else (1 + abs(item.angle) / 5)
                    self.vectors[1] += (-item.angle) / 10 if not item.reverse else (item.angle) / 10
                    if item.reverse:
                        self.move(item.draw_x - self.draw_size_x, self.y, self.z)
                    else:
                        self.move(item.draw_x + item.size_x, self.y, self.z)

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z
        self.particles.append(Particle(self.draw_x + self.size_x / 2, self.draw_y + self.size_y / 2, 0, tan(self.draw_y / self.draw_x)))
        if len(self.particles) > self.max_particles:
            self.particles = self.particles[1:]

    def update(self, parent):
        self.move(self.draw_x + self.force * self.vectors[0], self.draw_y + self.force * self.vectors[1],0) 
        self.check_wall_collision(parent)
        if self.vectors[0] > 0:
            self.vectors[0] -= 0.001
        if self.vectors[0] < 0:
            self.vectors[0] += 0.001
        self.vectors[1] += 0.005

        super().update(parent)

        for item in self.particles:
            item.update(parent)

    def copy(self):
        temp = Ball(self.x, self.y, self.sprite, self.grid, self.pixel_size, self.z, self.force)
        temp.vectors = self.vectors.copy()
        return temp

    def draw(self, screen, cam_x, cam_y):
        for item in self.particles:
            item.draw(screen, cam_x, cam_y)

        super().draw(screen, cam_x, cam_y)

call = "Ball"