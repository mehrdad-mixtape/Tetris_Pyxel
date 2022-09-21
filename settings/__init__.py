WIDTH = 176
HEIGHT = 240
SCALE = 8
FPS = 15 # Don't Change it! if you increase FPS, keyboard-inputs caching will be so fast
GAME_NAME = 'Pyxel TETRIS'
MAX_LEN_Q = 3
YES = True
NO = False
R = 'r'
L = 'l'
SCORE_FOR_EACH_ROW = 240
SCORE_FOR_EACH_PIECE = 30
XP_FOR_4LINE = 4
XP_FOR_3LINE = 2.5
XP_FOR_2LINE = 1.5
XP_FOR_1LINE = 1
KEY_BINDS = """
Key binds:

Arrows: MovePiece
-Down
-Right
-Left

Z: TurnRightRotate

X: TurnLeftRotate

M: ToggleMusic

ENTER:
-PlayGame
-Pause

BACKSpace:
-GameOver
"""
GAME_STATE_COLOR = {
    'START': 0,
    'READY': 2,
    'RUNNING': 3,
    'GAMEOVER': 8,
    'PAUSE': 9
}
DEAD = (0, 16)