from ... import *
from .constants import *

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


class DrawableNode(EmptyHud):
    def __init__(self: object, x: int, y: int, color=(0,0,0,0), size:int=30) -> None:
        super().__init__(x, y)
        self.size = size
        self.color = color

        self.debug()

    def debug(self):
        self.surface = Surface(Rect(self.draw_x,self.draw_y, self.size, self.size).size, SRCALPHA)
        draw.rect(self.surface, self.color, self.surface.get_rect())

    def change_color(self, color):
        self.color = color
        self.debug()


    def update(self, parent):
        m_a = mouse.get_pressed()

        if m_a[0]:
            color = parent.get_color()
        else:
            return

        mouse_x, mouse_y = mouse.get_pos()
        x,y,size = self.draw_x,self.draw_y,self.size

        for item in parent.hover_zone:
            if mouse_x >= item[0] and mouse_x <= item[2] and mouse_y >= item[1] and mouse_y <= item[3]:
                return

        if mouse_x >= x and mouse_x <= x + size and mouse_y >= y and mouse_y <= y + size:
            self.change_color(color)

    def draw(self, screen):
        screen.blit(self.surface, (self.draw_x,self.draw_y, self.size, self.size))

class ColorWidget(Container):
    def __init__(self, x, y, sprite=None, size=100):
        super().__init__(x, y, sprite)

        self.saturation = 0

        self.raw = 0
        self.raw_2 = -1

        self.color = (0,0,0)

        self.T_list = []
        self.T_ORDER = ({"edit":1, "full": 0, "zero": 2, "operator": '+'}, {"edit":0, "full": 1, "zero": 2, "operator": '-'}, {"edit":2, "full": 1, "zero": 0, "operator": '+'}, {"edit":1, "full": 2, "zero": 0, "operator": '-'}, {"edit":0, "full": 2, "zero": 1, "operator": '+'}, {"edit":2, "full": 0, "zero": 1, "operator": '-'})

        self.size = size
        self.surface = Surface(Rect(self.draw_x,self.draw_y, self.size, self.size).size, SRCALPHA)
        draw.rect(self.surface, (104,104,104,127), self.surface.get_rect())

        self.big_picker = []
        self.terciary_picker = []

        self.create_t_list()
        self.prepare_secondary_picker()

        size = len(self.T_list)/2
        self.text_r = Text((self.draw_x + self.size/2) + 10,self.draw_y + self.size - size/2 - 120 - (24*3)/2,'R : 0', (255,255,255),font.SysFont("consolas", 24))
        self.text_g = Text((self.draw_x + self.size/2) + 10,self.draw_y + self.size - size/2 - 96 - (24*3)/2,'G : 0',(255,255,255),font.SysFont("consolas", 24))
        self.text_b = Text((self.draw_x + self.size/2) + 10,self.draw_y + self.size - size/2 - 72 - (24*3)/2,'B : 0',(255,255,255),font.SysFont("consolas", 24))

        self.prepare_terciary_picker()

    def create_t_list(self):
        temp_l = []

        for rule in self.T_ORDER:
            for color in range(0,255, 6):
                actual = [0,0,0]
                actual[rule["full"]] = 255
                if rule["operator"] == '+':
                    actual[rule["edit"]] = color
                elif rule["operator"] == '-':
                    actual[rule["edit"]] = 255 - color

                S=Surface(Rect(0,0, 1, 20).size)
                draw.rect(S, actual, S.get_rect())
                temp_l.append((tuple(actual), S))

        self.T_list = temp_l

    def prepare_terciary_picker(self):
        temp_list = []

        s_x = (self.draw_x + 10)
        s_y = (self.draw_y + 10)

        saturation = self.saturation

        actual = self.T_list[self.raw][0]

        for y in range(255,-1, -1):
            r,g,b = map(lambda c: int(c + ((y / 255) * (saturation - c))), actual)

            S=Surface(Rect(0,0, 1, 20).size)

            draw.rect(S, (int(r), int(g), int(b)), S.get_rect())
            temp_list.append(((int(r), int(g), int(b)),S))

        self.terciary_picker = temp_list

        self.color = self.terciary_picker[self.raw_2][0]

        self.text_r.set_text(f"R: {self.color[0]}")
        self.text_g.set_text(f"G: {self.color[1]}")
        self.text_b.set_text(f"B: {self.color[2]}")

    def prepare_secondary_picker(self):
        temp_list = []
        s_x = (self.draw_x + 10)
        s_y = (self.draw_y + 10)
        actual = self.T_list[self.raw][0]
        for y in range(0,255+1):
            r,g,b = map(lambda c: int(c + ((y / 255) * (y/2 - c))), actual)

            S=Surface(Rect(0,0, 1, 20).size)

            draw.rect(S, (int(r), int(g), int(b)), S.get_rect())
            temp_list.append(((int(r), int(g), int(b)),S))

        self.big_picker = temp_list


    def draw_secondary_picker(self, screen):
        s_y = self.draw_y + self.size - 60
        s_x = (self.draw_x + self.size/2) - len(self.big_picker)/2
        for x, item in enumerate(self.big_picker):
            screen.blit(item[1], (x + s_x,s_y, 1, 20))

    def draw_terciary_picker(self, screen):
        s_y = self.draw_y + self.size - 90
        s_x = (self.draw_x + self.size/2) - len(self.terciary_picker)/2
        for x, item in enumerate(self.terciary_picker):
            screen.blit(item[1], (x + s_x,s_y, 1, 20))

    def draw_t_bar(self, screen):
        s_y = self.draw_y + self.size - 30
        s_x = (self.draw_x + self.size/2) - len(self.T_list)/2
        for x, item in enumerate(self.T_list):
            screen.blit(item[1], (s_x + x,s_y, 1, 20))

    def draw(self, screen: object):
        screen.blit(self.surface, (self.draw_x,self.draw_y, self.size, self.size))

        self.draw_t_bar(screen)
        self.draw_secondary_picker(screen)
        self.draw_terciary_picker(screen)

        self.text_b.draw(screen)
        self.text_g.draw(screen)
        self.text_r.draw(screen)

        size = len(self.T_list)/2
        draw.rect(screen, self.color, ((self.draw_x + self.size/2) - size,self.draw_y + self.size - size - 120, size, size))

    def update(self, parent):
        super().update(parent)

    def event(self, event):
        super().event(event)

        m_a = mouse.get_pressed()

        if m_a[0]:

            mouse_x, mouse_y = mouse.get_pos()
            x,y,size = self.draw_x,self.draw_y,self.size

            bar_x = (x + size/2) - len(self.T_list)/2
            bar_y = y + size - 30


            if mouse_x >= bar_x and mouse_x <= bar_x + len(self.T_list)-1 and mouse_y >= bar_y and mouse_y <= bar_y + 20:
                self.raw = int(mouse_x-bar_x)
                self.prepare_secondary_picker()
                self.prepare_terciary_picker()

            bar_x = (x + size/2) - len(self.big_picker)/2
            bar_y = y + size - 60

            if mouse_x >= bar_x and mouse_x <= bar_x + len(self.big_picker)-1 and mouse_y >= bar_y and mouse_y <= bar_y + 20:
                self.saturation = int(mouse_x-bar_x)
                self.prepare_secondary_picker()
                self.prepare_terciary_picker()

            bar_x = (x + size/2) - len(self.terciary_picker)/2
            bar_y = y + size - 90

            if mouse_x >= bar_x and mouse_x <= bar_x + len(self.terciary_picker)-1 and mouse_y >= bar_y and mouse_y <= bar_y + 20:
                self.raw_2 = int(mouse_x-bar_x)
                self.prepare_secondary_picker()
                self.prepare_terciary_picker()


