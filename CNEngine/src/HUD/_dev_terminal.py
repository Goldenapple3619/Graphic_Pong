from .empty_hud import EmptyHud
from .text_box import TextBox
from .input_box import InputBox
from ..commons import *
from ..libs import *

def gld_interp(term, args):
    if len(args) > 0:
        G = term.class_dict["gld"](args[0])

        G.lexer()
        G.interpret()

def edit_class(term, args):
    classes = term.class_dict
    if len(args) > 3:
        class_, attr, value, type_ = args
        if class_ in classes:
            class_ = classes[class_]
        else:
            return f"Class not found {class_}"

        if type_ == "int":
            value = int(value)
        elif type_ == "float":
            value = float(value)
        elif type_ == "str":
            pass
        elif type_ == "bool":
            type_ = bool(value)
        elif type_ == "list":
            type_ = list(value)
        elif type_ == "tuple":
            type_ = tuple(value)
        elif type_ == "dict":
            type_ = dict(value)
        else:
            return f"Invalid type {type_}"

        if hasattr(class_, attr):
            attr_old = getattr(class_, attr)
            setattr(class_, attr, value)
        else:
            return f"class {type(class_).__name__} has no attr \"{attr}\""

        return f"Succesfully edited {attr} from {type(class_).__name__}: {attr_old} -> {value}"

def show_class(term, args):
    classes = term.class_dict

    if len(args) > 0:
        class_ = args[0]
        if class_ in classes:
            class_ = classes[class_]
        else:
            return f"Class not found {class_}"

        if len(args) > 1:
            return f"[{type(class_).__name__}]:\n  - {args[1]}: {getattr(class_, args[1])}"
        else:
            return f"[{type(class_).__name__}]:\n" + '\n'.join([f"  - {attr}: {value}" for attr, value in class_.__dict__.items()])
    else:
        return '\n\n'.join([f"[{class_}]:\n" + '\n'.join([f"  - {attr}: {value}" for attr, value in classes[class_].__dict__.items()]) for class_ in classes])

def exit_(term, args):
    term.lock_ = False
    return ''

com_d = {
    "editc": edit_class,
    "showc": show_class,
    "gld": gld_interp,
    "exit": exit_
}

class Terminal(EmptyHud):
    def __init__(self: object, x: int, y: int, class_dict: dict, commands_dict: dict = com_d, size_x=None, size_y=None, do_lock = True) -> None:
        super().__init__(x, y)

        self.size_x, self.size_y = size_x, size_y

        self.commands_dict = commands_dict
        self.class_dict = class_dict

        self.stdout = TextBox(x,y, None, "[Dev Terminal]\n", (255,255,255), font.SysFont("Consolas", 12), (0,0,0,0), True, size_x, size_y, True)
        self.stdin = InputBox(x,y + size_y-12, None, '', (255,255,255) , font.SysFont("Consolas", 12), (0,0,0,0), size_x, 12)

        self.do_lock = do_lock
        self.lock_ = False

    def move(self, x, y):
        self.stdout.move(x, y)
        self.stdin.move(x,y + self.size_y - 12)
        super().move(x, y)

    def read_command(self, command):
        command = command.split(" ")
        if command == [] or command[0] == '':
            return ''
        if command[0] in self.commands_dict:
            if len(command) > 1:
                return self.commands_dict[command[0]](self, command[1:])
            else:
                return self.commands_dict[command[0]](self, [])
        else:
            return f"Invalid command : {command[0]}"

    def lock(self, parent):
        if not self.do_lock:
            return
        self.lock_ = True
        world = parent["world"]
        clock = world.clock
        fps = world.fps
        tick = clock.tick
        screen = world.screen

        while self.lock_:
            self.update(parent)
            for ev in event.get():
                self.event(ev)

            self.draw(screen)
            tick(fps)

        parent["parent"].hide = True


    def update(self, parent):
        self.stdin.update(parent)
        self.stdout.update(parent)

        if not self.lock_:
            self.lock(parent)

        if self.stdin.text != '' and self.stdin.text[-1] == '\n':
            self.stdout.set_text(self.stdout.text + '\n' + "[prompt]-$ " + self.stdin.text[:-1])
            self.stdout.set_text(self.stdout.text + '\n' + str(self.read_command(self.stdin.text[:-1])) + '\n')
            self.stdin.reset()

    def event(self, event):
        self.stdin.event(event)
        self.stdout.event(event)

        if event.type == KEYDOWN:
            k = event.key

            if k == K_F2:
                self.lock_ = False

    def draw(self, screen):
        if self.do_lock:
            screen.fill((0,0,0))
            super().draw(screen)

        draw.rect(screen, (0,0,0), Rect(self.draw_x, self.draw_y, self.size_x, self.size_y))

        self.stdout.draw(screen)

        draw.rect(screen, (0,0,255), Rect(self.draw_x,self.draw_y + self.size_y-12, self.size_x, 12))

        self.stdin.draw(screen)

        if self.do_lock:
            display.update()