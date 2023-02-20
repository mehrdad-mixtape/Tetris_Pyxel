#!/bin/python3.10
# -*- coding: utf8 -*-

# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Tetris_Pyxel

# Python Version 3.10
# Tetris:
# Based on Tetris DX on Gameboy-Color

# TODO: fix piece cover other when move it left or right
# TODO: Score board

__repo__ = 'https://github.com/mehrdad-mixtape/Tetris_Pyxel'
__version__ = 'v1.14.10'

import pyxel, sys
from enum import Enum
from time import time
from random import choice
from typing import Any, Callable
from itertools import cycle
from levels import LEVELS, Level
from piece import *
from settings import *

class Game_state(Enum): ...
class Remember: ...
class GameOver_animate(Remember): ...
class LevelUp_animate(Remember): ...
class CountDown_animate(Remember): ...
class Display: ...
class Tetris: ...

W = H = BIT = 8 # length of blocks are 8pixel
pixel8 = lambda x: x * BIT
rpixel8 = lambda x: x // BIT

def play_game(cls_game: Callable[[Any], Any]):
    def __runner__() -> None:
        with cls_game() as game: game()
    return __runner__

def random_piece() -> Piece:
    """ Get random piece from queue """
    for _ in range(0, MAX_LEN_Q):
        if len(queue_piece) != MAX_LEN_Q:
            queue_piece.append(choice(ALL_PIECES)())
        else: break
    return queue_piece.popleft()

def in_range(start: int, stop: int, input: int) -> bool:
    """ Check input that is in range or not """
    return start <= input <= stop

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

class Remember:
    def __init__(self, start: int, stop: int, reverse: bool=NO):
        if not reverse: self.__remember = cycle((i for i in range(start, stop)))
        else: self.__remember = cycle((i for i in reversed(range(start, stop))))
        self.current = start
    
    @property
    def remember(self) -> int:
        self.current = next(self.__remember)
        return self.current

    def do(self) -> Any: ...

class GameOver_animate(Remember):
    def __init__(self, display: Display):
        super().__init__(-21, 20, reverse=YES)
        self.__display = display

    def do(self) -> None:
        x = self.remember
        if  x > -1:
            for j in range(0, 10):
                self.__display[self.current][j].style = DEAD

        elif x == -21: return

        elif x <= -1:
            for j in range(0, 10):
                self.__display[-1 + self.current * -1][j].style = CHESS

class LevelUp_animate(Remember):
    def __init__(self):
        super().__init__(0, 5)

    def do(self) -> bool:
        if self.remember != len(LEVELUP_LOC):
            pyxel.text(47, 58 + pixel8(LEVELUP_LOC[self.current]), 'LevelUP!', pyxel.frame_count % 16)
            return NO
        else: return YES

class CountDown_animate(Remember):
    def __init__(self):
        super().__init__(0, 48)

    def do(self) -> bool:
        if in_range(0, FPS, self.remember): # Show 1
            pyxel.blt(56, 48, 0, *COUNTDOWN[0], 16, 24)
        elif in_range(FPS, FPS * 2, self.remember): # Show 2
            pyxel.blt(56, 48, 0, *COUNTDOWN[1], 16, 24)
        elif in_range(FPS * 2, FPS * 3, self.remember): # Show 3
            pyxel.blt(56, 48, 0, *COUNTDOWN[2], 16, 24)
        elif in_range(FPS * 3, FPS * 4, self.remember): # show GO!
            pyxel.blt(44, 84, 0, *COUNTDOWN[3], 40, 24)
        else: return YES
        return NO

