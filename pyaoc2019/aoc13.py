import os
import time
from collections import Counter
from enum import Enum
from typing import Dict, NamedTuple, Optional

from cytoolz import juxt, memoize, comp

from pyaoc2019.colors.colors import Color, Colors
from pyaoc2019.colors.tile_utils import ColorMatrix
from pyaoc2019.interpreter import Program, parse_file, process
from pyaoc2019.utils import Coord, exhaust

__author__ = 'acushner'


class Dimensions(NamedTuple):
    upper_left: Coord
    lower_right: Coord


class Tile(Enum):
    empty = 0
    wall = 1
    block = 2
    paddle = 3
    ball = 4


color_map: Dict[Tile, Color] = {
    Tile.empty: Colors.OFF,
    Tile.wall: Colors.YELLOW,
    Tile.block: Colors.COPILOT_BLUE,
    Tile.paddle: Colors.WHITE,
    Tile.ball: Colors.MARIO_RED,

}

cached_property = comp(property, memoize)


class Arcade:
    def __init__(self):
        self.board: Dict[Coord, Tile] = {}

    def run(self, program: Program):
        program.suppress_output = True
        proc = process(program)
        exhaust(map(self._update_board, *([proc] * 3)))
        self.draw()

    def _update_board(self, x, y, tile_id):
        self.board[Coord(x, y)] = Tile(tile_id)

    @cached_property
    def board_dimensions(self) -> Dimensions:
        xs = {c.x for c in self.board}
        ys = {c.y for c in self.board}

        min_x, max_x = juxt(min, max)(xs)
        min_y, max_y = juxt(min, max)(ys)
        return Dimensions(Coord(min_x, min_y), Coord(max_x, max_y))

    @cached_property
    def color_matrix(self) -> ColorMatrix:
        _, lr = self.board_dimensions
        return ColorMatrix.from_shape(lr.rc + (1, 1))

    @property
    def rc_board(self):
        return {c.rc: t for c, t in self.board.items()}

    def _display_board(self, board: ColorMatrix):
        if not display_board:
            return
        print(board.color_str)
        time.sleep(sleep_secs)

    def _populate_board(self):
        cm = self.color_matrix
        for rc, t in self.rc_board.items():
            cm[rc] = color_map[t]
        return cm

    def draw(self):
        """draw board to screen"""
        os.system('clear')
        self._display_board(self._populate_board())


class PlayArcade(Arcade):
    def __init__(self):
        super().__init__()
        self.score = 0
        self._ball_pos: Optional[Coord] = None
        self._next_ball_pos: Optional[Coord] = None
        self.paddle_pos: Optional[Coord] = None

    def _update_board(self, x, y, tile_id):
        if (x, y) == (-1, 0):
            self.score = tile_id
            return

        t = Tile(tile_id)
        if t is Tile.ball:
            self.ball_pos = Coord(x, y)
            return

        if t is Tile.paddle:
            self.paddle_pos = Coord(x, y)
        super()._update_board(x, y, tile_id)

    @property
    def ball_pos(self):
        return self._ball_pos

    @ball_pos.setter
    def ball_pos(self, next_pos: Coord):
        ub = super()._update_board
        if self._ball_pos:
            ub(*self._ball_pos, Tile.empty)

        self._ball_pos = self._next_ball_pos
        self._next_ball_pos = next_pos
        if self._ball_pos:
            ub(*self._ball_pos, Tile.ball)

    @property
    def ball_dir(self) -> Optional[int]:
        if not (self._next_ball_pos and self._ball_pos):
            return
        return (self._next_ball_pos - self._ball_pos).x

    def adjust_joystick(self):
        """input stream for program"""
        while True:
            if not self._ball_pos or not self.paddle_pos:
                self.draw()
                yield 0
                continue

            self.draw()
            mtb = self._move_toward_ball()
            yield mtb if mtb is not None else self.ball_dir

    def _move_toward_ball(self) -> Optional[int]:
        paddle_dir = (self._ball_pos - self.paddle_pos).x
        if not paddle_dir:
            return
        return min(1, max(-1, paddle_dir // 2))

    def _display_board(self, board: ColorMatrix):
        if not display_board:
            return
        score_str = f'SCORE: {self.score:05d}'
        print(Colors.COPILOT_BLUE.color_str(score_str))
        print(board.color_str)
        time.sleep(sleep_secs)


display_board = True
sleep_secs = .2


def aoc13_a():
    arcade = Arcade()
    arcade.run(parse_file(13))
    print(Counter(arcade.board.values()))
    print(arcade.board_dimensions)
    return sum(v is Tile.block for v in arcade.board.values())


def aoc13_b():
    arcade = PlayArcade()
    program = parse_file(13, arcade.adjust_joystick())
    program[0] = 2
    arcade.run(program)
    return arcade.score


def __main():
    print(aoc13_b())


if __name__ == '__main__':
    __main()
