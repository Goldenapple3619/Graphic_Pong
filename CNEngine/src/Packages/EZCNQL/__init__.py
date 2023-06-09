from ..DBHandler import *
from .constants import *

def load_cnql_script(path):
    with open(path, 'r') as f:
        text = f.read()

    CNQL_FILES['.'.join(path.split('/')[-1].split('.')[:-1])] = text

def auto_loader():
    for root in CNQL_AUTO_LOAD_PATH:
        path = root + '/' + CNQL_AUTO_LOAD_NAME

        if not isfile(path):
            continue

        DB = DataBase(path)

        for item in read_commands(DB, "READ *;")[0]:
            load_cnql_script(root + '/' + item[1] + '/' + item[0])

def read_query(DB, name, params=tuple()):
    text = CNQL_FILES[name]

    for key, value in params:
        text = text.replace(key, value)

    return read_commands(DB, text)