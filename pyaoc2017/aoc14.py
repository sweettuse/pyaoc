from typing import Set, Dict

from pyaoc2017.aoc12 import get_num_distinct_groups
from pyaoc2019.utils import Coord
from pyaoc2017.aoc10 import knot_hash

__author__ = 'acushner'

key = 'uugsqrei'


def get_hash(row: int):
    res = bin(int(knot_hash(f'{key}-{row}'), 16))[2:]
    return '0' * (128 - len(res)) + res


def aoc14_a():
    return sum(get_hash(i).count('1') for i in range(128))


def _get_occupied_mem_coords() -> Set[Coord]:
    return {Coord(r, c)
            for r in range(128)
            for c, v in enumerate(get_hash(r))
            if v == '1'}


def _create_connections(coords: Set[Coord]) -> Dict[Coord, Set[Coord]]:
    res = {}
    offsets = Coord(0, 0), Coord(1, 0), Coord(-1, 0), Coord(0, 1), Coord(0, -1)
    for c in coords:
        res[c] = {new_coord for o in offsets if (new_coord := c + o) in coords}
    return res


def aoc14_b():
    coords = _get_occupied_mem_coords()
    connections = _create_connections(coords)
    return get_num_distinct_groups(connections)


def __main():
    print(aoc14_a())
    print(aoc14_b())


if __name__ == '__main__':
    __main()
