from ctypes import resize
from .libs import *
from .commons import *
from .constants import *
from .Objects import *
from .Preset import *
from .Shaders import *
from .HUD import *
from .GLD_setup_func import *

def create_game(name: str = "Game", size: tuple = (800, 400), grid_size: int = 16, fps: int=FPS, fullscreen: bool = False, color: tuple = (0,0,0), resize: bool = False) -> object:
    return  Game(size, name, grid_size, fps, fullscreen, color, resize)

def create_camera(x: int, y: int, z: int = 0) -> object:
    return Camera(x, y, z)

def add_camera_to_game(game: object, camera: object) -> None:
    game.set_camera(camera)

def add_object_to_game(game:object, obj: object) -> None:
    game.add_object(obj)

def add_hud_to_game(game: object, hud: object) -> None:
    game.add_hud(hud)

def add_hud_to_container(container: object, hud: object) -> None:
    container.add_hud(hud)

def add_script_to_game(game: object, script: object) -> None:
    game.add_collection(script)

def add_action_to_player(player: object, condition: object, action: object) -> None:
    player.player_set_action(condition, action)

def free_editor(parent):
    distance = parent.clock.get_fps() * 0.4

    camera = parent.camera

    k = get_pressed()

    if k[K_UP]:
        camera.move(camera.x, camera.y - distance, camera.z)
    if k[K_DOWN]:
        camera.move(camera.x, camera.y + distance, camera.z)
    if k[K_LEFT]:
        camera.move(camera.x - distance, camera.y, camera.z)
    if k[K_RIGHT]:
        camera.move(camera.x + distance, camera.y, camera.z)

def show_fps(text_, parent):
    game_fps = round(parent.clock.get_fps())

    if game_fps >= 45:
        text = (f"fps : {game_fps}", (0, 255, 0))
    elif game_fps < 45 and game_fps > 25:
        text = (f"fps : {game_fps}", (255, 255, 0))
    else:
        text = (f"fps : {game_fps}", (255, 0, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_nb_objects(text_, parent):
    nb_objects = len(parent.objects)

    if nb_objects >= 2000:
        text = (f"loaded objects : {nb_objects}", (255, 0, 0))
    elif nb_objects < 2000 and nb_objects > 100:
        text = (f"loaded objects : {nb_objects}", (255, 255, 0))
    else:
        text = (f"loaded objects : {nb_objects}", (0, 255, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_nb_hud(text_, parent):
    nb_objects = len(parent.hud)

    if nb_objects >= 200:
        text = (f"loaded hud : {nb_objects}", (255, 0, 0))
    elif nb_objects < 200 and nb_objects > 50:
        text = (f"loaded hud : {nb_objects}", (255, 255, 0))
    else:
        text = (f"loaded hud : {nb_objects}", (0, 255, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_nb_scripts(text_, parent):
    nb_objects = len(parent.collection)

    if nb_objects >= 100:
        text = (f"loaded script : {nb_objects}", (255, 0, 0))
    elif nb_objects < 100 and nb_objects > 35:
        text = (f"loaded script : {nb_objects}", (255, 255, 0))
    else:
        text = (f"loaded script : {nb_objects}", (0, 255, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_memory_usage(text_, parent):
    nb_objects = get_memory_usage()

    if nb_objects >= 1500:
        text = (f"mem : {nb_objects} / {get_total_memory()} MB", (255, 0, 0))
    elif nb_objects < 1500 and nb_objects > 500:
        text = (f"mem : {nb_objects} / {get_total_memory()} MB", (255, 255, 0))
    else:
        text = (f"mem : {nb_objects} / {get_total_memory()} MB", (0, 255, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_processor_usage(text_, parent):
    nb_objects = get_cpu_percent()

    if nb_objects >= 70:
        text = (f"proc : {nb_objects} %", (255, 0, 0))
    elif nb_objects < 70 and nb_objects > 30:
        text = (f"proc : {nb_objects} %", (255, 255, 0))
    else:
        text = (f"proc : {nb_objects} %", (0, 255, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_disk_usage(text_, parent):
    r,w = get_disk_usage()

    if r >= 70:
        text = (f"Read : {r} MB, Write: {w} MB", (255, 0, 0))
    elif r < 70 and r > 30:
        text = (f"Read : {r} MB, Write: {w} MB", (255, 255, 0))
    else:
        text = (f"Read : {r} MB, Write: {w} MB", (0, 255, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_window_size(text_, parent):
    x,y = display.get_surface().get_size()

    text = (f"window size : {x}x{y}", (0, 0, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_camera_pos(text_, parent, C):
    x,y,z = round(C.x, 2), round(C.y, 2), C.z

    text = (f"camera pos : {x} , {y} , {z}", (0, 0, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])

def show_camera_grid_pos(text_, parent, C):
    x,y,z = int(C.x)//parent.grid_size, int(C.y)//parent.grid_size, C.z

    text = (f"camera grid pos : {x} , {y} , {z}", (0, 0, 0))

    text_.set_text(text[0])
    text_.set_color(text[1])


def load_image(key, value):
    LOADED_IMAGES[key] = image.load(value)

def load_image_dir(path):
    for item in listdir(path):
        if not isfile(path + '/' + item):
            continue;

        load_image('.'.join(item.split('.')[:-1]), path + '/' + item)

def parse_association(text):
    for item in ASSOCIATION:
        if item not in text:
            continue;

        text = text.replace(item, ASSOCIATION[item])

    return text

def load_include(path):
    for item in read_query(DataBase(path), "get_all_includes")[0]:
        complete_path = parse_association(item[1]) + '/' + item[0]

        if item[2] == "file":
            load_image('.'.join(item[0].split('.')[:-1]), complete_path)

        else:
            load_image_dir(complete_path)

def auto_load_images():
    for item in read_query(INCLUDES["image"], "get_all_includes")[0]:
        complete_path = parse_association(item[1]) + '/' + item[0]

        if item[2] == "file":
            load_image('.'.join(item[0].split('.')[:-1]), complete_path)

        else:
            load_image_dir(complete_path)

def color_blend(color_fg, color_bg, percent=0.5):
    if color_bg[3] == 0:
        return color_bg

    percent_bg = 1-percent

    percent_mod = 1 - (1 - percent) * (1 - percent_bg)

    blend = list(map(lambda c: c[0]*percent/percent_mod+c[1]*percent_bg*(1-percent)/percent_mod, ((color_fg[0],color_bg[0]),(color_fg[1],color_bg[1]),(color_fg[2],color_bg[2]))))

    return blend + [color_bg[3]]

def init_engine():
    CNQL_AUTO_LOAD_PATH.append(get_working_dir())
    auto_loader()
    auto_load_images()
    init_tags(tag_pool)