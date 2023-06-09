#!/bin/python3

from src.game_common import *

def main(inited = False) -> int:
    if not inited:
        init_engine()
        add_camera_to_game(GAME, CAMERA)

    prefabs = get_prefabs(GAME)

    ball, bar0, bar1 = choose_bar_menu(prefabs)

    run_game(bar0, bar1, ball)

    try:
        GAME.run()
    except KeyboardInterrupt:
        return (130)
    except Exception as e:
        print(f"Unexepted error {e}")
        return (84)

    ball.particles.clear()

    if game_over_menu(bar0, bar1):
        GAME.objects.clear()
        GAME.hud.clear()
        GAME.collection.clear()
        GAME.running = True
        main()

    return (0)

if __name__ == "__main__":
    exit(main())
