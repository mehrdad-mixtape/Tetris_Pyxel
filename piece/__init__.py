from libs import *
from settings import MAX_LEN_Q

BLACK = (0, 0)
DARK_BLUE = (48, 24)
PURPLE = (8, 24)
DARK_GREEN = (24, 24)
BROWN = (32, 24)
BLUE = (16, 24)
WHITE_BLUE = (40, 24)
WHITE = (72, 16)
RED = (0, 24)
ORANGE = (48, 24)
YELLOW = (16, 32)
GREEN = (0, 32)
MID_BLUE = (48, 32)
GRAY = (24, 32)
PINK = (8, 32)
WHITE_PINK = (32, 32)

COLORS = cycle(
    [
        BLACK, DARK_BLUE, PURPLE, DARK_GREEN,
        BROWN, BLUE, WHITE_BLUE, WHITE,
        RED, ORANGE, YELLOW, GREEN,
        MID_BLUE, GRAY, PINK, WHITE_PINK, 
    ]
)

CYAN = (80, 0)
CHESS = (104, 32)
DEAD = (0, 16)
STONE = (16, 16)

@dataclass(slots=True)
class Block:
    """ Display of Tetris filled with Blocks """

    style: Tuple[int] = YELLOW
    fill: int = 0


@dataclass(slots=True)
class Base_piece:
    """ Father of All-Pieces, All rotations of pieces store on 'Cycle' data-structure """

    limit_h: int = 0 # height of piece
    limit_w: int = 0 # width of piece
    x: int = 0 # current loc_x
    y: int = 0 # current loc_y
    limit_x: int = 0 # maximum loc_x value that the piece can have on Display.
    limit_y: int = 0 # maximum loc_y value that the piece can have on Display.
    current_rotation: Tuple[Tuple[str]] = None
    pool_piece: Cycle = None # store all rotations of piece.
    style: Tuple[int] = (0, 0)


    def rotate(self) -> None:
        self.current_rotation = self.pool_piece.nexT()


    def rrotate(self) -> None:
        self.current_rotation = self.pool_piece.preV()


class Piece_L(Base_piece):
    """ Piece L with 4 rotation """

    __slots__ = '_piece_01', '_piece_02', '_piece_03', '_piece_04'

    def __init__(self):
        super().__init__()
        self.style = (8, 0)
        self._piece_01 = (
            (1, 1, 1,),
            (1, 0, 0,),
        )
        self._piece_02 = (
            (1, 1),
            (0, 1),
            (0, 1),
        )
        self._piece_03 = (
            (0, 0, 1,),
            (1, 1, 1,),
        )
        self._piece_04 = (
            (1, 0,),
            (1, 0,),
            (1, 1,),
        )
        self.pool_piece = Cycle(
            self._piece_01,
            self._piece_02,
            self._piece_03,
            self._piece_04,
        )
        self.current_rotation = self._piece_01


    def __str__(self):
        return """
        Piece L:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██████▒▒████▒▒▒▒▒▒██▒▒██▒▒▒▒
        ▒▒██▒▒▒▒▒▒▒▒██▒▒██████▒▒██▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒████▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """


class Piece_J(Base_piece):
    """ Piece J with 4 rotation """

    __slots__ = '_piece_11', '_piece_12', '_piece_13', '_piece_14'

    def __init__(self):
        super().__init__()
        self.style = (24, 8)
        self._piece_11 = (
            (1, 0, 0,),
            (1, 1, 1,),
        )
        self._piece_12 = (
            (1, 1,),
            (1, 0,),
            (1, 0,),
        )
        self._piece_13 = (
            (1, 1, 1,),
            (0, 0, 1,),
        )
        self._piece_14 = (
            (0, 1,),
            (0, 1,),
            (1, 1,),
        )
        self.pool_piece = Cycle(
            self._piece_11,
            self._piece_12,
            self._piece_13,
            self._piece_14,
        )
        self.current_rotation = self._piece_11


    def __str__(self):
        return """
        Piece J:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒████▒▒██████▒▒▒▒██▒▒
        ▒▒██████▒▒██▒▒▒▒▒▒▒▒██▒▒▒▒██▒▒
        ▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒████▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """


