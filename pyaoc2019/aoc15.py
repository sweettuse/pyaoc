import random
from enum import Enum
from itertools import cycle
from typing import Dict, Set

from cytoolz import last, first

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


disp_map: Dict[Tile, str] = {
    Tile.empty: '.',
    Tile.wall: '#',
    Tile.oxygen_unit: 'O',
    None: ' ',
}

_dirs = Coord(0, 1), Coord(0, -1), Coord(-1, 0), Coord(1, 0)
dir_offset_map: Dict[int, Coord] = dict(zip(range(1, 5), _dirs))
offset_dir_map: Dict[Coord, int] = dict(zip(_dirs, range(1, 5)))

_opps = Coord(0, -1), Coord(0, 1), Coord(1, 0), Coord(-1, 0)
offset_opp_dir_map: Dict[Coord, Coord] = dict(zip(_opps, range(1, 5)))
opposites = {1: 2, 2: 1, 3: 4, 4: 3}


class Map(dict):
    def __init__(self, wall_size=None):
        super().__init__()
        self._wall_size = wall_size

    def to_check(self, c: Coord):
        return [d for
                d, offset in dir_offset_map.items()
                if (new_pos := c + offset) not in self
                and (self._wall_size is None or
                     (abs(new_pos.x) <= self._wall_size
                      and abs(new_pos.y) <= self._wall_size))]


Map: Dict[Coord, Tile]


class RepairDroid:
    def __init__(self, program: Program):
        self._cur_pos = Coord(0, 0)
        self._map = Map()
        self._map[self._cur_pos] = Tile.empty
        self._prog = self._init_program(program)
        self._last_dir = None
        self._dirs = []

    def _init_program(self, prog: Program):
        prog.inputs = self._next_dir()
        prog.suppress_output = True
        return prog

    def run(self):
        for t in map(Tile, self._prog.execute()):
            next_pos = self._cur_pos + dir_offset_map[self._last_dir]

            print(self._cur_pos, next_pos, t, Direction(self._last_dir))

            if t is not Tile.wall:
                if next_pos not in self._map:
                    self._dirs.append(offset_dir_map[self._cur_pos - next_pos])
                self._cur_pos = next_pos

            if t is Tile.oxygen_unit:
                print(t, next_pos)
                try:
                    return self._cur_pos.manhattan
                finally:
                    U.Pickle.write(droid=self)
            self._map[next_pos] = t
            self.draw(t)

    def _next_dir(self):
        while True:
            if to_check := self._map.to_check(self._cur_pos):
                self._last_dir = random.choice(to_check)
            else:
                self._last_dir = self._dirs.pop()
            yield self._last_dir

    def draw(self, t: Tile, around=8):
        res = [[None] * around * 2 for _ in range(around * 2)]
        cp = self._cur_pos

        coords = (Coord(x, y) for x in range(cp.x - around, cp.x + around)
                  for y in range(cp.y - around, cp.y + around))
        res_rcs = ((r, c) for c in range(2 * around) for r in range(2 * around))
        for coord, (r, c) in zip(coords, res_rcs):
            res[r][c] = disp_map[self._map.get(coord)]

        res[around][around] = 'D'
        s = f'{Direction(self._last_dir)} -> {self._cur_pos} {t}'
        print(len(s) * '-')
        print(s)
        print(2 * around * '_')
        for l in reversed(res):
            print(''.join(l) + '|')
        print(2 * around * '-')
        print()


def __main():
    rd = RepairDroid(parse_file(15))
    print(rd.run())


if __name__ == '__main__':
    __main()
