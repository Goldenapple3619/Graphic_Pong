from CNEngine.dev_tools import *
from sys import argv

def main(args: list) -> None:
    if args == []:
        start_pixel_art_tool()


    elif args[0] == "-p":
        start_pixel_art_tool()

    elif args[0] == "-m":
        start_map_editor_tool()

if __name__ == "__main__":
    exit(main(argv[1:]))