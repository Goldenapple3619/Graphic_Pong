from .libs import *

PREFABS_PATH = "datas/prefabs"

def get_prefabs(G):
    prefabs = [(item[1].replace("$prefabs_path$", PREFABS_PATH) + '/' + item[0], item[2], item[3])  for item in read_commands(DataBase("datas/prefabs/include.cnd"), "READ *")[0]]
    loaded = []

    for item in prefabs:
        lib = import_module(item[0].replace('/', '.') + '.' + "class")
 
        CUSTOM_CLASS[lib.call] = getattr(lib, lib.call)

        a = GLD(item[0] + '/' + "structure.gld", G)
        a.lexer()
        loaded.append((a.interpreteur(a.code[0]), item[1], item[2]))

    return loaded