from CNEngine import *
from src.load_prefabs import *

class ImageButton(Button):
    def __init__(self: object, x: int, y: int, size_x: int, size_y: int, sprite: object, callback=None) -> None:
        super().__init__(x, y, size_x, size_y, callback)
        self.sprite = sprite

    def draw(self, screen):
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

class Panel(Container):
    def __init__(self, x, y, sprite=None, size=(1000, 20)):
        super().__init__(x, y, sprite)
        self.rect = Rect(x, y, size[0], size[1])
        self.size_x, self.size_y = size

    def event(self, event):
        super().event(event)

    def update(self, parent):
        super().update(parent)

    def move(self, x, y):
        self.rect = Rect(x, y, self.size_x, self.size_y)
        super().move(x, y)

    def draw(self, screen: object):
        draw.rect(screen, (15,50,170), self.rect)
        super().draw(screen)


class Window(EmptyHud):
    def __init__(self: object, contained: object, title: str) -> None:
        super().__init__(contained.x - 2, contained.y - 20)
        self.size_x = contained.size_x + 4
        self.size_y = contained.size_y + 22
        self.contained = contained
        self.active = False
        self.dragged = False
        self.rect_up = Rect(contained.x - 2, contained.y - 20, contained.size_x + 4, 20)
        self.rect_side = Rect(contained.x - 2, contained.y - 2, self.size_x, contained.size_y + 4)
        self.title = Text(self.x + 2, self.y, title, (255,255,255), font.Font("./Tahoma.ttf", 18), False)
        self.close = ImageButton(self.x + self.size_x - 23, self.y, 21,21, get_image("xp_c"), lambda: (self.show()))

    def show(self):
        self.active = not self.active

    def event(self, event):
        if self.active:
            self.close.event(event)
            self.contained.event(event)

            if event.type == MOUSEBUTTONDOWN and event.pos[0] >= self.draw_x and event.pos[1] >= self.draw_y and event.pos[0] <= self.draw_x + self.size_x - 21 and event.pos[1] <= self.draw_y + 20:
                if mouse.get_pressed()[0]:
                    self.dragged = True
            if event.type == MOUSEBUTTONUP:
                self.dragged = False


    def update(self, parent):
        pos = mouse.get_pos()

        if self.active:
            self.close.update(parent)
            self.contained.update(parent)

            if self.dragged:
                self.move(pos[0], pos[1])

    def move(self, x, y):
        self.contained.move(x + 2, y + 20)
        self.rect_up = Rect(x, y, self.contained.size_x + 4, 20)
        self.rect_side = Rect(x, y + 18, self.size_x, self.contained.size_y + 4)
        self.title.move(x + 2, y)
        self.close.move(x + self.size_x - 23, y)
        super().move(x, y)

    def draw(self, screen):
        if self.active:
            draw.rect(screen, (5,5, 245), self.rect_side)
            self.contained.draw(screen)
            draw.rect(screen, (5,5, 245), self.rect_up)
            self.title.draw(screen)
            self.close.draw(screen)

class TextButton(Button):
    def __init__(self: object, x: int, y: int, size_x: int, size_y: int, text: str, callback=None, color=(0,0,0)) -> None:
        super().__init__(x, y, size_x, size_y, callback)
        self.text_button = Text(self.draw_x,self.draw_y,text, color, font.Font("./Tahoma.ttf", 18), False)

    def move(self,x,y):
        self.text_button.move(self.text_button.draw_x - self.draw_x + x, self.text_button.draw_y - self.draw_y + y)
        super().move(x,y)
        
    def update(self, parent):
        if self.clicked:
            if self.callback is not None:
                self.callback(self.text_button.text)

            self.clicked = False

    def draw(self, screen):
        self.text_button.draw(screen)
        super().draw(screen)

class CustomIcon(ImageButton):
    def __init__(self: object, x: int, y: int, size_x: int, size_y: int, sprite: object, callback=None, args=[]) -> None:
        super().__init__(x, y, size_x, size_y, sprite, callback)
        self.args = args

    def update(self, parent):
        if self.clicked:
            if self.callback is not None:
                self.callback(*self.args)

            self.clicked = False

class SpawnMenu(Container):
    def __init__(self, x, y, game, sprite=None, size=(100,200), tabs=("general", "fun", "items"), prefabs=[]):
        super().__init__(x, y, sprite)
        self.rect = Rect(x, y, size[0], size[1])
        self.size_x, self.size_y = size
        self.tabs = tabs
        self.constructed_tabs = {}
        self.open_tab = tabs[0]
        self.prefabs = prefabs
        self.panel = Panel(0,0,None,(self.size_x, 20))
        self.add_hud(self.panel)
        self.create_menu()
        self.G = game

    def create_menu(self):
        for i,item in enumerate(self.tabs):
            self.constructed_tabs[item] = []
            self.panel.add_hud(TextButton(i*100,0,100,20, item,lambda temp: setattr(self, "open_tab", temp), (15,15,30)))
        decalage = 0
        for i, items in enumerate(self.prefabs):
            decalage += 10
            self.constructed_tabs[items[1]].append(CustomIcon(decalage + self.draw_x,30 + self.draw_y,get_image(items[2]).get_size()[0] * 3, get_image(items[2]).get_size()[1] * 3,get_image(items[2]),lambda thing: add_object_to_game(self.G, thing.copy()), [items[0]]))
            decalage += 10 + get_image(items[2]).get_size()[0] * 3

    def event(self, event):
        for item in self.constructed_tabs[self.open_tab]:
            item.event(event)
        super().event(event)

    def update(self, parent):
        for item in self.constructed_tabs[self.open_tab]:
            item.update(parent)
        super().update(parent)

    def move(self, x, y):
        for items in self.constructed_tabs:
            for item in self.constructed_tabs[items]:
                item.move(item.draw_x - self.draw_x + x, item.draw_y - self.draw_y + y)
        self.rect = Rect(x, y, self.size_x, self.size_y)
        super().move(x, y)

    def draw(self, screen: object):
        draw.rect(screen, (230,230,240), self.rect)
        for item in self.constructed_tabs[self.open_tab]:
            item.draw(screen)
        super().draw(screen)

