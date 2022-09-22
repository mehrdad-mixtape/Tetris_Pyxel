PYTHON_VERSION = '310'
WIDTH = 176
HEIGHT = 240
SCALE = 32
FPS = 12 # Don't Change it! if you increase FPS, keyboard-inputs caching will be so fast
GAME_NAME = 'Pyxel TETRIS'
MAX_LEN_Q = 3
YES = True
NO = False
ON = True
OFF = False
R = 'r'
L = 'l'
SCORE_FOR_EACH_ROW = 240
SCORE_FOR_EACH_PIECE = 30
SCORE_FOR_MOVE_DOWN = 1
XP_FOR_4LINE = 4
XP_FOR_3LINE = 2.5
XP_FOR_2LINE = 1.5
XP_FOR_1LINE = 1
KEY_BINDS = """
Key binds:

Arrows: Move piece
-Down
-Right
-Left

UpArrow:
-Hide next piece
-Show next piece

Z: Rotate to right
X: Rotate to left
M: Toggle music

ENTER:
-Play game
-Pause

BACKSpace:
-GameOver
"""
GAME_STATE_COLOR = {
    'START': 0,
    'READY': 2,
    'RUNNING': 3,
    'GAMEOVER': 8,
    'PAUSE': 9,
    'END': 12
}
DEAD_SPEED = 30
