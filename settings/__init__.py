from typing import List, Tuple, Dict

PYTHON_VERSION = '310'
WIDTH = 176
HEIGHT = 240
SCALE = 16
FPS = 12 # Don't Change it! if you increase FPS, keyboard-inputs caching will be so fast
GAME_NAME = 'Pyxel TETRIS'
MAX_LEN_Q = 3
CLEAR_SPEED = FPS * 2
GAMEOVER_SPEED = 30
YES = True
NO = False
ON = True
OFF = False
R = 'r'
L = 'l'
SCORE_FOR_EACH_ROW = 240
SCORE_FOR_EACH_PIECE = 30
SCORE_FOR_MOVE_DOWN = 1
XP_FOR_LINES = {
    1: 1,
    2: 1.5,
    3: 2.5,
    4: 4
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
"""
CHOOSE_LEVEL_BANNER_1 = """
Choose level
 ----------
 with Mouse
"""
CHOOSE_LEVEL_BANNER_2 = """
Press SELECT

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
    ---------
     Dev by
  mehrdad-mixtape

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
CLEAR_LOC: List[Dict[Tuple[int], bool]] = [
    {(0, 9): NO},
    {(0, 9): NO},
    {(0, 9): NO},
    {(1, 8): NO},
    {(2, 7): NO},
    {(3, 6): NO},
    {(4, 5): NO},
]
LEVELUP_LOC: List[int] = [
    1, 2, 3, 4
]
COUNTDOWN: List[Tuple[int]] = [
    (120, 24), (136, 24), (152, 24), (168, 24)
]
