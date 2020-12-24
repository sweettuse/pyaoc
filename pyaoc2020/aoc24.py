from collections import Counter
from enum import Enum
from functools import reduce
from operator import add

from more_itertools import collapse

from pyaoc2019.utils import read_file, timer, Coord

__author__ = 'acushner'


class HexOffset(Enum):
    e = Coord(1, 0)
    se = Coord(0, 1)
    sw = Coord(-1, 1)
    w = Coord(-1, 0)
    nw = Coord(0, -1)
    ne = Coord(1, -1)


def _delimit(s):
    replace = 'se sw ne nw'.split()
    for r in replace:
        s = s.replace(r, f' {r} ')

    return list(collapse((list(c) if c.startswith(tuple('ew')) else c for c in s.split()), base_type=str))


def _parse_data(fname=24):
    return list(map(_delimit, read_file(fname, 2020)))


def _flip_tiles(fname=24):
    return Counter(reduce(add, (HexOffset[inst].value for inst in line)) for line in _parse_data(fname))


def part1():
    return sum(v & 1 for v in _flip_tiles().values())


def part2():
    black = {t for t, flips in _flip_tiles().items() if flips & 1}
    offsets = [ho.value for ho in HexOffset]

    def _update():
        num_living_neighbors = Counter(t + offset for t in black for offset in offsets)
        white_to_black = {t for t, num_neighbs in num_living_neighbors.items() if num_neighbs == 2}
        black_to_white = {t for t in black if (num_neighbs := num_living_neighbors[t]) == 0 or num_neighbs > 2}
        return (black | white_to_black) - black_to_white

    for _ in range(100):
        black = _update()
    return len(black)


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
