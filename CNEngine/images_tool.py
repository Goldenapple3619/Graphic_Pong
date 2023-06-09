from .src.ABC import init_engine
from .src.constants import INCLUDES
from .src.libs import *
from .src.commons import *

try:
    init_engine()
except Exception:
    pass

def get_all_image(path):
    return [f"{path}/{file}" for file in listdir(path) if isfile(f"{path}/{file}")]

def sprite_sheets_cut(file, size):
    sheet = Image.open(file)

    count = 0

    w, h = sheet.size

    name = '.'.join(file.split('/')[-1].split('.')[:-1])

    path = f"./datas/images/{name}"

    if read_query(INCLUDES["image"], "get_include", (("$name$", name),))[0] == []:
        read_query(INCLUDES["image"], "add_include", (("$name$", name),("$path$", "./datas/images/"), ("$type$", "dir")))

    if not isdir(path):
        mkdir(path)

    for y in range(h//size[1]):

        for x in range(w//size[0]):

            x_ = (x + 1) * size[0]
            y_ = (y + 1) * size[1]

            img = sheet.crop((x_ - size[0], y_ - size[1], x_, y_))

            background = Image.new("RGBA", img.size, (255, 255, 255, 0))
            background.paste(img)
            background.save(f"{path}/{name}{count}.png")

            count += 1

def cut_sprites(size = (16,16)):
    for sheet in get_all_image(f"./datas/images/sheets"):
        print(f"cutting : {sheet}....")
        sprite_sheets_cut(sheet, size)


def main(args):
    if args == []:
        cut_sprites()

    elif args[0] == "-a":
        read_query(INCLUDES["image"], "add_include", (("$name$", input("Enter Name: ")),("$path$", input("Enter Path: ")), ("$type$", input("Enter Type [file/dir]: "))))

    return 0

if __name__ == "__main__":
    exit(main(argv[1:]))