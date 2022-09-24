from typing import Any, Tuple, Union, List
from collections import deque
from enum import Enum

BLUE = (16, 24)
PINK = (24, 16)
YELLOW = (32, 16)
CYAN = (80, 0)
RED = (0, 24)
PURPLE = (8, 24)
CHESS = (104, 32)
DEAD = (0, 16)
CLEAR = (8, 16)

class Direction(Enum):
    RightTurn = 1
    LeftTurn = -1

class Cycle:
    """ Cycle data structure """
    __slots__ = '__index', '__cycle', '__len'
    def __init__(self, *args):
        self.__index = 0
        self.__cycle: List[Any] = [*args]
        self.__len = len(args)
    
    def __str__(self):
        return f"Index={self.__index}, Len={self.__len}"
    
    def nexT(self) -> Any:
        if self.__index + 1 == self.__len:
            self.__index = 0
        else:
            self.__index += 1
        return self.__cycle[self.__index]
    
    def preV(self) -> Any:
        if self.__index - 1 == -1:
            self.__index = self.__len - 1
        else:
            self.__index -= 1
        return self.__cycle[self.__index]

class Block:
    """ Display of Tetris filled with Blocks """
    __slots__ = 'style', 'fill'
    def __init__(self, style: Tuple[int]=YELLOW, fill: int=0):
        self.style = style
        self.fill = fill

class Base_piece:
    """ Father of All-Pieces, All rotations of pieces store on 'Cycle' data-structure """
    __slots__ = 'limit_h', 'limit_w', 'x', 'y', 'limit_x', \
        'limit_y', 'current_rotation', 'pool_piece', 'style'
    def __init__(self):
        self.limit_h = 0 # height of piece
        self.limit_w = 0 # width of piece
        self.x = 0 # current loc_x
        self.y = 0 # current loc_y
        self.limit_x = 0 # maximum loc_x value that the piece can have on Display.
        self.limit_y = 0 # maximum loc_y value that the piece can have on Display.
        self.current_rotation: Tuple[Tuple[str]] = None
        self.pool_piece: Cycle = Cycle() # store all rotations of piece
        self.style: Tuple[int] = (0, 0)

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
    __slots__ = '_piece_21', '_piece_22', '__allowed'
    def __init__(self):
        super().__init__()
        self.style = (24, 0)
        self._piece_21 = (
            (1,),
            (1,),
            (1,),
            (1,),
        )
        self._piece_22 = (
            (1, 1, 1, 1,),
        )
        self.pool_piece = Cycle(
            self._piece_21,
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
    """ Piece Z with 2 rotation"""
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
ALL_PIECES: List[Piece] = [
    Piece_L,
    Piece_J,
    Piece_I,
    Piece_S,
    Piece_Z,
    Piece_T,
    Piece_O
]
queue_piece: List[Piece] = deque()