class DrawableZone(Container):
    def __init__(self, x, y, get_color, sprite=None, zoom=3, size=16, hover_zone = []):
        super().__init__(x, y, sprite)

        self.hover_zone = hover_zone

        self.get_color = get_color

        self.zoom = zoom

        self.size = size

        self.back_draw = []

        self.calc_size()

        self.create_nodes()

        self.create_back()

        self.ctrl_press = False
        self.shift_press = False
        self.scroll_start = None
        self.scroling = False
        self.max = None


    def calc_size(self):
        size, zoom = self.size, self.zoom

        self.draw_x = self.x-size*zoom/2
        self.draw_y = self.y-size*zoom/2


        self.draw_end_x = self.draw_x+size*zoom
        self.draw_end_y = self.draw_y+size*zoom


    def update_nodes(self):
        zoom = self.zoom

        for node in self.contained:
            x,y,node_zoom = node.x, node.y, node.size

            node.x = ((x/node_zoom) * zoom)
            node.y = ((y/node_zoom) * zoom)

            node.draw_x = self.draw_x + node.x
            node.draw_y = self.draw_y + node.y
            node.size = self.zoom

            node.debug()

    def create_nodes(self):
        size = self.size
        zoom = self.zoom

        for y in range(0, size):
            for x in range(0,size):
                add_hud_to_container(self, DrawableNode(x*zoom,y*zoom, (0,0,0,0), zoom))

    def create_back(self):
        size = self.size
        zoom = self.zoom

        dx, dy = self.draw_x, self.draw_y

        back_draw = []

        for y in range(0, size):
            for x in range(0,size):
                rect = dx+x*zoom,dy+y*zoom, zoom, zoom
                S = Surface(Rect(rect).size)
                if x % 2 == y%2:
                    color = (220,220,220)
                else:
                    color = (169,169,169)

                draw.rect(S, color, S.get_rect())
                back_draw.append((S, rect))

        self.back_draw = back_draw

    def event(self, event):
        if event.type == KEYDOWN:
            k = event.key

            if k == K_LCTRL:
                self.ctrl_press = True

            elif k == K_LSHIFT:
                self.shift_press = True

        elif event.type == KEYUP:
            k = event.key

            if k == K_LCTRL:
                self.ctrl_press = False

            elif k == K_LSHIFT:
                self.shift_press = False

        elif event.type == MOUSEBUTTONDOWN and self.ctrl_press:
            if event.button == 4:
                self.zoom += 1

            elif event.button == 5 and self.zoom > 1:
                self.zoom -= 1

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4:
                if self.shift_press:
                    if 1*self.zoom + self.x < self.max[0]:
                        self.x += 1*self.zoom
                else:
                    if 1*self.zoom + self.y < self.max[1]:
                        self.y += 1*self.zoom

            elif event.button == 5:
                if self.shift_press:
                    if -1*self.zoom + self.x > 0:
                        self.x -= 1*self.zoom
                else:
                    if -1*self.zoom + self.y > 0:
                        self.y -= 1*self.zoom

            elif event.button == 2:
                self.scroling = True
                self.scroll_start = mouse.get_pos()

        elif event.type == MOUSEBUTTONUP:
            if event.button == 2:
                self.scroling = False
                self.scroll_start = None


        super().event(event)


    def update(self, parent):
        mouse_pos = mouse.get_pos()
        scroll_start = self.scroll_start
        size, zoom = self.size, self.zoom

        if self.max is None:
            self.max = parent.size

        if self.scroling and scroll_start != mouse_pos:
            new_x, new_y = mouse_pos
            x,y = scroll_start
            x,y = new_x - x, new_y - y


            self.scroll_start = new_x,new_y

            if x+ self.x > 0 and y + self.y > 0 and x+ self.x + size < parent.size[0] and y + self.y + size < parent.size[1]:
                self.x += x
                self.y += y


        if self.x-size*zoom//2 != self.draw_x or self.y-size*zoom//2 != self.draw_y:
            self.calc_size()
            self.create_back()
            self.update_nodes()

        super().update(self)

    def draw(self, screen):
        for surface, pos in self.back_draw:
            screen.blit(surface, pos)


        super().draw(screen)

