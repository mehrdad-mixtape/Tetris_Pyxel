from typing import Tuple, List, Dict
from piece import PINK, YELLOW, BLUE

class Level:
    """ Levels of game """
    __slots__ = 'level_num', 'speed', 'line', 'color'
    def __init__(self, level_num: int, speed: float, line: int, color: Tuple[int]):
        self.level_num = level_num
        self.speed = speed
        self.line = line
        self.color = color
    
    def __str__(self):
        return f"{self.level_num=} {self.speed=} {self.line=} {self.color=}"

Statics_level: Dict[int, Tuple[float, int, Tuple[int]]] = { # level_number: (speed, line, color)
    0: (2, 15, YELLOW),
    1: (2.5, 25, YELLOW),
    2: (3, 35, YELLOW),
    3: (3.5, 45, YELLOW),
    4: (4, 55, YELLOW),
    5: (4.5, 65, PINK),
    6: (5, 75, PINK),
    7: (5.5, 85, PINK),
    8: (6.5, 95, PINK),
    9: (7.5, 105, PINK),
    10: (8.5, 115, BLUE),
    11: (10, 125, BLUE),
    12: (11.5, 135, BLUE),
    13: (13, 145, BLUE),
    14: (15, 160, BLUE),
}

LEVELS: List[Level] = [
    Level(
        n,
        Statics_level[n][0],
        Statics_level[n][1],
        Statics_level[n][2]
    ) for n in range(len(Statics_level))
]
Statics_level.clear()
