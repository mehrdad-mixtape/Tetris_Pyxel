import sys
import random
import argparse
import http.server
import socketserver
import pyxel
from typing import Any, Tuple, List, Dict, Set, \
    Callable, Union, Generator
from collections import deque
from dataclasses import dataclass
from itertools import cycle
from enum import Enum
from time import time

class Display: ...
class Tetris: ...

# Game state labels
class Game_state(Enum):
    START = 'START'
    READY = 'READY'
    COUNTDOWN = 'TETRIS'
    RUNNING = 'RUNNING'
    CLEAR = 'CLEAR'
    LEVELUP = 'LEVELUP'
    GAMEOVER = 'GAMEOVER'
    PAUSE = 'PAUSE'
    END = 'END'


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


    @property
    def len(self):
        return self.__len


    def nexT(self) -> Any:
        if self.__index + 1 == self.__len:
            self.__index = 0
        else: self.__index += 1
        return self.__cycle[self.__index]


    def preV(self) -> Any:
        if self.__index - 1 == -1:
            self.__index = self.__len - 1
        else: self.__index -= 1
        return self.__cycle[self.__index]


class Remember:
    """ Remember help to save last state of animates of game """

    def __init__(self, start: int, stop: int, reverse: bool=False):
        if not reverse: self.__remember = cycle((i for i in range(start, stop)))
        else: self.__remember = cycle((i for i in reversed(range(start, stop))))
        self.current = start


    @property
    def remember(self) -> int:
        self.current = next(self.__remember)
        return self.current


def play_game(cls_game: Callable[[Any], Any]):
    def __runner__() -> None:
        with cls_game() as game: game()

    return __runner__


def in_range(start: int, stop: int, input_: int) -> bool:
    """ Check input that is in range or not """

    return start <= input_ <= stop