class ToolPick(Container):
    def __init__(self, x, y, picker, sprite=None, size=100):
        super().__init__(x, y, sprite)

        self.picker = picker

        self.tool = 0

        self.size = size

        self.surface = Surface(Rect(self.draw_x,self.draw_y, self.size, self.size*2).size, SRCALPHA)
        draw.rect(self.surface, (104,104,104,127), self.surface.get_rect())

    def get_color(self):
        tool = self.tool

        if tool == 0:
            return self.picker.color

        elif tool == 1:
            return (0,0,0,0)

        else:
            return (0,0,0,255)


    def update(self, parent):
        for item in self.contained:
            item.update(self)

    def event(self, event):
        super().event(event)

    def draw(self, screen: object):
        super().draw(screen)

        screen.blit(self.surface, (self.draw_x,self.draw_y, self.size, self.size*2))

class CustomImage(ImageHud):
    def __init__(self, x, y, iid, sprite=None):
        super().__init__(x, y, sprite)
        self.update_check = False

        self.iid = iid

        self.surface = Surface(Rect(self.draw_x-5,self.draw_y-5, self.draw_size_x+10, self.draw_size_y+10).size, SRCALPHA)
        draw.rect(self.surface, (104,104,104,127), self.surface.get_rect())


    def event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            m_x, m_y = mouse.get_pos()
            if event.button == 1 and (m_x >= self.draw_x-5 and m_y >= self.draw_y-5 and m_x <= self.draw_x + self.draw_size_x+10 and m_y <= self.draw_y + self.draw_size_y+10):
                self.update_check = True

    def update(self, parent):
        if self.update_check:
            self.update_check = False
            parent.tool = self.iid

    def draw(self, screen: object):
        screen.blit(self.surface, (self.draw_x-5,self.draw_y-5, self.draw_size_x+10, self.draw_size_y+10))
        super().draw(screen)