class Piece_I(Base_piece):
    """ Piece I with 2 rotation """

    __slots__ = '_piece_21', '_piece_22', '_piece_23'

    def __init__(self):
        super().__init__()
        self.style = (24, 0)
        self._piece_21 = (
            (0, 1, 0, 0,),
            (0, 1, 0, 0,),
            (0, 1, 0, 0,),
            (0, 1, 0, 0,),
        )
        self._piece_22 = (
            (1, 1, 1, 1,),
        )
        self._piece_23 = (
            (0, 0, 1, 0,),
            (0, 0, 1, 0,),
            (0, 0, 1, 0,),
            (0, 0, 1, 0,),
        )
        self.pool_piece = Cycle(
            self._piece_21,
            self._piece_22,
            self._piece_23,
            self._piece_22,
        )
        self.current_rotation = self._piece_21


    def __str__(self):
        return """
        Piece I:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒████████▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """


class Piece_S(Base_piece):
    """ Piece S with 2 rotation """

    __slots__ = '_piece_31', '_piece_32'

    def __init__(self):
        super().__init__()
        self.style = (8, 8)
        self._piece_31 = (
            (1, 0,),
            (1, 1,),
            (0, 1,),
        )
        self._piece_32 = (
            (0, 1, 1,),
            (1, 1, 0,),
        )
        self.pool_piece = Cycle(
            self._piece_31,
            self._piece_32,
        )
        self.current_rotation = self._piece_31


    def __str__(self):
        return """
        Piece S:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒██▒▒▒▒▒▒████▒▒
        ▒▒████▒▒████▒▒▒▒
        ▒▒▒▒██▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """


class Piece_Z(Base_piece):
    """ Piece Z with 2 rotation """

    __slots__ = '_piece_41', '_piece_42'

    def __init__(self):
        super().__init__()
        self.style = (0, 8)
        self._piece_41 = (
            (0, 1,),
            (1, 1,),
            (1, 0,),
        )
        self._piece_42 = (
            (1, 1, 0,),
            (0, 1, 1,),
        )
        self.pool_piece = Cycle(
            self._piece_41,
            self._piece_42,
        )
        self.current_rotation = self._piece_41


    def __str__(self):
        return """
        Piece Z:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒██▒▒████▒▒▒▒
        ▒▒████▒▒▒▒████▒▒
        ▒▒██▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """


class Piece_T(Base_piece):
    """ Piece T with 4 rotation """

    __slots__ = '_piece_51', '_piece_52', '_piece_53', '_piece_54'

    def __init__(self):
        super().__init__()
        self.style = (16, 0)
        self._piece_51 = (
            (0, 1, 0,),
            (1, 1, 1,),
        )
        self._piece_52 = (
            (1, 0,),
            (1, 1,),
            (1, 0,),
        )
        self._piece_53 = (
            (1, 1, 1,),
            (0, 1, 0,),
        )
        self._piece_54 = (
            (0, 1,),
            (1, 1,),
            (0, 1,),
        )
        self.pool_piece = Cycle(
            self._piece_51,
            self._piece_52,
            self._piece_53,
            self._piece_54,
        )
        self.current_rotation = self._piece_51


    def __str__(self):
        return """
        Piece T:
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        ▒▒▒▒██▒▒▒▒██▒▒▒▒██████▒▒▒▒██▒▒
        ▒▒██████▒▒████▒▒▒▒██▒▒▒▒████▒▒
        ▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒
        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
        """


class Piece_O(Base_piece):
    """ Piece O with 1 rotation """

    __slots__ = '_piece_61'

    def __init__(self):
        super().__init__()
        self.style = (16, 8)
        self._piece_61 = (
            (1, 1,),
            (1, 1,),
        )
        self.pool_piece = Cycle(
            self._piece_61,
        )
        self.current_rotation = self._piece_61


    def __str__(self):
        return """
        Piece O:
        ▒▒▒▒▒▒▒▒
        ▒▒████▒▒
        ▒▒████▒▒
        ▒▒▒▒▒▒▒▒
        """


Piece = Union[Piece_L, Piece_J, Piece_I, Piece_S, Piece_Z, Piece_T, Piece_O]

ALL_PIECES: List[Piece] = [Piece_I, Piece_L, Piece_J, Piece_S, Piece_Z, Piece_T, Piece_O]

queue_piece: deque[Piece] = deque(maxlen=MAX_LEN_Q)
for _ in range(MAX_LEN_Q - 1):
    random.shuffle(ALL_PIECES)
    queue_piece.appendleft(
        ALL_PIECES[
            random.randint(100, 900) % len(ALL_PIECES)
        ]())
