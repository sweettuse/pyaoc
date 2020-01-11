from collections import Set, defaultdict
from enum import Enum
from typing import Dict

from pyaoc2019.interpreter import Program
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


dirs = Coord(0, 1), Coord(0, -1), Coord(-1, 0), Coord(1, 0)
dir_map = dict(zip(range(1, 5), dirs))

to_explore = lambda: set(dir_map)


class Map:
    def __init__(self):
        self._map: Dict[Coord, Tile] = {}

    def update(self, c: Coord, t: Tile):
        self._map[c] = t

    def to_check(self, c: Coord):
        return {next_c for d in dir_map.values() if (next_c := c + d) not in self._map}


class RepairDroid:
    def __init__(self, program: Program):
        self._cur_pos = Coord(0, 0)
        self._map = Map()
        self._map.update(self._cur_pos, Tile.empty, 0)
        self._next_dir: Coord
        self._next_pos: Coord
        self._prog = program
        self._running = None

    def run(self):
        self._running = self._prog.execute()


def __main():
    pass


if __name__ == '__main__':
    __main()