def start_pixel_art_tool():
    init_engine()
    load_include(IMAGES_INCLUDE)

    G = create_game("Pixel Art Tool", fullscreen=True, color=(47,47,47), resize=True)

    size = G.size

    C = Camera(0,0,12)
    add_camera_to_game(G, C)

    zoom = size[0]//70
    draw_size = 32
    pick_size = 300

    Picker = ColorWidget(10,G.size[1]-pick_size-10,size=pick_size)
    Tools=ToolPick(10,10,Picker, None, 150)

    add_hud_to_container(Tools, CustomImage((150/2)/2-32/2, 10, 0, transform.scale(get_image("draw"), (32,32))))
    add_hud_to_container(Tools, CustomImage((150/2)*1.5-32/2, 10,1, transform.scale(get_image("erase"), (32,32))))

    Back = DrawableZone(size[0]/2, size[1]/2, lambda: Tools.get_color(), None, zoom, draw_size, [(10, G.size[1]-pick_size-10, 10+pick_size, G.size[1]-10)])

    Cont_DEBUG = HidableDevMenu(0,0,None, key=K_TAB)
    Cont_2 = HidableDevMenu(0,0,None, key = K_F2)
    Term = Terminal(0,0, {"tool": Tools, "picker": Picker, "canvas": Back, "camera": C, "game": G, "gld": lambda file: GLD(file, G)}, size_x = G.size[0], size_y = G.size[1])

    T = Text(10, 10, color=(255,255,255), font=font.SysFont("Consolas", 12))

    add_script_to_game(G, lambda P: show_fps(T, P))
    add_hud_to_container(Cont_2, Term)

    add_hud_to_game(G, Back)
    add_hud_to_game(G, Tools)
    add_hud_to_game(G, Picker)
    add_hud_to_game(G, Cont_2)
    add_hud_to_container(Cont_DEBUG, T)
    add_hud_to_game(G, Cont_DEBUG)

    G.run()