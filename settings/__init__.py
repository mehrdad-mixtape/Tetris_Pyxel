from libs import *

PYTHON_VERSION = '310'
WIDTH = 176
HEIGHT = 240
SCALE = 16
FPS = 20 # Don't Change it!
GAME_NAME = 'Pyxel TETRIS'
MAX_LEN_Q = 5
CLEAR_SPEED = FPS * 0.1
GAMEOVER_SPEED = FPS * 0.1
LEVELUP_SPEED = FPS * 0.1
COUNTDOWN_CLEAR_SPEED = FPS * 0.05
DRAW_WAIT = 5
YES = True
NO = False
ON = True
OFF = False
R = 'r'
L = 'l'
SCORE_FOR_EACH_ROW = 240
SCORE_FOR_EACH_PIECE = 30
SCORE_FOR_MOVE_DOWN = 1
LEVEL_LOC = (24, 68)
LEVEL_SELECTOR_SX = 24
LEVEL_SELECTOR_EX = 96
LEVEL_SELECTOR_Y = 78
LEVEL_SELECTOR = (112, 32)
XP_FOR_LINES: Dict[int, float] = {
    1: 2.0,
    2: 2.5,
    3: 3.0,
    4: 5.0,
}
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

     {}
"""
CHOOSE_LEVEL_BANNER_1 = """
  Choose Level
   ----------
   with <- ->
"""
CHOOSE_LEVEL_BANNER_2 = """
Press SELECT BUTTON

        Or

    Press ENTER
"""
GAMEOVER_BANNER = """
Press Esc to Exit

   Press ENTER

       Or

   Press START

  to Play Again
"""
END_BANNER = """
      End Game!
       -------
Dev by mehrdad-mixtape

   Press Esc to Exit

  Press ENTER to Play
"""
GAME_STATE_COLOR: Dict[str, int] = {
    'START': 0,
    'READY': 2,
    'RUNNING': 3,
    'CLEAR': 4, 
    'GAMEOVER': 8,
    'PAUSE': 9,
    'END': 12
}
CLEAR_LOC: List[Tuple[int]] = [
    (4, 5), (3, 6), (2, 7), (1, 8), (0, 9)
]
LEVELUP_LOC: List[int] = [
    1, 2, 3, 4
]
COUNTDOWN: List[Tuple[int]] = [
    (120, 24), (136, 24), (152, 24), (168, 24)
]
