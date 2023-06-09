from ... import *


class HidableDevMenu(Container):
    def __init__(self, x, y, sprite, hide=True, key=K_p):
        self.hide = hide
        self.key = key

        super().__init__(x, y, sprite)

    def update(self, parent):
        if self.hide:
            return

        super().update({"world":parent, "parent":self})

    def event(self, event):
        if not self.hide:
            super().event(event)

        if event.type == KEYDOWN:
            if event.key == self.key:
                self.hide = not self.hide

    def draw(self, screen):
        if self.hide:
            return
        super().draw(screen)


class SpritePicker(Container):
    def __init__(self, x, y, sprite=None, size=(0,0)):
        super().__init__(x, y, sprite)

        self.tool = 0

        self.size = size

        self.surface = Surface(Rect(self.draw_x,self.draw_y, self.size[0], self.size[1]).size, SRCALPHA)
        draw.rect(self.surface, (104,104,104,127), self.surface.get_rect())


    def update(self, parent):
        for item in self.contained:
            item.update(self)

    def event(self, event):
        super().event(event)

    def draw(self, screen: object):
        super().draw(screen)

        screen.blit(self.surface, (self.draw_x,self.draw_y, self.size[0], self.size[1]))

class Canvas(EmptyHud):
    def __init__(self, x,y,color, size):
        super().__init__(x, y)
        self.color = color

        self.size = size

        self.surface = Surface(Rect(self.draw_x,self.draw_y, self.size[0], self.size[1]).size, SRCALPHA)
        draw.rect(self.surface, color, self.surface.get_rect())

    def draw(self, screen: object):
        super().draw(screen)

        screen.blit(self.surface, (self.draw_x,self.draw_y, self.size[0], self.size[1]))


class SpriteImage(ImageHud):
    def __init__(self, x, y, name, sprite=None):
        super().__init__(x, y, sprite)

        self.name = name

def start_map_editor_tool():
    init_engine()
    load_include(IMAGES_INCLUDE)

    G = create_game("Map Editor Tool", fullscreen=True, color=(47,47,47), resize=True)

    size = G.size

    max_size = 64

    C = Camera(0,0,12)
    add_camera_to_game(G, C)

    zoom = size[0]//70

    sprite_pick = SpritePicker(0,0, None, (size[0], size[1]*(1-(100-10)/100)))
    canvas = Canvas(0, size[1]*(1-(100-10)/100), (0,0,0), (size[0], size[1] - (size[1]*(1-(100-10)/100))))

    pos = 0

    for item in LOADED_IMAGES:
        g = get_image(item)
        if g.get_height() > max_size or g.get_width() > max_size:
            continue;

        add_hud_to_container(sprite_pick, SpriteImage((pos + 10),sprite_pick.size[1]//2-g.get_height()//2, item, g))

        pos += g.get_width() + 10

    add_hud_to_game(G, sprite_pick)
    add_hud_to_game(G, canvas)

    Cont_DEBUG = HidableDevMenu(0,0,None, key=K_TAB)
    Cont_2 = HidableDevMenu(0,0,None, key = K_F2)
    Term = Terminal(0,0, {"camera": C, "game": G, "gld": lambda file: GLD(file, G)}, size_x = G.size[0], size_y = G.size[1])

    T = Text(10, 10, color=(255,255,255), font=font.SysFont("Consolas", 12))

    add_script_to_game(G, lambda P: show_fps(T, P))
    add_hud_to_container(Cont_DEBUG, T)
    add_hud_to_container(Cont_2, Term)
    add_hud_to_game(G, Cont_DEBUG)
    add_hud_to_game(G, Cont_2)

    G.run()