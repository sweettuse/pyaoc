from enum import Enum
from functools import reduce
from itertools import accumulate
from operator import add

from cytoolz.itertoolz import first

import pyaoc2019.utils as U
from pyaoc2019.utils import Coord

__author__ = 'acushner'


class HexOffset(Enum):
    n = Coord(0, 1)
    ne = Coord(1, 0)
    se = Coord(1, -1)
    s = Coord(0, -1)
    sw = Coord(-1, 0)
    nw = Coord(-1, 1)


def _get_offsets(s: str):
    return (HexOffset[d].value for d in s.split(','))


def calc_final_dist(s: str):
    return reduce(add, _get_offsets(s)).hex_manhattan


def calc_farthest_dist(s: str):
    return max(h.hex_manhattan for h in accumulate(_get_offsets(s)))


def __main():
    data = first(U.read_file(11, 2017))
    print(calc_final_dist(data))
    print(calc_farthest_dist(data))


if __name__ == '__main__':
    __main()
