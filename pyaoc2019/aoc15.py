import random
from enum import Enum
from typing import Dict, Set

from cytoolz import last

import pyaoc2019.utils as U

from pyaoc2019.interpreter import Program, parse_file
from pyaoc2019.utils import Coord

__author__ = 'acushner'


class Direction(Enum):
    north = 1
    south = 2
    west = 3
    east = 4


class Tile(Enum):
    empty = 0
    wall = 1
    oxygen_unit = 2


_dirs = Coord(0, 1), Coord(0, -1), Coord(-1, 0), Coord(1, 0)
dir_offset_map: Dict[int, Coord] = dict(zip(range(1, 5), _dirs))
offset_dir_map: Dict[Coord, int] = dict(zip(_dirs, range(1, 5)))


# _opps = Coord(0, -1), Coord(0, 1), Coord(1, 0), Coord(-1, 0)
# offset_opp_dir_map: Dict[Coord, Coord] = dict(zip(_opps, range(1, 5)))


class Map:
    def __init__(self):
        self._map: Dict[Coord, Tile] = {}

    def __setitem__(self, key, value):
        self._map[key] = value

    def to_check(self, c: Coord):
        return [d for d, offset in dir_offset_map.items() if c + offset not in self._map]


class RepairDroid:
    def __init__(self, program: Program):
        self._cur_pos = Coord(0, 0)
        self._map = Map()
        self._map[self._cur_pos] = Tile.empty
        self._prog = self._init_program(program)
        self._path = [self._cur_pos]
        self._last_dir = None
        self._dirs = []

    def _init_program(self, prog: Program):
        prog.inputs = self._next_dir()
        prog.suppress_output = True
        return prog

    def run(self):
        for t in map(Tile, self._prog.execute()):
            next_pos = self._cur_pos + dir_offset_map[self._last_dir]
            self._map[next_pos] = t

            if random.random() < .0001:
                print(t, next_pos)

            if t is not Tile.wall:
                self._cur_pos = next_pos
                self._path.append(next_pos)

            if t is Tile.oxygen_unit:
                print(t, next_pos)
                try:
                    return self._cur_pos.manhattan
                finally:
                    U.Pickle.write(droid=self)

    def _next_dir(self):
        while True:
            if to_check := self._map.to_check(last(self._path)):
                self._last_dir = random.choice(to_check)
                self._dirs.append(self._last_dir)
            else:
                ld = self._path.pop()
                offset = last(self._path) - ld
                self._last_dir = offset_dir_map[offset]
                self._dirs.pop()
            yield self._last_dir


def __main():
    rd = RepairDroid(parse_file(15))
    print(rd.run())


if __name__ == '__main__':
    __main()
