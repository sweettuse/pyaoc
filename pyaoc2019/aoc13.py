from collections import Counter
from enum import Enum
from typing import Dict, NamedTuple, Optional, Tuple

from pyaoc2019.interpreter import Program, parse_file, process
import pyaoc2019.utils as U
from pyaoc2019.colors.colors import Color, Colors, RGB
from pyaoc2019.colors.tile_utils import RC, ColorMatrix

__author__ = 'acushner'


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other[0], self.y + other[1])

    @property
    def rc(self):
        return RC(self.y, self.x)


class Dimensions(NamedTuple):
    upper_left: Coord
    lower_right: Coord

    def to_rc(self):
        return self.upper_left.rc, self.lower_right.rc


class Tile(Enum):
    empty = 0
    wall = 1
    block = 2
    paddle = 3
    ball = 4


class Arcade:
    def __init__(self):
        self.board: Dict[Coord, Tile] = {}

    def run(self, program: Program):
        program.suppress_output = True
        proc = process(program)
        U.exhaust(map(self._update_board, *([proc] * 3)))

    def _update_board(self, x, y, tile_id):
        self.board[Coord(x, y)] = Tile(tile_id)

    def _get_board_dimensions(self) -> Dimensions:
        pass

    def draw(self):
        """draw board to screen"""
        _, lr = self._get_board_dimensions()
        cm = ColorMatrix.from_shape(lr.rc)


class PlayArcade(Arcade):
    def __init__(self):
        super().__init__()
        self.score = 0
        self._prev_ball_pos: Optional[int] = None

    def _update_board(self, x, y, tile_id):
        if (x, y) == (-1, 0):
            self.score = tile_id
        else:
            super()._update_board(x, y, tile_id)

    def _adjust_joystick(self):
        pass


def aoc13_a():
    arcade = Arcade()
    arcade.run(parse_file(13))
    print(Counter(arcade.board.values()))
    return sum(v is Tile.block for v in arcade.board.values())


def __main():
    print(aoc13_a())


if __name__ == '__main__':
    __main()
