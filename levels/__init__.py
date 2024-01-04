from libs import *
from piece import PINK, YELLOW, GREEN, RED, WHITE_BLUE

@dataclass(slots=True)
class Level:
    """ Levels of game """

    level_num: int
    speed: float
    line: int
    color: Tuple[int]


LEVELS: List[Level] = [
    Level(0,    2.0,    15,     YELLOW),
    Level(1,    2.5,    25,     YELLOW),
    Level(2,    3.0,    35,     YELLOW),
    Level(3,    3.5,    45,     YELLOW),
    Level(4,    4.0,    55,     YELLOW),

    Level(5,    5.0,    65,     PINK),
    Level(6,    5.5,    75,     PINK),
    Level(7,    6.0,    85,     PINK),
    Level(8,    6.5,    95,     PINK),
    Level(9,    7.0,    105,    PINK),

    Level(10,   8.0,    120,    WHITE_BLUE),
    Level(11,   8.5,    135,    WHITE_BLUE),
    Level(12,   9.0,    150,    WHITE_BLUE),
    Level(13,   9.5,    165,    WHITE_BLUE),
    Level(14,   10.0,   180,    WHITE_BLUE),

    Level(15,   12.0,   200,    GREEN),
    Level(16,   13.0,   220,    GREEN),
    Level(17,   14.0,   240,    GREEN),
    Level(18,   15.0,   260,    GREEN),
    Level(19,   16.0,   280,    GREEN),

    Level(20,   18.0,   300,    RED),
]