class Menu(Container):
    def __init__(self, x, y, sprite=None, size=(100,200)):
        super().__init__(x, y, sprite)
        self.rect = Rect(x, y, size[0], size[1])
        self.size_x, self.size_y = size

    def event(self, event):
        super().event(event)

    def update(self, parent):
        super().update(parent)

    def move(self, x, y):
        self.rect = Rect(x, y, self.size_x, self.size_y)
        super().move(x, y)

    def draw(self, screen: object):
        draw.rect(screen, (230,230,240), self.rect)
        super().draw(screen)

class Value(InputBox):
    def __init__(self, x, y, key, value, typ, background, color, font, text_margin=(0,0,0), size_x=None, size_y=None):
        super().__init__(x, y, background, str(value), color, font, text_margin, size_x, size_y)
        self.active = False
        self.type = typ
        self.key = key
        self.value = value

    def event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.pos[0] >= self.draw_x and event.pos[1] >= self.draw_y and event.pos[0] <= self.draw_x + self.draw_size_x and event.pos[1] <= self.draw_y + self.draw_size_y:
            self.active = True
        elif event.type == MOUSEBUTTONDOWN and not (event.pos[0] >= self.draw_x and event.pos[1] >= self.draw_y and event.pos[0] <= self.draw_x + self.draw_size_x and event.pos[1] <= self.draw_y + self.draw_size_y):
            self.active = False
        if event.type == KEYDOWN:
            k = event.key
            if k == K_RETURN:
                self.value = self.type(self.text)
                return

        super().event(event)

    def update(self, *args):
        super().update(*args)

class Planet(EmptyObject):
    def __init__(self, x, y, z, size, color) -> None:
        super().__init__(x, y, z)
        self.color = color
        self.size = size
        self.dragged = False
        self.hover = False
        menu = Menu(x, y)
        self.context_menu = Window(menu, "Menu")
        menu.add_hud(Value(0,0, "size", size, int ,None, (0,0,0), font.Font("./Tahoma.ttf", 18), (0,0,0), self.context_menu.size_x, 18))

    def event(self, event):
        self.context_menu.event(event)
        if event.type == MOUSEBUTTONDOWN and event.pos[0] >= self.x - self.size and event.pos[1] >= self.y - self.size and event.pos[0] <= self.x + self.size and event.pos[1] <= self.y + self.size:
            if mouse.get_pressed()[0] and (not self.context_menu.active or not (event.pos[0] >= self.context_menu.draw_x and event.pos[1] >= self.context_menu.draw_y and event.pos[0] <= self.context_menu.draw_x + self.context_menu.size_x and event.pos[1] <= self.context_menu.draw_y + self.context_menu.size_y)):
                self.dragged = True
            elif mouse.get_pressed()[2]:
                self.context_menu.move(*event.pos)
                self.context_menu.active = True
        if event.type == MOUSEBUTTONUP:
            self.dragged = False


    def update(self, parent):
        self.context_menu.update(parent)
        pos = mouse.get_pos()

        for item in self.context_menu.contained.contained:
            if hasattr(item, "key"):
                setattr(self, item.key, item.value)
    
        if self.dragged:
            self.x = pos[0]
            self.y = pos[1]

            self.draw_x = pos[0]
            self.draw_y = pos[1]
        
        if pos[0] >= self.x - self.size and pos[1] >= self.y - self.size and pos[0] <= self.x + self.size and pos[1] <= self.y + self.size:
            self.hover = True
        else:
            self.hover = False

    def draw(self, screen, cam_x, cam_y):
        draw.circle(screen, self.color, (self.x, self.y), self.size)
        if self.hover:
            draw.circle(screen, (245, 245, 245), (self.x, self.y), self.size + 3, 3)
        self.context_menu.draw(screen)

def main() -> int:
    init_engine()

    G = create_game("test0", fullscreen=True, color=(140,140,140), resize=True)
    C = Camera(0,0,12)
    prefabs = get_prefabs(G)
    panel = Panel(0,0, size=(G.size[0], 20))
    S = Window(SpawnMenu(100, 100, G, size=(600,300), prefabs=prefabs), "SpawnMenu")
    Term = Terminal(200,200,{"spawn_menu": S, "camera": C, "game": G, "gld": lambda file: GLD(file, G)}, size_x = 600, size_y = 300, do_lock = False)
    T_W = Window(Term, "Terminal")
    T_W.active = True
    S.active = True

    
    add_camera_to_game(G, C)

    add_hud_to_game(G, S)
    add_hud_to_game(G, T_W)
    add_hud_to_game(G, panel)

    try:
        G.run()
    except KeyboardInterrupt:
        return 130

    return 0

if __name__ == "__main__":
    exit(main())