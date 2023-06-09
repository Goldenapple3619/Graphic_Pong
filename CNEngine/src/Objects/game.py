from ..libs import *
from ..Exceptions import *
from ..constants import *

class Game:
    def __init__(self: object, size: tuple, name: str ='Game', grid_size=16, fps = 60, fullscreen = True, color = (0,0,0), resize=False) -> None:
        self.resize = resize
        self.name = name
        self.size = size
        self.fps = fps
        self.color = color
        self.grid_size = grid_size
        self.fullscreen = fullscreen

        self.screen = None
        self.camera = None
        self.running = False

        self.collection = []
        self.objects = []
        self.hud = []
        self.shaders = []

        self.show()

    def sort_z(self):
        self.objects.sort(key=Z_SORT_RULE)

    def add_collection(self, func):
        self.collection.append(func)

    def set_camera(self: object, camera: object):
        self.camera = camera

    def add_hud(self: object, hud: object):
        self.hud.append(hud)

    def add_shader(self: object, shader: object):
        self.shaders.append(shader)

    def add_object(self: object, obj: object):
        self.objects.append(obj)
        self.sort_z()

        for shader in self.shaders:
            shader.apply(self)

    def show(self: object) -> None:
        init()
        font.init()

        display.set_caption(self.name)
        I  = display.Info()

        if not self.fullscreen:
          self.screen = display.set_mode(self.size)
        else:
            if not self.resize:
                self.screen = display.set_mode(self.size, FULLSCREEN|SCALED)
            else:
                self.screen = display.set_mode((I.current_w, I.current_h), FULLSCREEN)
                self.size = (I.current_w, I.current_h)

        self.clock = Clock()

        self.running = True

    def draw(self: object) -> None:
        screen = self.screen
        camera = self.camera

        cam_x = camera.x
        cam_y = camera.y
        cam_z = camera.z

        size_x, size_y = self.size

        screen.fill(self.color)

        for item in self.objects:
            if item.z > cam_z:
                continue;

            d_x = item.draw_x

            if d_x + item.draw_size_x >= cam_x and d_x <= cam_x + size_x:
                d_y = item.draw_y

                if d_y + item.draw_size_y >= cam_y and d_y <= cam_y + size_y:
                    item.draw(screen, cam_x, cam_y)

        for item in self.hud:
            item.draw(screen)

        display.update()

    def update(self: object):
        for ev in event.get():
            if ev.type == QUIT:
                self.running = False

            for item in (*self.hud, *self.objects):
                item.event(ev)

        for item in (*self.hud, *self.objects):
            item.update(self)

        for item in self.collection:
            item(self)

    def stop(self: object) -> None:
        self.running = False

    def run(self: object) -> None:
        if self.camera is None:
            raise(NoCameraSet())

        if not self.running:
            raise(GameNotInited())

        while self.running:
            self.update()
            self.draw()

            self.clock.tick(self.fps)