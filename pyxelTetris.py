#!/bin/python3.10
# -*- coding: utf8 -*-

# Developed by mehrdad-mixtape https://github.com/mehrdad-mixtape/Tetris_Pyxel

# Python Version 3.10
# Tetris:
# Based on Tetris DX on Gameboy-Color

# TODO: Cache the piece
# TODO: Fix piece cover piece when move it left or right
# TODO: Score board
# TODO: Implement center rotation

__repo__ = 'https://github.com/mehrdad-mixtape/Tetris_Pyxel'
__version__ = 'v1.20.0'

from libs import *
from levels import *
from piece import *
from settings import *

W = H = BIT = 8 # length of blocks are 8pixel
pixel8 = lambda x: x * BIT
rpixel8 = lambda x: x // BIT


def random_piece() -> Generator[Piece, None, None]:
    """ Get random piece from queue """

    while True:
        new_piece: Piece = random.choice(ALL_PIECES)()
        if new_piece.style not in [p.style for p in queue_piece]:
            queue_piece.appendleft(new_piece)
            break
    
    yield queue_piece.pop()


class GameOver_animate(Remember):

    def __init__(self, display: Display):
        super().__init__(~20, 20, reverse=YES)
        self.__display = display()
        self.__kill_switch = OFF


    def do(self) -> bool:
        if self.__kill_switch: return YES
        if pyxel.frame_count % GAMEOVER_SPEED != 0: return NO

        x = self.remember
        if  x > -1:
            for j in range(0, 10):
                self.__display[self.current][j].style = DEAD

            return NO

        elif x == -21:
            self.__kill_switch = ON

            return YES

        elif x <= -1:
            for j in range(0, 10):
                self.__display[~self.current][j].style = CHESS
            
            return NO


class Clear_animate(Remember):
    
    def __init__(self, display: Display):
        super().__init__(0, len(CLEAR_LOC) + 1)
        self.__display = display()
        self.__candidate_rows = display.candidate_rows


    def do(self, style: Tuple[int]) -> bool:
        if pyxel.frame_count % CLEAR_SPEED != 0: return NO

        if self.remember != len(CLEAR_LOC):
            for j in CLEAR_LOC[self.current]:
                for index_row in self.__candidate_rows:
                    self.__display[index_row][j].style = style
                    self.__display[index_row][j].fill = 0

            return NO

        return YES


class LevelUp_animate(Remember):

    def __init__(self):
        super().__init__(0, len(LEVELUP_LOC) + 1)


    def do(self) -> bool:
        if pyxel.frame_count % LEVELUP_SPEED != 0: return NO

        if self.remember != len(LEVELUP_LOC):
            pyxel.text(47, 58 + pixel8(LEVELUP_LOC[self.current]), 'LevelUP!', pyxel.frame_count % 16)
            return NO

        else: return YES


class CountDown_animate(Remember):

    def __init__(self, display: Display):
        super().__init__(0, FPS * 10)
        self.__display = display()
        self.__kill_switch: bool = OFF


    def do(self) -> bool:
        if self.__kill_switch: return YES

        if in_range(0, FPS, self.remember): # Show 1
            pyxel.blt(56, 48, 0, *COUNTDOWN[0], 16, 24)
            if self.remember == 1: pyxel.play(0, 12)

        elif in_range(FPS, FPS * 3, self.remember): # Show 2
            pyxel.blt(56, 48, 0, *COUNTDOWN[1], 16, 24)
            if self.remember == 24: pyxel.play(0, 13)

        elif in_range(FPS * 3, FPS * 5, self.remember): # Show 3
            pyxel.blt(56, 48, 0, *COUNTDOWN[2], 16, 24)
            if self.remember == 64: pyxel.play(0, 14)

        elif in_range(FPS * 5, FPS * 9, self.remember): # show GO!
            pyxel.blt(44, 84, 0, *COUNTDOWN[3], 40, 24)
            if self.remember == 105: pyxel.play(0, 15)

        else:
            super().__init__(0, 21)
            self.__kill_switch = ON

            return YES

        return NO
    
    
    def clear(self, level_color: Tuple[int]) -> bool:
        if pyxel.frame_count % COUNTDOWN_CLEAR_SPEED != 0: return NO

        x = self.remember
        if x == 20: return YES

        elif  x > -1:
            for j in range(0, 10):
                self.__display[self.current][j].style = level_color

            return NO



