from .constants import *
from .libs import *
from .load_prefabs import *
from .constants import *
from .classes import *


def randomize_vector(ball) -> None:
    ball.vectors[0] = randint(-2, 2)
    if ball.vectors[0] == 0: ball.vectors[0] = 1

def check_win_condition(bar0, bar1, ball) -> None:
    if (ball.draw_x + ball.draw_size_x) >= GAME.size[0]:
        ball.move(GAME.size[0] / 2 - ball.size_x / 2, GAME.size[1] / 2 - ball.size_y / 2, ball.z)
        bar0.score += 1
        randomize_vector(ball)
        mixer.Channel(1).set_volume(0.5)
        mixer.Channel(1).play(SCORE_SOUND)

    if (ball.draw_x) <= 0:
        ball.move(GAME.size[0] / 2 - ball.size_x / 2, GAME.size[1] / 2 - ball.size_y / 2, ball.z)
        bar1.score += 1
        randomize_vector(ball)
        mixer.Channel(1).set_volume(0.5)
        mixer.Channel(1).play(SCORE_SOUND)

    if bar0.score >= 10 or bar1.score >= 10:
        GAME.stop()

def terminator(bar, ball):
    if int(ball.draw_y + ball.draw_size_y / 2) == int(bar.draw_y + bar.size_y / 2):
        bar.move_to = None
    elif (bar.reverse and ball.vectors[0] < 0) or (not bar.reverse and ball.vectors[0] > 0):
        bar.move_to = None
    elif ((ball.draw_y + ball.draw_size_y / 2 > bar.draw_y + bar.size_y / 2 or ball.draw_y + ball.draw_size_y / 2 > bar.draw_y + bar.size_y / 2)) and (ball.x >= GAME.size[0] / 2 if bar.reverse else  ball.x <= GAME.size[0] / 2):
        bar.move_to = "down"
    elif ((ball.draw_y + ball.draw_size_y / 2 < bar.draw_y + bar.size_y / 2 or ball.draw_y + ball.draw_size_y / 2 < bar.draw_y + bar.size_y / 2)) and (ball.x >= GAME.size[0] / 2 if bar.reverse else  ball.x <= GAME.size[0] / 2):
        bar.move_to = "up"
    else:
        bar.move_to = None

def free_cam():
    keys=get_pressed()

    if not keys[K_f]: return
    while 1:
        event.get()
        keys=get_pressed()
    
        if keys[K_ESCAPE]:
            break
        if keys[K_LEFT]:
            CAMERA.x -= 10.5
        if keys[K_UP]:
            CAMERA.y -= 10.5
        if keys[K_RIGHT]:
            CAMERA.x += 10.5
        if keys[K_DOWN]:
            CAMERA.y += 10.5
        GAME.draw()
        GAME.clock.tick(GAME.fps)
    CAMERA.x = 0
    CAMERA.y = 0

def create_map(bar_0, bar_1):
    CUSTOM_CLASS["Lawn"] = Lawn

    maps = GLD(f"./datas/maps/map{randint(0,4)}.gld", GAME)
    maps.lexer()
    maps.interpret()

    score1 = Text(GAME.size[0] / 3, GAME.size[1] / 5, "0", (255,255,255), font.Font("./Tahoma.ttf", 40), False)
    score2 = Text(GAME.size[0] / 1.5, GAME.size[1] / 5, "0", (255,255,255), font.Font("./Tahoma.ttf", 40), False)

    add_hud_to_game(GAME, score1)
    add_hud_to_game(GAME, score2)

    add_script_to_game(GAME, lambda *args: free_cam())

    add_script_to_game(GAME, lambda *args: score1.set_text(str(bar_0.score)))
    add_script_to_game(GAME, lambda *args: score2.set_text(str(bar_1.score)))

def run_game(bar_0, bar_1, ball):
    GAME.running = True
    bar_0.move(50, GAME.size[1] / 2 - bar_0.size_y / 2, bar_0.z)
    bar_0.score = 0

    bar_1.move(GAME.size[0] - 100, GAME.size[1] / 2 - bar_1.size_y / 2, bar_1.z)
    bar_1.score = 0
    bar_1.reverse = True

    if bar_0.is_bot:
        add_script_to_game(GAME, lambda *args: terminator(bar_0, ball))
    if bar_1.is_bot:
        add_script_to_game(GAME, lambda *args: terminator(bar_1, ball))

    create_map(bar_0, bar_1)

    ball.move(GAME.size[0] / 2 - ball.size_x / 2, GAME.size[1] / 2 - ball.size_y / 2, ball.z)
    randomize_vector(ball)

    add_object_to_game(GAME, bar_0)
    add_object_to_game(GAME, bar_1)
    add_object_to_game(GAME, ball)
    
    add_script_to_game(GAME, lambda *args: check_win_condition(bar_0, bar_1, ball))