class Display:
    """ Display is part of main place that store pieces """
    __slots__ = 'tile_map', 'u', 'v', 'w', 'h', 'candidate_rows', 'valid_w', 'valid_h', \
        '_main_style', '__pesudo_display', 'is_full', 'gameover_animate', 'levelup_animate', \
        'countdown_animate'
    def __init__(self):
        self.tile_map = 0
        self.u = 0
        self.v = 0
        self.w = pixel8(24)
        self.h = pixel8(32)
        self.candidate_rows: List[int] = []
        self.valid_w: Tuple[int] = (pixel8(3), pixel8(12)) # (start, end)
        self.valid_h: Tuple[int] = (pixel8(1), pixel8(20)) # (start, end)
        self._main_style = CHESS
        # __pesudo_display have 21-rows & 10-cols
        self.__pesudo_display: List[List[Block]] = [
            [Block(style=self._main_style) for _ in range(10)] for _ in range(20)
        ]
        self.__pesudo_display.append([Block(style=STONE, fill=1) for _ in range(10)])
        self.is_full = NO
        self.gameover_animate = GameOver_animate(self.__pesudo_display)
        self.levelup_animate = LevelUp_animate()
        self.countdown_animate = CountDown_animate()

    def __str__(self):
        """ Print pesudo display """
        dis = ''
        for row in self.__pesudo_display:
            for col in row:
                dis += f"{col.fill} "
            dis += '\n'
        return dis + '-------------------'

    def __call__(self):
        return self.__pesudo_display

    @property
    def style(self) -> Tuple[int]:
        # raise Exception('Display.style is write-only')
        return self._main_style
    @style.setter
    def style(self, new: Tuple[int]) -> None:
        self._main_style = new
        for i, row in enumerate(self.__pesudo_display):
            if i == 20: break # Skip Last row
            for block in row:
                if not block.fill:
                    block.style = self._main_style

    def draw(self, *, state: str='START', score: int=0, lines: int=0, level: Level=LEVELS[0]) -> None:
        """ Draw display """
        pyxel.bltm(0, 0, self.tile_map, self.u, self.v, self.w, self.h)
        for i, row in enumerate(self.__pesudo_display):
            for j, block in enumerate(row):
                pyxel.blt(pixel8(3 + j), pixel8(1 + i), 0, *block.style, W, H)
        self.draw_text(text=state, X=127, Y=10, static=True, color=GAME_STATE_COLOR.get(state, 0))
        self.draw_text(text='Score:', X=127, Y=82, static=True, color=8)
        self.draw_text(text=f"{int(score)}", X=123, Y=93, static=True, color=1)
        self.draw_text(text='Lines:', X=127, Y=114, static=True, color=3)
        self.draw_text(text=f"{lines} / {level.line}", X=123, Y=125, static=True, color=1)
        self.draw_text(text='Level:', X=127, Y=146, static=True, color=9)
        self.draw_text(text=f"{level.level_num}", X=123, Y=157, static=True, color=1)
        self.draw_text(text='Select Start', X=68, Y=203, static=True, color=1)
    
    def draw_piece(self, piece: Piece, loc_x: int, loc_y: int, style: Tuple[int]=None) -> None:
        """ Draw piece that falling on display """
        for i, row in enumerate(piece.current_rotation):
            if not sum(row): continue
            for j, col in enumerate(row):
                if col:
                    if style is None:
                        pyxel.blt(loc_x + pixel8(i), loc_y + pixel8(j), 0, *piece.style, W, H)
                    else: pyxel.blt(loc_x + pixel8(i), loc_y + pixel8(j), 0, *style, W, H)

    def draw_top_bar(self) -> None:
        """ Draw the top bar of display """
        for i in range(10): pyxel.blt(pixel8(i + 3), 0, 0, 120, 16, W, H)

    def draw_next_piece(self, *, random: bool=False, kill_switch: bool=OFF) -> None:
        """ Draw the next piece in right corner on display """
        if kill_switch: return
        if not random:
            piece = queue_piece[0]
        else:
            piece = random_piece()
        offset_x = len(piece.current_rotation)
        offset_y = len(piece.current_rotation[0])
        self.draw_piece(
            piece,
            pixel8(16 + (4 - offset_x) // 2),
            pixel8(4 + (4 - offset_y) // 2)
        )

    def draw_start(self) -> None:
        self.draw_text(Y=15)
        self.draw_text(text=KEY_BINDS.format(__version__), X=30, Y=20, static=True)

    def draw_ready(self) -> None:
        self.draw_text(text=CHOOSE_LEVEL_BANNER_1, X=40, Y=35)
        pyxel.rect(25, 64, 78, 7, 10)
        if in_range(64, 76, pyxel.mouse_y) and in_range(25, 98, pyxel.mouse_x):
            pyxel.rect(pyxel.mouse_x - 2, 64, 7, 7, 3)
        self.draw_text(text='0|1|2|3|4|5|6|7|8|9', X=26, Y=65, static=True, color=0)
        self.draw_text(text=CHOOSE_LEVEL_BANNER_2, X=40, Y=80, static=True)

    def draw_pause(self) -> None:
        self.draw_empty()
        self.draw_text(text='PAUSE\n-----', X=55, Y=15)
        self.draw_text(text=KEY_BINDS.format(__version__), X=30, Y=20, static=True)

    def draw_game_over(self) -> None:
        self.draw_text(text='GAME OVER\n---------', X=47, Y=58)
        self.draw_text(text=GAMEOVER_BANNER, X=30, Y=74, static=True)
    
    def draw_end(self) -> None:
        self.draw_text(text=END_BANNER, X=47)

    def draw_text(self, *, text: str="Pyxel Tetris\n------------", X: int=41, Y: int=60, static: bool=False, color: int=7) -> None:
        if static: pyxel.text(X, Y, text, color)
        else: pyxel.text(X, Y, text, pyxel.frame_count % 16)

    def draw_empty(self) -> None:
        for i in range(20):
            for j in range(10):
                pyxel.blt(pixel8(j + 3), pixel8(i + 1), 0, *CHESS, W, H)

    def piece_placer(self, piece: Piece) -> None:
        """ Piece is placing on piece.x + i & piece.y + j in display """
        if piece.y <= 0: return # This will help keep the pieces from appearing suddenly
        for i, row in enumerate(piece.current_rotation):
            for j, col in enumerate(row):
                if col:
                    I = j - 1 + rpixel8(piece.y)
                    J = i - 3 + rpixel8(piece.x)
                    if I < 1: self.is_full = YES
                    self.__pesudo_display[I][J].style = piece.style
                    self.__pesudo_display[I][J].fill = col

    def piece_check_place(self, piece: Piece) -> bool:
        """ Check around of piece that wanna close to other pieces or walls or bottom """
        if piece.y <= 0: return True # This will help keep the pieces from appearing suddenly
        for i, row in enumerate(piece.current_rotation):
            for j, col in enumerate(row):
                if col:
                    try:
                        I = j - 1 + rpixel8(piece.y) + 1
                        J = i - 3 + rpixel8(piece.x)
                        # Other pieces maybe fill loc_x + i and loc_y + j
                        if self.__pesudo_display[I][J].fill: return False
                    except IndexError: return False
        return True

    def check_rows(self) -> bool:
        """ Find rows that were filled with block """
        score_flag = False
        for i, row in enumerate(self.__pesudo_display):
            if i == 20: break # Skip Last row
            for block in row:
                score_flag = True if block.fill else False
                if not score_flag: break
            else:
                index_row = self.__pesudo_display.index(row)
                self.candidate_rows.append(index_row)
                score_flag = not score_flag
        return len(self.candidate_rows) != 0

    def clear_rows(self) -> Tuple[int]:
        loc = CLEAR_LOC.pop()
        for key in loc.keys():
            if not loc[key]: 
                loc[key] = YES
                for j in key:
                    for i in self.candidate_rows:
                        self.__pesudo_display[i][j].style = self.style
                        self.__pesudo_display[i][j].fill = 0
                CLEAR_LOC.insert(0, loc)
                return 0, 0
            else:
                CLEAR_LOC.append(loc)
                for loc in CLEAR_LOC:
                    for key in loc.keys():
                        loc[key] = NO
                num_of_lines = len(self.candidate_rows)
                score = num_of_lines * SCORE_FOR_EACH_ROW * XP_FOR_LINES[num_of_lines]
                for i in self.candidate_rows:
                    self.__pesudo_display.insert(0, self.__pesudo_display.pop(i))
                self.candidate_rows.clear()
                return score, num_of_lines

@play_game
class Tetris:
    """ Tetris class """
    __slots__ = '__current_state', '__previous_state', 'score', 'lines', 'level', 'display', \
        'speed', 'next_piece_flag', 'time_last_frame', 'dt', 'time_since_last_move', '__current_piece', \
        'is_piece_placed', 'is_level_up', 'is_new_game', 'force_update', 'is_tetris_moment', 'bypass'
    def __init__(self):
        # Game state:
        self.__previous_state = None
        self.__current_state = None
        self.current_state = Game_state.START
        # Game instance:
        self.score = 0
        self.lines = 0
        self.level = LEVELS[0]
        # Display of Game:
        self.display = Display()
        # Frame timing:
        self.speed = self.level.speed # Speed of game
        self.time_last_frame = time()
        self.dt = 0 # Delta time
        self.time_since_last_move = 0
        # Current piece:
        self.__current_piece = None
        self.current_piece = random_piece()
        self.init_loc_piece()
        # Game Flags:
        self.is_new_game = YES
        self.is_level_up = NO
        self.is_tetris_moment = NO
        self.is_piece_placed = NO
        self.force_update = NO
        self.next_piece_flag = NO
        self.bypass = NO

    def __call__(self):
        if FPS == 12:
            pyxel.init(WIDTH, HEIGHT, display_scale=SCALE, title=GAME_NAME, fps=FPS)
            pyxel.load("./assets/tetris.pyxres")
            pyxel.mouse(True)
            pyxel.run(self.update, self.draw)
        else: print(f"Please Don\'t Change the FPS!, Set {FPS=}")

    def __enter__(self):
        return self

    def __exit__(self, *handlers):
        try: del self
        except handlers: sys.exit()

    @staticmethod
    def __version__():
        return f"Tetris with Pyxel Retro Game Engine\nRepo: {__repo__}\nVersion: {__version__}"

    @property    
    def current_piece(self) -> Piece:
        """ Get current_piece that is on display """
        return self.__current_piece
    @current_piece.setter
    def current_piece(self, new_piece: Piece) -> None:
        """ Set new piece to current_piece and update important instance of piece """
        self.__current_piece = new_piece
        self.__current_piece.limit_h = pixel8(len(self.__current_piece.current_rotation[0]) - 1)
        self.__current_piece.limit_w = pixel8(len(self.__current_piece.current_rotation) - 1)
        self.__current_piece.limit_x = self.display.valid_w[1] - self.__current_piece.limit_w
        self.__current_piece.limit_y = self.display.valid_h[1] - self.__current_piece.limit_h

    @property
    def current_state(self) -> Game_state:
        return self.__current_state
    @current_state.setter
    def current_state(self, new_state: Game_state) -> None:
        self.__previous_state = self.__current_state
        self.__current_state = new_state

    @property
    def previous_state(self) -> Game_state:
        return self.__previous_state

    def update(self) -> None:
        """ Update game """
        try:
            time_this_frame = time()
            self.dt = time_this_frame - self.time_last_frame
            self.time_last_frame = time_this_frame
            self.time_since_last_move += self.dt
            self.check_input_keyboard()
            self.check_input_mouse()
            # Check game state:
            if (self.time_since_last_move >= 1 / self.speed) or self.force_update:
                self.time_since_last_move = 0
                # print(self.display)
                self.force_update = NO
                match self.current_state:
                    case Game_state.COUNTDOWN:
                        if not self.is_new_game:
                            self.current_state = Game_state.RUNNING

                    case Game_state.RUNNING:
                        if self.display.check_rows(): # Let's clear the rows
                            self.current_state = Game_state.CLEAR
                            self.speed = CLEAR_SPEED
                            if len(self.display.candidate_rows) == 4:
                                pyxel.play(1, 9) # tetris moment
                                self.is_tetris_moment = YES
                            else: pyxel.play(1, 7) # other moment
                        else: self.move_piece()
                        self.check_level()

                    case Game_state.CLEAR:
                        score, lines = self.display.clear_rows()
                        if score and lines:
                            self.display.style = self.level.color
                            self.speed = self.level.speed
                            self.current_state = Game_state.RUNNING
                            self.score += score + self.level.line * 50
                            self.lines += lines
                            self.is_tetris_moment = NO
                            self.move_piece() # prevent to show blink animate

                    case Game_state.LEVELUP:
                        if self.is_level_up:
                            self.set_level(level_number=self.level.level_num + 1)
                            self.current_state = Game_state.RUNNING
                            self.is_level_up = NO

        except KeyboardInterrupt: ...

    def draw(self) -> None:
        """ Draw frame """
        pyxel.cls(0)
        try:
            self.display.draw(
                state=self.current_state.value,
                score=self.score,
                lines=self.lines,
                level=self.level
            )
            match self.current_state:
                case Game_state.START:
                    self.display.draw_next_piece(random=True)
                    self.display.draw_start()

                case Game_state.READY:
                    self.display.draw_next_piece(random=True)
                    self.display.draw_ready()

                case Game_state.COUNTDOWN:
                    self.display.draw_empty()
                    if self.display.countdown_animate.do():
                        self.is_new_game = NO
                        self.force_update = YES

                case Game_state.RUNNING:
                    self.display.draw_next_piece(kill_switch=self.next_piece_flag)
                    # if not self.display.is_full:
                    if not self.is_piece_placed:
                        self.display.draw_piece(
                            self.current_piece,
                            self.current_piece.x,
                            self.current_piece.y
                        )
                    else: # show blink animate when piece was placed
                        self.display.draw_piece(
                            self.current_piece,
                            self.current_piece.x,
                            self.current_piece.y,
                            style=WHITE
                        )
                        self.force_update = YES

                case Game_state.CLEAR:
                    if self.is_tetris_moment: self.display.style = next(COLORS)
                    self.display.draw_next_piece(kill_switch=self.next_piece_flag)

                case Game_state.LEVELUP:
                    self.display.draw_next_piece(kill_switch=self.next_piece_flag)
                    self.display.draw_piece(
                        self.current_piece,
                        self.current_piece.x,
                        self.current_piece.y
                    )
                    if self.display.levelup_animate.do(): self.is_level_up = YES
                
                case Game_state.PAUSE:
                    self.display.draw_pause()
                
                case Game_state.GAMEOVER:
                    self.display.gameover_animate.do()
                    self.display.draw_game_over()

                case Game_state.END:
                    self.display.draw_end()
            
            self.display.draw_top_bar()
        except KeyboardInterrupt: ...

    def admit_piece(self) -> None:
        """ Admit important Instance of piece """
        self.current_piece.limit_h = pixel8(len(self.current_piece.current_rotation[0]) - 1)
        self.current_piece.limit_w = pixel8(len(self.current_piece.current_rotation) - 1)
        self.__current_piece.limit_x = self.display.valid_w[1] - self.__current_piece.limit_w
        self.current_piece.limit_y = self.display.valid_h[1] - self.current_piece.limit_h

    def init_loc_piece(self) -> None:
        if self.current_piece.name == 'I':
            self.current_piece.y = self.display.valid_h[0] - pixel8(4)
            self.current_piece.x = pixel8(4 + (len(self.current_piece.current_rotation[0])) // 2)
        else:
            self.current_piece.y = self.display.valid_h[0] - pixel8(3)
            self.current_piece.x = pixel8(6 + (len(self.current_piece.current_rotation[0])) // 2)

    def move_piece(self) -> None:
        """ Move down piece in each frame """
        # Move-down piece
        if not self.display.is_full:
            if not self.is_piece_placed:
                # piece placed
                if not self.display.piece_check_place(self.current_piece):
                    self.display.piece_placer(self.current_piece)
                    self.is_piece_placed = YES
                    pyxel.play(0, 5)
                # piece moved
                else: self.current_piece.y += pixel8(1)

            else: # Next piece is going on
                self.score += SCORE_FOR_EACH_PIECE
                self.is_piece_placed = NO
                self.current_piece = random_piece()
                self.admit_piece()
                self.init_loc_piece()
        else:
            self.current_state = Game_state.GAMEOVER
            pyxel.play(0, 6)

    def handle_move_left(self) -> None:
        """ Handle move left piece """
        if self.current_piece.x - W >= self.display.valid_w[0]:
            self.current_piece.x -= W
            if not self.display.piece_check_place(self.current_piece):
                self.current_piece.x += W
            else: pyxel.play(0, 2)

    def handle_move_right(self) -> None:
        """ Handle move right piece """
        if self.current_piece.x + W <= self.current_piece.limit_x:
            self.current_piece.x += W
            if not self.display.piece_check_place(self.current_piece):
                self.current_piece.x -= W
            else: pyxel.play(0, 2)
    
    def handle_move_down(self) -> None:
        """ Handle move down piece """
        if self.bypass:
            if self.current_piece.y + H <= self.current_piece.limit_y:
                self.current_piece.y += pixel8(1)
                if not self.display.piece_check_place(self.current_piece):
                    self.current_piece.y -= pixel8(1)
                else: self.score += SCORE_FOR_MOVE_DOWN
        else:
            if (
                self.current_piece.y + H <= self.current_piece.limit_y
                and self.display.piece_check_place(self.current_piece)
            ):
                self.current_piece.y += pixel8(1)
                self.score += SCORE_FOR_MOVE_DOWN

    def handle_rotate(self, mode: Direction) -> None:
        """
        Handle rotate operation for current piece.
        Critical Arias in Display:
            1. Right wall
            2. bottom
            3. between two pieces
            4. between piece and right wall
        """
   
        for _ in range(len(self.current_piece.pool_piece)):
            if mode == Direction.LeftTurn: self.current_piece.rrotate()
            elif mode == Direction.RightTurn: self.current_piece.rotate()

            self.admit_piece()

            temp_y = self.current_piece.limit_h + self.current_piece.y
            temp_x = self.current_piece.limit_w + self.current_piece.x

            # 1. if piece closed to bottom:
            # self.current_piece.y of previous piece
            # self.current_piece.limit_y of rotated piece
            offset_y = 0
            if temp_y > self.current_piece.limit_y:
                if self.current_piece.y - pixel8(3) == self.current_piece.limit_y:
                    offset_y = pixel8(3)
                    self.current_piece.y -= offset_y
                
                elif self.current_piece.y - pixel8(2) == self.current_piece.limit_y:
                    offset_y = pixel8(2)
                    self.current_piece.y -= offset_y

                elif self.current_piece.y - pixel8(1) == self.current_piece.limit_y:
                    offset_y = pixel8(1)
                    self.current_piece.y -= offset_y

            # 2. if piece closed to right wall:
            # self.current_piece.x of previous piece
            # self.current_piece.limit_x of rotated piece
            offset_x = 0
            if temp_x > self.current_piece.limit_x:
                if self.current_piece.x - pixel8(3) == self.current_piece.limit_x:
                    offset_x = pixel8(3)
                    self.current_piece.x -= offset_x

                elif self.current_piece.x - pixel8(2) == self.current_piece.limit_x:
                    offset_x = pixel8(2)
                    self.current_piece.x -= offset_x

                elif self.current_piece.x - pixel8(1) == self.current_piece.limit_x:
                    offset_x = pixel8(1)
                    self.current_piece.x -= offset_x

            # 3. If piece closed to other pieces or was between peaces or was between piece and wall:
            if self.display.piece_check_place(self.current_piece):
                pyxel.play(0, 3)
                break
            else:
                if offset_x: self.current_piece.x += offset_x
                if offset_y: self.current_piece.y += offset_y

        self.admit_piece()

    def check_level(self) -> None:
        if self.lines >= self.level.line:
            if self.level.level_num + 1 != len(LEVELS):
                self.current_state = Game_state.LEVELUP
                pyxel.play(2, 8)
            else: self.current_state = Game_state.END
    
    def set_level(self, level_number: int=0) -> None:
        self.level = LEVELS[level_number]
        self.display.style = self.level.color
        self.speed = self.level.speed

    def new_game(self) -> None:
        # Game state:
        self.current_state = Game_state.START
        # Game instance:
        self.score = 0
        self.lines = 0
        self.level = LEVELS[0]
        # Display of Game:
        self.display = Display()
        # Frame timing:
        self.speed = self.level.speed # Speed of game
        self.time_last_frame = time()
        self.dt = 0 # Delta time
        self.time_since_last_move = 0
        # Current Piece:
        self.__current_piece = None
        self.current_piece = random_piece()
        self.init_loc_piece()
        # Game Flags:
        self.is_new_game = YES
        self.is_level_up = NO
        self.is_tetris_moment = NO
        self.is_piece_placed = NO
        self.force_update = NO
        self.next_piece_flag = NO
        self.bypass = NO

    def toggle_music(self) -> None: ...

    def check_input_keyboard(self) -> None:
        """ Capture keyboard inputs """
        if pyxel.btn(pyxel.KEY_RETURN):
            match self.current_state:
                case Game_state.START:
                    self.current_state = Game_state.READY
                    pyxel.play(0, 10)

                case Game_state.READY:
                    # If Player didn't select level, by default level will be 0
                    if self.display.style == CHESS:
                        self.set_level()
                    self.current_state = Game_state.COUNTDOWN
                    pyxel.play(0, 10)

                case Game_state.RUNNING:
                    self.current_state = Game_state.PAUSE
                    pyxel.play(0, 0)

                case Game_state.PAUSE:
                    self.current_state = Game_state.RUNNING
                    pyxel.play(0, 0)

                case Game_state.GAMEOVER | Game_state.END:
                    self.new_game()
        
        if pyxel.btnp(pyxel.KEY_M):
            self.toggle_music()

        if pyxel.btn(pyxel.KEY_BACKSPACE):
            self.current_state = Game_state.GAMEOVER

        if self.current_state == Game_state.RUNNING:
            # Do piece close to right wall?
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.handle_move_right()

            # Do piece close to left wall?
            if pyxel.btn(pyxel.KEY_LEFT):
                self.handle_move_left()
            
            # Do piece close to bottom?
            if pyxel.btn(pyxel.KEY_DOWN):
                self.handle_move_down()

            if pyxel.btn(pyxel.KEY_UP):
                if self.next_piece_flag == YES:
                    self.next_piece_flag = NO
                else:
                    self.next_piece_flag = YES
                pyxel.play(0, 4)

            if pyxel.btn(pyxel.KEY_Z):
                self.handle_rotate(Direction.RightTurn)
            
            if pyxel.btn(pyxel.KEY_X):
                self.handle_rotate(Direction.LeftTurn)

    def check_input_mouse(self) -> None:
        """ Capture mouse inputs """
        # print(pyxel.mouse_x, pyxel.mouse_y)
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            match self.current_state:
                case Game_state.START: 
                    if ( # Press "Start" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(97, 112, pyxel.mouse_x)
                    ):
                        self.current_state = Game_state.READY
                        pyxel.play(0, 10)
                    if ( # Cheat for move down piece
                        in_range(24, 31, pyxel.mouse_y)
                        and in_range(120, 127, pyxel.mouse_x)
                    ):
                        self.bypass = YES

                case Game_state.READY:
                    if in_range(64, 69, pyxel.mouse_y): # Ready display for choose level
                        if in_range(24, 31, pyxel.mouse_x): # Select level 0
                            self.set_level(level_number=0)
                        elif in_range(32, 39, pyxel.mouse_x): # Select level 1
                            self.set_level(level_number=1)
                        elif in_range(40, 47, pyxel.mouse_x): # Select level 2
                            self.set_level(level_number=2)
                        elif in_range(48, 55, pyxel.mouse_x): # Select level 3
                            self.set_level(level_number=3)
                        elif in_range(56, 63, pyxel.mouse_x): # Select level 4
                            self.set_level(level_number=4)
                        elif in_range(64, 71, pyxel.mouse_x): # Select level 5
                            self.set_level(level_number=5)
                        elif in_range(72, 79, pyxel.mouse_x): # Select level 6
                            self.set_level(level_number=6)
                        elif in_range(80, 87, pyxel.mouse_x): # Select level 7
                            self.set_level(level_number=7)
                        elif in_range(88, 95, pyxel.mouse_x): # Select level 8
                            self.set_level(level_number=8)
                        elif in_range(96, 103, pyxel.mouse_x): # Select level 9
                            self.set_level(level_number=9)
                    elif ( # Press "Select" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(72, 87, pyxel.mouse_x)
                    ):
                        # If Player didn't select level, by default level will be 0
                        if self.display.style == CHESS:
                            self.set_level(level_number=0)
                        self.current_state = Game_state.RUNNING
                        pyxel.play(0, 10)

                case Game_state.RUNNING: 
                    if ( # Press "Start" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(97, 112, pyxel.mouse_x)
                    ):
                        self.current_state = Game_state.PAUSE
                        pyxel.play(0, 0)
                    elif ( # Press "A" button
                        in_range(193, 206, pyxel.mouse_y)
                        and in_range(145, 157, pyxel.mouse_x)
                    ): self.handle_rotate(Direction.RightTurn)
                    elif ( # Press "B" button
                        in_range(209, 222, pyxel.mouse_y)
                        and in_range(122, 134, pyxel.mouse_x)
                    ): self.handle_rotate(Direction.LeftTurn)
                    elif ( # Press "D-pad left" button
                        in_range(201, 214, pyxel.mouse_y)
                        and in_range(17, 30, pyxel.mouse_x)
                    ): self.handle_move_left()
                    elif ( # Press "D-pad right" button
                        in_range(201, 214, pyxel.mouse_y)
                        and in_range(48, 62, pyxel.mouse_x)
                    ): self.handle_move_right()
                    elif ( # Press "D-pad down" button
                        in_range(216, 230, pyxel.mouse_y)
                        and in_range(33, 46, pyxel.mouse_x)
                    ): self.handle_move_down()
                    elif ( # Press "D-pad up" button
                        in_range(185, 199, pyxel.mouse_y)
                        and in_range(33, 45, pyxel.mouse_x)
                    ):
                        if self.next_piece_flag == YES:
                            self.next_piece_flag = NO
                        else:
                            self.next_piece_flag = YES
                        pyxel.play(0, 4)

                case Game_state.PAUSE:
                    if ( # Press "Start" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(97, 112, pyxel.mouse_x)
                    ):
                        self.current_state = Game_state.RUNNING
                        pyxel.play(0, 0)

                case Game_state.GAMEOVER | Game_state.END:
                    if ( # Press "Start" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(97, 112, pyxel.mouse_x)
                    ): self.new_game()

def main() -> None:
    Tetris()

if __name__ == '__main__':
    main()
