#!/bin/python3
# -*- coding: utf8 -*-

# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape

# Python Version 3.10
# Tetris:
# Based on Tetris DX on Gameboy-Color

# TODO: make music and sound effect for game
# TODO: clear animate
# TODO: fix piece cover other when move it left or right
# TODO: Score board

__repo__ = 'https://github.com/mehrdad-mixtape/'
__version__ = 'v1.0.1'

import pyxel
from enum import Enum
from time import time
from typing import Any, Callable, List
from random import choice
from piece import *
from levels import *
from settings import *

W = H = BIT = 8 # length of assets are 8pixel
pixel8 = lambda x: x * BIT
rpixel8 = lambda x: x // BIT
START = time()

def play_game(cls_game: Any):
    def __runner__() -> None:
        game = cls_game()
        game.run()
    return __runner__

def random_piece() -> Piece:
    """ Get random piece from queue """
    for _ in range(0, MAX_LEN_Q):
        if len(queue_piece) != MAX_LEN_Q:
            queue_piece.append(choice(ALL_PIECES)())
        else:
            break
    return queue_piece.popleft()

def in_range(start: int, stop: int, input: int) -> bool:
    return start <= input <= stop

def time_out(wait: float) -> Callable[[Any], Any]:
    def __decorator__(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        def __wrapper__(*arg, **kwargs) -> None:
            global START
            if time() - START > wait:
                START = time()
                func(*arg, **kwargs)
        return __wrapper__
    return __decorator__

# Game state labels
class Game_state(Enum):
    START = 'START'
    READY = 'READY'
    RUNNING = 'RUNNING'
    GAMEOVER = 'GAMEOVER'
    PAUSE = 'PAUSE'
    END = 'END'

class Display:
    """ Display is part of main place that store pieces """
    __slots__ = 'tile_map', 'u', 'v', 'w', 'h', '__walker', 'valid_w', \
        'valid_h', '_main_asset', '__pesudo_display', 'is_full'
    def __init__(self):
        self.tile_map = 0
        self.u = 0
        self.v = 0
        self.w = pixel8(24)
        self.h = pixel8(32)
        self.__walker = 19
        self.valid_w: Tuple[int] = (pixel8(3), pixel8(12)) # start, end
        self.valid_h: Tuple[int] = (pixel8(1), pixel8(20)) # start, end
        self._main_asset = CHESS
        self.__pesudo_display: List[List[Block]] = [
            [Block(asset=self._main_asset) for _ in range(10)] for _ in range(20)
        ]
        self.__pesudo_display.append([Block(asset=CYAN, fill=1) for _ in range(10)])
        self.is_full = False

    def __str__(self):
        """ Print pesudo display """
        dis = ''
        for row in self.__pesudo_display:
            for col in row:
                dis += f"{col.fill} "
            dis += '\n'
        return dis + '-------------------'

    @property
    def asset(self) -> None:
        # raise Exception('Display.asset is write-only')
        return self._main_asset
    @asset.setter
    def asset(self, new: Tuple[int]) -> None:
        self._main_asset = new
        for i, row in enumerate(self.__pesudo_display):
            for block in row:
                if i == 20:
                    break
                else:
                    if not block.fill:
                        block.asset = self._main_asset
    
    def draw(self, *, state: str='START', score: int=0, lines: int=0, level: Level=LEVELS[0]) -> None:
        """ Draw display """
        pyxel.bltm(0, 0, self.tile_map, self.u, self.v, self.w, self.h)
        for i, row in enumerate(self.__pesudo_display):
            for j, block in enumerate(row):
                pyxel.blt(pixel8(3 + j), pixel8(1 + i), 0, *block.asset, W, H)
        self.draw_text(text=state, X=127, Y=10, static=True, color=GAME_STATE_COLOR.get(state, 0))
        self.draw_text(text='Score:', X=127, Y=82, static=True, color=8)
        self.draw_text(text=f"{int(score)}", X=127, Y=93, static=True, color=1)
        self.draw_text(text='Lines:', X=127, Y=114, static=True, color=3)
        self.draw_text(text=f"{lines} / {level.line}", X=127, Y=125, static=True, color=1)
        self.draw_text(text='Level:', X=127, Y=146, static=True, color=9)
        self.draw_text(text=f"{level.level_num}", X=127, Y=157, static=True, color=1)
    
    def draw_piece(self, piece: Piece, loc_x: int, loc_y: int) -> None:
        """ Draw piece that falling on display """
        for i, row in enumerate(piece.current_rotation):
            for j, col in enumerate(row):
                if col:
                    pyxel.blt(loc_x + pixel8(i), loc_y + pixel8(j), 0, *piece.asset, W, H)

    def draw_next_piece(self, random: bool=False, kill_switch: bool=OFF) -> None:
        """ Draw the next piece in right corner on display """
        if not kill_switch:
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
        self.draw_next_piece(random=True)
        self.draw_text(Y=15)
        self.draw_text(text=KEY_BINDS, X=30, Y=20, static=True)

    def draw_ready(self) -> None:
        self.draw_next_piece(random=True)
        self.draw_text(text='Choose level', X=40, Y=35)
        self.draw_text(text=' With Mouse', X=40, Y=45)
        pyxel.rect(25, 64, 78, 7, 10)
        if in_range(64, 69, pyxel.mouse_y) and in_range(25, 98, pyxel.mouse_x):
            pyxel.rect(pyxel.mouse_x - 2, 64, 7, 7, 3)
        self.draw_text(text='0|1|2|3|4|5|6|7|8|9', X=26, Y=65, static=True, color=0)
        self.draw_text(text='Press SELECT', X=40, Y=80, static=True)

    def draw_pause(self) -> None:
        for i in range(20):
            for j in range(10):
                pyxel.blt(pixel8(j + 3), pixel8(i + 1), 0, 104, 32, W, H)
        self.draw_text(text='PAUSE', X=55, Y=15)
        self.draw_text(text=KEY_BINDS, X=30, Y=20, static=True)

    def draw_game_over(self) -> None:
        if self._main_asset == CHESS: color = 7
        else: color = 0
        self.draw_text(text='GAME OVER', X=47, Y=58)
        self.draw_text(text='Press Esc to Exit', X=30, Y=74, static=True, color=color)
        self.draw_text(text='Press ENTER to Play', X=27, Y=82, static=True, color=color)
    
    def draw_end(self) -> None:
        self.draw_text(text='End Game!', X=47)
        self.draw_text(text=' Dev by', X=47, Y=70, static=True, color=8)
        self.draw_text(text='mehrdad-mixtape', X=34, Y=78, static=True, color=8)
        self.draw_text(text='Press Esc to Exit', X=30, Y=88, static=True)
        self.draw_text(text='Press ENTER to Play', X=27, Y=96, static=True)

    def is_dead(self) -> bool:
        if self.__walker > -1:
            for j in range(0, 10):
                self.__pesudo_display[self.__walker][j].asset = DEAD
            self.__walker -= 1
            return False
        else:
            self.__walker = 19
            return True

    def draw_text(self, *, text: str="Pyxel Tetris", X: int=41, Y: int=60, static: bool=False, color: int=7) -> None:
        if static:
            pyxel.text(X, Y, text, color)
        else:
            pyxel.text(X, Y, text, pyxel.frame_count % 16)

    def piece_placer(self, piece: Piece) -> None:
        """ Piece is placing on piece.x + i & piece.y + j in display """
        for i, row in enumerate(piece.current_rotation):
            for j, col in enumerate(row):
                if col:
                    I = j - 1 + rpixel8(piece.y)
                    J = i - 3 + rpixel8(piece.x)
                    if I < 1:
                        self.is_full = True
                    self.__pesudo_display[I][J].asset = piece.asset
                    self.__pesudo_display[I][J].fill = col

    def piece_check_place(self, piece: Piece) -> bool:
        """ Check around of piece that wanna close to other pieces or walls or bottom"""
        flag = True
        for i, row in enumerate(piece.current_rotation):
            for j, col in enumerate(row):
                if col:
                    try:
                        I = j - 1 + rpixel8(piece.y) + 1
                        J = i - 3 + rpixel8(piece.x)
                        # Other pieces maybe fill loc_x + i and loc_y + j
                        if self.__pesudo_display[I][J].fill:
                            flag = False
                            break
                    except IndexError:
                        flag = False
                        break
        return flag

    def check_rows(self) -> Tuple[int]:
        """ Find rows that were filled with block """
        score_flag = False
        index_of_rows = []
        num_of_rows = 0
        score = 0
        xp = XP_FOR_1LINE
        for i, row in enumerate(self.__pesudo_display):
            for block in row:
                if i == 20:
                    score_flag = False
                    break
                else:
                    score_flag = True if block.fill else False
                if not score_flag:
                    break
            if score_flag:
                index_of_rows.append(self.__pesudo_display.index(row))

        num_of_rows = len(index_of_rows)

        if num_of_rows:
            match num_of_rows:
                case 4:
                    xp = XP_FOR_4LINE; #play_music(6)
                case 3:
                    xp = XP_FOR_3LINE; #play_music(5)
                case 2:
                    xp = XP_FOR_2LINE; #play_music(4)
                case 1:
                    xp = XP_FOR_1LINE; #play_music(3)
            for i in index_of_rows:
                row = self.__pesudo_display.pop(i)
                for block in row:
                    block.asset = self._main_asset
                    block.fill = 0
                self.__pesudo_display.insert(0, row) # Skip hidden rows and insert new row of blocks.
                score += SCORE_FOR_EACH_ROW * xp
        return score, num_of_rows

@play_game
class Tetris:
    """ Tetris class """
    __slots__ = 'current_state', 'score', 'lines', 'level', 'display', 'speed', 'dont_draw_next_piece', \
        'time_last_frame', 'dt', 'time_since_last_move', '_current_piece', 'is_piece_placed'
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, display_scale=SCALE, title=GAME_NAME, fps=FPS)
        pyxel.load("./assets/tetris.pyxres")
        pyxel.mouse(True)
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
        self._current_piece = None
        self.current_piece = random_piece()
        self.current_piece.x = pixel8(6 + (len(self.current_piece.current_rotation[0])) // 2)
        self.current_piece.y = self.display.valid_h[0] - pixel8(1)
        self.is_piece_placed = NO
        self.dont_draw_next_piece = NO

    @property    
    def current_piece(self) -> Piece:
        """ Get current_piece that is on display """
        return self._current_piece
    @current_piece.setter
    def current_piece(self, new_piece: Piece) -> None:
        """ Set new piece to current_piece and update important instance of piece """
        self._current_piece = new_piece
        self._current_piece.limit_h = pixel8(len(self._current_piece.current_rotation) - 1)
        self._current_piece.limit_w = pixel8(len(self._current_piece.current_rotation[0]) - 1)
        self._current_piece.limit_x = self.display.valid_w[1] - self._current_piece.limit_h
        self._current_piece.limit_y = self.display.valid_h[1] - self._current_piece.limit_w

    def update(self):
        """ Update frame """
        time_this_frame = time()
        self.dt = time_this_frame - self.time_last_frame
        self.time_last_frame = time_this_frame
        self.time_since_last_move += self.dt
        self.check_input()
        self.check_mouse()
        try:
            # Check game state:
            match self.current_state:
                case Game_state.RUNNING:
                    if self.time_since_last_move >= 1 / self.speed:
                        self.time_since_last_move = 0
                        self.move_piece()
                        score, lines = self.display.check_rows()
                        self.score += score
                        self.lines += lines
                        self.check_level()
                case Game_state.PAUSE: ...
        except KeyboardInterrupt: ...

    def draw(self):
        """ Draw frame """
        try:
            pyxel.cls(0)
            self.display.draw(
                state=self.current_state.value,
                score=self.score,
                lines=self.lines,
                level=self.level
            )
            self.display.draw_text(text='Select Start', X=68, Y=203, static=True, color=1)
            match self.current_state:
                case Game_state.START:
                    self.display.draw_start()
                case Game_state.READY:
                    self.display.draw_ready()
                case Game_state.PAUSE:
                    self.display.draw_pause()
                case Game_state.GAMEOVER:
                    self.display.draw_game_over()
                case Game_state.END:
                    self.display.draw_end()
                case Game_state.RUNNING:
                    if (not self.display.is_full) and (not self.is_piece_placed):
                        self.display.draw_piece(
                            self.current_piece,
                            self.current_piece.x,
                            self.current_piece.y
                        )
                    self.display.draw_next_piece(kill_switch=self.dont_draw_next_piece)
        except KeyboardInterrupt: ...

    def run(self):
        pyxel.run(self.update, self.draw)

    def admit_piece(self) -> None:
        """ Admit important Instance of piece """
        self.current_piece.limit_h = pixel8(len(self.current_piece.current_rotation) - 1)
        self.current_piece.limit_w = pixel8(len(self.current_piece.current_rotation[0]) - 1)
        self.current_piece.limit_x = self.display.valid_w[1] - self.current_piece.limit_h
        self.current_piece.limit_y = self.display.valid_h[1] - self.current_piece.limit_w

    def move_piece(self) -> None:
        """ Move down piece in each frame """
        # Move-down piece
        if not self.display.is_full:
            if not self.is_piece_placed:
                if not self.display.piece_check_place(self.current_piece):
                    self.display.piece_placer(self.current_piece)
                    self.is_piece_placed = YES
                else:
                    self.current_piece.y += 8

            else: # Next piece is going on
                self.score += SCORE_FOR_EACH_PIECE
                self.is_piece_placed = NO
                self.current_piece = random_piece()
                choice([self.current_piece.rotate, self.current_piece.rrotate, lambda: None])()
                self.admit_piece()
                self.current_piece.y = self.display.valid_h[0]
                self.current_piece.x = pixel8(6 + (len(self.current_piece.current_rotation[0])) // 2)
        else:
            self.dead_demo()

    def handle_move_left(self) -> None:
        """ Handle move left piece """
        if self.current_piece.x - W >= self.display.valid_w[0]:
            self.current_piece.x -= pixel8(1)
            if not self.display.piece_check_place(self.current_piece):
                self.current_piece.x += pixel8(1)

    def handle_move_right(self) -> None:
        """ Handle move right piece """
        if self.current_piece.x + W <= self.current_piece.limit_x:
            self.current_piece.x += pixel8(1)
            if not self.display.piece_check_place(self.current_piece):
                self.current_piece.x -= pixel8(1)
    
    def handle_move_down(self) -> None:
        """ Handle move down piece """
        self.score += SCORE_FOR_MOVE_DOWN
        if self.current_piece.y + H <= self.current_piece.limit_y:
            self.current_piece.y += pixel8(1)
            if not self.display.piece_check_place(self.current_piece):
                self.current_piece.y -= pixel8(1)

    def handle_rotate(self, mode: Direction) -> None:
        """
        Handle rotate operation for current piece.
        Critical Arias in Display:
            1. Right wall
            2. bottom
            3. between two pieces
            4. between piece and right wall
        """
        if mode == Direction.LeftTurn: self.current_piece.rrotate()
        elif mode == Direction.RightTurn: self.current_piece.rotate()
        
        self.admit_piece()

        temp_y = self.current_piece.limit_h + self.current_piece.y
        temp_x = self.current_piece.limit_w + self.current_piece.x

        # 1. if piece closed to bottom:
        if temp_y > self.current_piece.limit_y:
            if self.current_piece.y - pixel8(3) == self.current_piece.limit_y:
                self.current_piece.y -= pixel8(3)
            
            elif self.current_piece.y - pixel8(2) == self.current_piece.limit_y:
                self.current_piece.y -= pixel8(2)

            elif self.current_piece.y - pixel8(1) == self.current_piece.limit_y:
                self.current_piece.y -= pixel8(1)

        # 2. if piece closed to right wall:
        if temp_x > self.current_piece.limit_x:
            if self.current_piece.x - pixel8(3) == self.current_piece.limit_x:
                self.current_piece.x -= pixel8(3)
            
            elif self.current_piece.x - pixel8(2) == self.current_piece.limit_x:
                self.current_piece.x -= pixel8(2)

            elif self.current_piece.x - pixel8(1) == self.current_piece.limit_x:
                self.current_piece.x -= pixel8(1)

        # 3. If piece closed to other pieces or was between peaces or was between piece and wall:
        if not self.display.piece_check_place(self.current_piece):
            if mode == Direction.LeftTurn:
                self.current_piece.rotate()
            elif mode == Direction.RightTurn:
                self.current_piece.rrotate()
            self.current_piece.x = temp_x - self.current_piece.limit_w
            self.current_piece.y = temp_y - self.current_piece.limit_h

        self.admit_piece()

    def check_level(self) -> None:
        if self.lines >= self.level.line:
            if self.level.level_num + 1 != len(LEVELS):
                self.level = LEVELS[self.level.level_num + 1]
                self.display.asset = self.level.color
                self.speed = self.level.speed
            else:
                self.current_state = Game_state.END
    
    def set_level(self, level_number: int=0) -> None:
        self.level = LEVELS[level_number]
        self.display.asset = self.level.color
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
        self._current_piece = None
        self.current_piece = random_piece()
        self.current_piece.x = pixel8(6 + (len(self.current_piece.current_rotation[0])) // 2)
        self.current_piece.y = self.display.valid_h[0] - pixel8(1)
        self.is_piece_placed = NO
    
    def dead_demo(self) -> None:
        self.speed = DEAD_SPEED
        if self.display.is_dead():
            self.current_state = Game_state.GAMEOVER

    def toggle_music(self) -> None: ...

    # @time_out(0.035)
    def check_input(self) -> None:
        """ capture keyboard inputs """
        if pyxel.btn(pyxel.KEY_RETURN):
            match self.current_state:
                case Game_state.START:
                    self.current_state = Game_state.READY
                case Game_state.PAUSE:
                    self.current_state = Game_state.RUNNING
                case Game_state.RUNNING:
                    self.current_state = Game_state.PAUSE
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
                if self.dont_draw_next_piece == YES:
                    self.dont_draw_next_piece = NO
                else:
                    self.dont_draw_next_piece = YES

            if pyxel.btn(pyxel.KEY_Z):
                self.handle_rotate(Direction.RightTurn)
            
            if pyxel.btn(pyxel.KEY_X):
                self.handle_rotate(Direction.LeftTurn)

    def check_mouse(self) -> None:
        """ capture mouse inputs """
        # print(pyxel.mouse_x, pyxel.mouse_y)
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            match self.current_state:
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
                        if self.display.asset == CHESS:
                            self.set_level(level_number=0)
                        self.current_state = Game_state.RUNNING

                case Game_state.RUNNING: 
                    if ( # Press "Start" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(97, 112, pyxel.mouse_x)
                    ): self.current_state = Game_state.PAUSE
                    elif ( # Press "A" button
                        in_range(193, 206, pyxel.mouse_y)
                        and in_range(145, 157, pyxel.mouse_x)
                    ): self.current_piece.rotate()
                    elif ( # Press "B" button
                        in_range(209, 222, pyxel.mouse_y)
                        and in_range(122, 134, pyxel.mouse_x)
                    ): self.current_piece.rrotate()
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
                        if self.dont_draw_next_piece == YES:
                            self.dont_draw_next_piece = NO
                        else:
                            self.dont_draw_next_piece = YES

                case Game_state.PAUSE:
                    if ( # Press "Start" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(97, 112, pyxel.mouse_x)
                    ): self.current_state = Game_state.RUNNING

def main() -> None:
    Tetris()

if __name__ == '__main__':
    main()
