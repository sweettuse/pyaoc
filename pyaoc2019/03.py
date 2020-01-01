from itertools import groupby
import operator as op
from typing import NamedTuple, List, Tuple

from cytoolz import memoize
from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


class Coord(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Coord(self.x + other[0], self.y + other[1])

    def __mul__(self, num):
        return Coord(self.x * num, self.y * num)

    def __rmul__(self, num):
        return self * num

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y)


class Line(NamedTuple):
    c1: Coord
    c2: Coord

    def _get_xs_or_ys(self, get_y=True):
        res = [self.c1[get_y], self.c2[get_y]]
        if op.le(*res):
            res[-1] += 1
            res.append(1)
        else:
            res[-1] -= 1
            res.append(-1)
        return res

    @property
    def xs(self):
        return self._get_xs_or_ys(False)

    @property
    def ys(self):
        return self._get_xs_or_ys()

    def __and__(self, other):
        return self.range() & other.range()

    @memoize
    def range(self, return_type=set):
        return return_type(Coord(x, y) for x in range(*self.xs) for y in range(*self.ys))


def parse_file(name):
    return map(parse_data, U.read_file(name))


def parse_data(data) -> List[Line]:
    data = data.split(',')
    offsets = dict(
        R=Coord(1, 0),
        U=Coord(0, 1),
        D=Coord(0, -1),
        L=Coord(-1, 0),
    )

    res = [Coord(0, 0)]
    for val in data:
        res.append(res[-1] + offsets[val[0]] * int(val[1:]))

    return [Line(*cs) for cs in zip(res, res[1:])]


Wire = List[Line]


def get_intersections(w1: Wire, w2: Wire):
    return [intsect for l1 in w1 for l2 in w2 for intsect in l1 & l2 if intsect != Coord(0, 0)]


def populate_wire_points(w: Wire):
    points = (p for l in w for p in l.range(list))
    # remove side-by-side dupes
    return tuple(first(p) for p in groupby(points))


@memoize
def wirelen(wp: Tuple[Coord], p: Coord):
    return wp.index(p)


def aoc3_a(w1: Wire, w2: Wire):
    return min(i.manhattan for i in get_intersections(w1, w2))


def aoc3_b(w1: Wire, w2: Wire):
    wp1, wp2 = map(populate_wire_points, (w1, w2))
    intsects = get_intersections(w1, w2)
    get_wp_vals = lambda wp: {p: wirelen(wp, p) for p in intsects}
    wp1_vals, wp2_vals = map(get_wp_vals, (wp1, wp2))
    return min(wp1_vals[i] + wp2_vals[i] for i in intsects)


def __main():
    w1, w2 = parse_file('03')
    print(aoc3_a(w1, w2))
    print(aoc3_b(w1, w2))


if __name__ == '__main__':
    __main()
