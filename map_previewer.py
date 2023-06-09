from src.classes import *
from src.libs import *
from src.game_common import *
from sys import argv

def make_map():
    CUSTOM_CLASS["Lawn"] = Lawn

    maps = GLD(f"./datas/maps/map{int(argv[1])}.gld", GAME)
    maps.lexer()
    maps.interpret()

    add_script_to_game(GAME, lambda *args: free_cam())

def main():
    init_engine()

    add_camera_to_game(GAME, CAMERA)

    make_map()

    try:
        GAME.run()
    except KeyboardInterrupt:
        return (130)
    except Exception as e:
        print(f"Unexepted error {e}")
        return (84)

if __name__ == "__main__":
    main()