from .libs import *

GAME: object = Game((1200, 600), "101pong", 16, 60, True, (50,50,50), True)
CAMERA: object = Camera(0, 0, 12)
SCORE_SOUND: object = mixer.Sound("score.mp3")