class Display:
    """ Display is part of main place that store pieces """

    __slots__ = 'tile_map', 'u', 'v', 'w', 'h', 'candidate_rows', 'valid_w', 'valid_h', \
        '_main_style', '_next_piece', '__pesudo_display', 'is_full', 'gameover_animate', \
        'clear_animate', 'levelup_animate', 'countdown_animate'

    def __init__(self):
        self.tile_map = 0
        self.u = 0
        self.v = 0
        self.w = pixel8(24)
        self.h = pixel8(32)
        self.candidate_rows: List[int] = []
        self.valid_w: Tuple[int] = (pixel8(3), pixel8(12)) # (start, end)
        self.valid_h: Tuple[int] = (pixel8(1), pixel8(20)) # (start, end)
        self._main_style: Tuple[int] = CHESS
        self._next_piece: Piece = None
        # __pesudo_display have 20-rows & 10-cols
        self.__pesudo_display: List[List[Block]] = [
            [Block(style=self._main_style) for _ in range(10)] for _ in range(20)
        ]
        self.is_full: bool = NO
        self.gameover_animate = GameOver_animate(self)
        self.clear_animate = Clear_animate(self)
        self.levelup_animate = LevelUp_animate()
        self.countdown_animate = CountDown_animate(self)


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
        """ Get style of display """

        return self._main_style


    @style.setter
    def style(self, new: Tuple[int]) -> None:
        """ Set style of display """

        self._main_style = new
        for row in self.__pesudo_display:
            for block in row:
                if block.fill: continue
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
                if not col: continue

                if style is None:
                    pyxel.blt(loc_x + pixel8(i), loc_y + pixel8(j), 0, *piece.style, W, H)

                else: pyxel.blt(loc_x + pixel8(i), loc_y + pixel8(j), 0, *style, W, H)


    def draw_top_bar(self) -> None:
        """ Draw the top bar of display """

        for i in range(10): pyxel.blt(pixel8(i + 3), 0, 0, 120, 16, W, H)


    def draw_next_piece(self, *, random: bool=NO, kill_switch: bool=OFF) -> None:
        """ Draw the next piece in right corner on display """

        if kill_switch: return

        if not random:
            self._next_piece = queue_piece[-1]

        elif pyxel.frame_count % DRAW_WAIT == 0:
            self._next_piece = next(random_piece())

        try:
            offset_x = len(self._next_piece.current_rotation)
            offset_y = len(self._next_piece.current_rotation[0])
            self.draw_piece(
                self._next_piece,
                pixel8(16 + (4 - offset_x) // 2),
                pixel8(4 + (4 - offset_y) // 2)
            )

        except AttributeError: ...


    def draw_start(self) -> None:
        self.draw_text(Y=15)
        self.draw_text(text=KEY_BINDS.format(__version__), X=30, Y=20, static=True)


    def draw_ready(self, level_selector_loc: int) -> None:
        self.draw_text(text=CHOOSE_LEVEL_BANNER_1, X=32, Y=35)
        pyxel.blt(*LEVEL_LOC, 0, 168, 16, 80, 8)
        pyxel.blt(level_selector_loc, LEVEL_SELECTOR_Y, 0, *LEVEL_SELECTOR, 8, 8)
        self.draw_text(text=CHOOSE_LEVEL_BANNER_2, X=26, Y=82, static=True)


    def draw_pause(self) -> None:
        self.draw_empty()
        self.draw_text(text='PAUSE\n-----', X=55, Y=15)
        self.draw_text(text=KEY_BINDS.format(__version__), X=30, Y=20, static=True)


    def draw_game_over(self) -> None:
        self.draw_text(text='GAME OVER\n---------', X=47, Y=58)
        self.draw_text(text=GAMEOVER_BANNER, X=30, Y=74, static=True)


    def draw_end(self) -> None:
        self.draw_text(text=END_BANNER, X=47)


    def draw_text(self, *,
        text: str="Pyxel Tetris\n------------",
        X: int=41, Y: int=60,
        static: bool=NO, color: int=7
    ) -> None:
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
                if not col: continue
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
                if not col: continue
                try:
                    I = j - 1 + rpixel8(piece.y) + 1
                    J = i - 3 + rpixel8(piece.x)
                    # Other pieces maybe fill loc_x + i and loc_y + j
                    if self.__pesudo_display[I][J].fill: return False
                except IndexError: return False

        return True


    def check_rows(self) -> bool:
        """ Find rows that were filled with block """

        for index_row, row in enumerate(self.__pesudo_display):
            for block in row:
                if not block.fill: break

            else:
                self.candidate_rows.append(index_row)

        return len(self.candidate_rows) != 0


@play_game
class Tetris:
    """ Tetris class """

    __slots__ = '__current_state', '__previous_state', 'score', 'lines', 'level', '__level_selector_loc', \
        'display', 'speed', 'next_piece_flag', 'time_last_frame', 'dt', 'time_since_last_move', '__current_piece', \
        'is_piece_placed', 'is_clear', 'is_level_up', 'is_new_game', 'force_update', 'is_tetris_moment', 'bypass',

    def __init__(self):
        # Game state:
        self.__previous_state: Game_state = None
        self.__current_state: Game_state = None
        self.current_state = Game_state.START
        # Game instance:
        self.score = 0
        self.lines = 0
        self.level: Level = LEVELS[0]
        self.__level_selector_loc: int = LEVEL_SELECTOR_SX
        # Display of Game:
        self.display = Display()
        # Frame timing:
        self.speed = self.level.speed # Speed of game
        self.time_last_frame: float = time()
        self.dt = 0 # Delta time
        self.time_since_last_move = 0
        # Current piece:
        self.__current_piece: Piece = None
        self.current_piece = next(random_piece())
        self.init_loc_piece()
        # Game Flags:
        self.is_new_game: bool = YES
        self.is_clear: bool = NO
        self.is_level_up: bool = NO
        self.is_tetris_moment: bool = NO
        self.is_piece_placed: bool = NO
        self.force_update: bool = NO
        self.next_piece_flag: bool = NO
        self.bypass: bool = NO


    def __call__(self):
        if FPS == 20:
            pyxel.run(self.update, self.draw)

        else: print(f"Please Don\'t Change the FPS!, Reset it to FPS=20")


    def __enter__(self):
        pyxel.init(WIDTH, HEIGHT, display_scale=SCALE, title=GAME_NAME, fps=FPS)
        pyxel.load("./assets/tetris.pyxres")
        pyxel.mouse(True)
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
    def level_selector_loc(self) -> int:
        return self.__level_selector_loc

    
    @level_selector_loc.setter
    def level_selector_loc(self, value: int) -> None:
        if LEVEL_SELECTOR_SX <= value <= LEVEL_SELECTOR_EX:
            self.__level_selector_loc = value


    @property
    def previous_state(self) -> Game_state:
        return self.__previous_state


    def update(self) -> None:
        """ Update important variables of game """

        try:
            time_this_frame = time()
            self.dt = time_this_frame - self.time_last_frame
            self.time_last_frame = time_this_frame
            self.time_since_last_move += self.dt

            self.check_input_keyboard()
            self.check_input_mouse()

            match self.current_state:
                case Game_state.COUNTDOWN:
                    if not self.is_new_game:
                        self.current_state = Game_state.RUNNING


                case Game_state.RUNNING:
                    if (self.time_since_last_move >= 1 / self.speed) or self.force_update:
                        self.time_since_last_move = 0
                        self.force_update = NO

                        if self.display.check_rows(): # Let's clear the rows
                            self.current_state = Game_state.CLEAR
                            if len(self.display.candidate_rows) == 4:
                                pyxel.play(1, 9) # tetris moment
                                self.is_tetris_moment = YES

                            else:
                                pyxel.play(1, 7) # other moment

                        else: self.move_piece()
                        self.check_level()


                case Game_state.CLEAR:
                    if self.is_clear:
                        num_of_lines = len(self.display.candidate_rows)
                        score = num_of_lines * SCORE_FOR_EACH_ROW * XP_FOR_LINES[num_of_lines]
                        for i in self.display.candidate_rows:
                            self.display().insert(0, self.display().pop(i))

                        self.current_state = Game_state.RUNNING
                        self.score += score
                        self.lines += num_of_lines
                        self.is_tetris_moment = NO
                        self.is_clear = NO
                        self.display.candidate_rows.clear()
                        self.move_piece() # prevent to show blink animate


                case Game_state.LEVELUP:
                    if self.is_level_up:
                        self.set_level(level_number=self.level.level_num + 1)
                        self.current_state = Game_state.RUNNING
                        self.speed = self.level.speed
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
                    self.display.draw_next_piece(random=YES)
                    self.display.draw_start()


                case Game_state.READY:
                    self.display.draw_next_piece(random=YES)
                    self.display.draw_ready(self.level_selector_loc)


                case Game_state.COUNTDOWN:
                    if self.display.countdown_animate.do():
                        if self.display.countdown_animate.clear(self.level.color):
                            self.is_new_game = NO
                            self.force_update = YES


                case Game_state.RUNNING:
                    self.display.draw_next_piece(kill_switch=self.next_piece_flag)
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
                    self.display.draw_next_piece()
                    if self.is_tetris_moment:
                        self.display.style = next(COLORS)

                    if self.display.clear_animate.do(self.level.color):
                        self.is_clear = YES
                        self.display.style = self.level.color


                case Game_state.LEVELUP:
                    self.display.draw_next_piece()
                    self.display.draw_piece(
                        self.current_piece,
                        self.current_piece.x,
                        self.current_piece.y
                    )
                    if self.display.levelup_animate.do():
                        self.is_level_up = YES
                

                case Game_state.PAUSE:
                    self.display.draw_pause()
                

                case Game_state.GAMEOVER:
                    if self.display.gameover_animate.do():
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
        if self.current_piece.__class__.__name__ == 'Piece_I':
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

                # piece moved down
                else: self.current_piece.y += pixel8(1)

            else: # Next piece is going on, prevent blink piece when state is CLEAR
                self.score += SCORE_FOR_EACH_PIECE
                self.is_piece_placed = NO
                self.current_piece = next(random_piece())
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
        Critical Areas in Display:
            1. Right wall
            2. bottom
            3. between two pieces
            4. between piece and right wall
        """
   
        for _ in range(self.current_piece.pool_piece.len):
            if mode == Direction.LeftTurn: self.current_piece.rrotate()
            elif mode == Direction.RightTurn: self.current_piece.rotate()

            self.admit_piece()

            temp_y = self.current_piece.limit_h + self.current_piece.y
            temp_x = self.current_piece.limit_w + self.current_piece.x

            # 1. if piece closed to bottom:
            # self.current_piece.y of previous rotation of piece
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
            # self.current_piece.x of previous rotation of piece
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

            # 3. If piece closed to other pieces or was between pieces or was between piece and wall:
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
        # When the player was choosing level, display style should not change!
        if self.current_state != Game_state.READY:
            if self.display.style != self.level.color:
                self.display.style = self.level.color
        self.speed = self.level.speed


    def new_game(self) -> None:
        # Game state:
        self.current_state = Game_state.START
        # Game instance:
        self.score = 0
        self.lines = 0
        self.level = LEVELS[0]
        self.__level_selector_loc = LEVEL_SELECTOR_SX
        # Display of Game:
        self.display = Display()
        # Frame timing:
        self.speed = self.level.speed # Speed of game
        self.time_last_frame = time()
        self.dt = 0 # Delta time
        self.time_since_last_move = 0
        # Current Piece:
        self.__current_piece: Piece = None
        self.current_piece = next(random_piece())
        self.init_loc_piece()
        # Game Flags:
        self.is_new_game = YES
        self.is_clear = NO
        self.is_level_up = NO
        self.is_tetris_moment = NO
        self.is_piece_placed = NO
        self.force_update = NO
        self.next_piece_flag = NO
        self.bypass = NO


    def toggle_music(self) -> None: ...


    def check_input_keyboard(self) -> None:
        """ Capture keyboard inputs """

        if pyxel.btnp(pyxel.KEY_RETURN, hold=1):
            match self.current_state:
                case Game_state.START:
                    self.current_state = Game_state.READY
                    pyxel.play(0, 10)


                case Game_state.READY:
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
        
        if pyxel.btnp(pyxel.KEY_M, hold=1):
            self.toggle_music()

        if pyxel.btnp(pyxel.KEY_BACKSPACE, hold=1):
            self.current_state = Game_state.GAMEOVER

        if self.current_state == Game_state.READY:
            if pyxel.btnp(pyxel.KEY_LEFT, hold=1):
                pyxel.play(0, 11)
                self.level_selector_loc -= pixel8(1)
                self.set_level(level_number=(self.level_selector_loc // 8) - 3)

            elif pyxel.btnp(pyxel.KEY_RIGHT, hold=1):
                pyxel.play(0, 11)
                self.level_selector_loc += pixel8(1)
                self.set_level(level_number=(self.level_selector_loc // 8) - 3)

        if self.current_state == Game_state.RUNNING:
            # Do piece close to right wall?
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.handle_move_right()

            # Do piece close to left wall?
            if pyxel.btn(pyxel.KEY_A):
                self.handle_move_left()
            
            # Do piece close to bottom?
            if pyxel.btn(pyxel.KEY_DOWN):
                self.handle_move_down()

            if pyxel.btnp(pyxel.KEY_UP, hold=1):
                self.next_piece_flag = not self.next_piece_flag
                pyxel.play(0, 4)

            if pyxel.btnp(pyxel.KEY_Z, hold=1):
                self.handle_rotate(Direction.RightTurn)
            
            if pyxel.btnp(pyxel.KEY_X, hold=1):
                self.handle_rotate(Direction.LeftTurn)


    def check_input_mouse(self) -> None:
        """ Capture mouse inputs """
        # print(pyxel.mouse_x, pyxel.mouse_y)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, hold=1):
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
                        pyxel.play(0, 0)
                        self.bypass = YES


                case Game_state.READY:
                    if ( # Press "Select" button
                        in_range(192, 199, pyxel.mouse_y)
                        and in_range(72, 87, pyxel.mouse_x)
                    ):
                        self.current_state = Game_state.COUNTDOWN
                        pyxel.play(0, 10)

                    if ( # Press "D-pad left" button
                        in_range(201, 214, pyxel.mouse_y)
                        and in_range(17, 30, pyxel.mouse_x)
                    ): 
                        pyxel.play(0, 11)
                        self.level_selector_loc -= pixel8(1)
                        self.set_level(level_number=(self.level_selector_loc // 8) - 3)

                    elif ( # Press "D-pad right" button
                        in_range(201, 214, pyxel.mouse_y)
                        and in_range(48, 62, pyxel.mouse_x)
                    ): 
                        pyxel.play(0, 11)
                        self.level_selector_loc += pixel8(1)
                        self.set_level(level_number=(self.level_selector_loc // 8) - 3)
                    

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
                        self.next_piece_flag = not self.next_piece_flag
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
