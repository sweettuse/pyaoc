from enum import Enum
from typing import Dict, NamedTuple

from cytoolz import take

from pyaoc2019.interpreter import Instructions, parse_file, process

__author__ = 'acushner'


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other[0], self.y + other[1])


class Tile(Enum):
    empty = 0
    wall = 1
    block = 2
    paddle = 3
    ball = 4


tile_map = {t.value: t for t in Tile}


class Arcade:
    def __init__(self):
        self.board: Dict[Coord, Tile] = {}

    def run(self, instructions: Instructions):
        proc = process(instructions)
        for val in proc:
            self._update_board(val, *take(2, proc))

    def _update_board(self, x, y, tile_id):
        self.board[Coord(x, y)] = tile_map[tile_id]


def aoc13_a():
    arcade = Arcade()
    arcade.run(parse_file(13))
    return sum(v is Tile.block for v in arcade.board.values())


def __main():
    print(aoc13_a())


if __name__ == '__main__':
    __main()