def game_over_menu(player1, player2):
    GAME.running = True
    menu = get_image("back_menu")
    menu_container = Container(GAME.size[0] / 2 - (menu.get_size()[0] * 4) / 2, GAME.size[1] / 2 - (menu.get_size()[1] * 4) / 2, transform.scale(menu, (menu.get_size()[0] * 4, menu.get_size()[1] * 4)))

    start = StartButton(menu_container.size_x / 2 - 300 / 2, menu_container.size_y - 130 - 25, 300, 60, lambda: GAME.stop())
    end = StartButton(menu_container.size_x / 2 - 300 / 2, menu_container.size_y - 60 - 25, 300, 60, lambda: GAME.stop())

    add_hud_to_container(menu_container, Text(45,10, "Player1", (140,20,20), font.Font("./Tahoma.ttf", 28), False))
    add_hud_to_container(menu_container, Text(menu_container.size_x - 45*3,10, "Player2", (20,20,140), font.Font("./Tahoma.ttf", 28), False))
    add_hud_to_container(menu_container, Text(menu_container.draw_size_x / 2 - 90,50,"Game Over", (240,240,240), font.Font("./Tahoma.ttf", 40), False))
    add_hud_to_container(menu_container, Text(menu_container.draw_size_x / 2 - 100,150, str(player1.score), (180,60,60), font.Font("./Tahoma.ttf", 30), False))
    add_hud_to_container(menu_container, Text(menu_container.draw_size_x / 2 + 90,150, str(player2.score), (60,60,180), font.Font("./Tahoma.ttf", 30), False))
    add_hud_to_container(menu_container, Text(menu_container.draw_size_x / 2 - 3,150, "-", (230,230,230), font.Font("./Tahoma.ttf", 30), False))
    add_hud_to_container(menu_container, start)
    add_hud_to_container(menu_container, end)

    add_hud_to_game(GAME, menu_container)

    while GAME.running:
        menu_container.update(GAME)

        for ev in event.get():
            menu_container.event(ev)
    
        GAME.draw()
        GAME.clock.tick(GAME.fps)

    return 1 if start.hovered else 0

def choose_bar_menu(prefabs) -> tuple:
    menu = get_image("back_menu")
    menu_container = Container(GAME.size[0] / 2 - (menu.get_size()[0] * 4) / 2, GAME.size[1] / 1.5 - (menu.get_size()[1] * 4) / 1.5, transform.scale(menu, (menu.get_size()[0] * 4, menu.get_size()[1] * 4)))
    text = Container(GAME.size[0] / 2 - (menu.get_size()[0] * 2.5) / 2,60, transform.scale(get_image("back_menu"), (menu.get_size()[0] * 2.5,60)))
    back = ImageHud(0,0, get_image("background"))
    fps = Text(0,0, "0", (0,0,0), font.Font("./Tahoma.ttf", 18), False)
    animation_move = 1
    bot_choose = ContainerBool(125,188, (40, 40))
    bot_choose_2 = ContainerBool(menu_container.size_x - 135 * 1.25,188, (40, 40))
    size_choose = ContainerInt(130,100,(30,38), 9)
    size_choose_2 = ContainerInt(menu_container.size_x - 130 * 1.25,100,(30,38), 9)
    bar_choose = ContainerSprites(70,100,(7*5,19*5), [item for item in prefabs if type(item[0]).__name__ == "Bar"])
    bar_choose_2 = ContainerSprites(menu_container.size_x-70*1.5,100,(7*5,19*5), [item for item in prefabs if type(item[0]).__name__ == "Bar"])
    ball_choose = ContainerSprites(menu_container.size_x / 2 - (15*5)/2,110,(15*5,15*5), [item for item in prefabs if type(item[0]).__name__ == "Ball"])
    start = StartButton(menu_container.size_x / 2 - 300 / 2, menu_container.size_y - 60 - 25, 300, 60, lambda: GAME.stop())

    add_hud_to_container(menu_container, Text(45,10, "Player1", (140,20,20), font.Font("./Tahoma.ttf", 28), False))
    add_hud_to_container(menu_container, Text(menu_container.size_x - 45*3,10, "Player2", (20,20,140), font.Font("./Tahoma.ttf", 28), False))

    add_hud_to_container(menu_container, bot_choose)
    add_hud_to_container(menu_container, bot_choose_2)

    add_hud_to_container(menu_container, size_choose)
    add_hud_to_container(menu_container, size_choose_2)

    add_hud_to_container(menu_container, bar_choose)
    add_hud_to_container(menu_container, bar_choose_2)
    add_hud_to_container(menu_container, ball_choose)

    add_hud_to_container(menu_container, start)
    add_hud_to_container(text, Text(text.size_x / 2 - 55,text.size_y / 2 - 30/2 - 5, "101Pong", (10,10,12), font.Font("./Tahoma.ttf", 30), False))
    add_hud_to_game(GAME, back)
    add_hud_to_game(GAME, menu_container)
    add_hud_to_game(GAME, text)
    add_hud_to_game(GAME, fps)

    while GAME.running:
        GAME.update()
        GAME.draw()
        if (animation_move and back.draw_x + back.size_x > GAME.size[0] and back.draw_y + back.size_y > GAME.size[1]):
            back.move(back.draw_x - 3, back.draw_y - 3)
        elif (not animation_move and back.draw_x < 0 and back.draw_y < 0):
            back.move(back.draw_x + 3, back.draw_y + 3)
        else:
            animation_move = not animation_move
        show_fps(fps, GAME)
        GAME.clock.tick(GAME.fps)

    GAME.hud.clear()
    GAME.objects.clear()
    GAME.collection.clear()

    ball = [item for item in prefabs if type(item[0]).__name__ == "Ball"][ball_choose.actual][0].copy()
    bar_0 = [item for item in prefabs if type(item[0]).__name__ == "Bar"][bar_choose.actual][0].copy()
    bar_0.set_size(size_choose.actual)
    bar_0.is_bot = bot_choose.actual
    bar_1 = [item for item in prefabs if type(item[0]).__name__ == "Bar"][bar_choose_2.actual][0].copy()
    bar_1.set_size(size_choose_2.actual)
    bar_1.is_bot = bot_choose_2.actual

    return ball, bar_0, bar_1