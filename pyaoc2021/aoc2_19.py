from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import permutations, pairwise, starmap, combinations, product, chain
from operator import itemgetter

from pyaoc2019.utils import read_file, mapt, exhaust, timer
from typing import NamedTuple, TypedDict, Iterable, Iterator

__author__ = 'acushner'


def parse_data(*, debug=False, test_num=None) -> list[Scanner]:
    prob_num = __file__[-5:-3]
    prob_num = 19
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test' + ('' if test_num is None else str(test_num))

    data = iter(read_file(filename, 2021))
    res = []
    while True:
        try:
            res.append(Scanner.from_str_iter(data))
        except StopIteration:
            break

    return res


@cache
def _point_canon(p: Point) -> tuple[Point, ...]:
    return tuple(Point(*map(p._get, c)) for c in canonical_order())


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def _get(self, item):
        sign, attr = item
        res = getattr(self, attr)
        if sign == '-':
            res = -res
        return res

    @property
    def canonical(self):
        return _point_canon(self)

    @classmethod
    def from_str(cls, s):
        return eval(f'cls({s})')

    def __add__(self, other):
        return type(self)(*map(sum, zip(self, other)))

    def __sub__(self, other):
        return type(self)(*(s - o for s, o in zip(self, other)))

    @property
    def manhattan(self):
        return sum(map(abs, self))


PointPair = tuple[Point, Point]


@cache
def canonical_order():
    """
    pos_neg: +, -
    facing: x, y, z
    rotation: up, right, down, left

    x:
    order: y, z, -y, -z, y
    +x up -> (y, z)
    +x right -> (z, -y)
    +x down -> (-y, -z)
    +x left -> (-z, y)

    order: y, -z, -y, z, y
    -x up -> (y, -z)
    -x right -> (-z, -y)
    -x down -> (-y, z)
    -x left -> (z, y)

    general with a, b, c
    +a up -> (b, c, -b, -c, ...)
    -a up -> (b, -c, -b, c, ...)

    y+up -> (z, x)
    z+up -> (x, y)

    """
    axis_up_map = {
        'x': ('+y', '+z'),
        'y': ('+z', '+x'),
        'z': ('+x', '+y')
    }
    _flip = dict(('+-', '-+'))

    def flip(s):
        return _flip[s[0]] + s[1]

    def order(pos_neg, b: str, c: str):
        if pos_neg == '-':
            c = flip(c)
        seq = b, c, flip(b), flip(c), b
        return pairwise(seq)

    def options(axis: str):
        facing = '+' + axis
        for pn in '+-':
            if pn == '-':
                facing = flip(facing)
            for bc in order(pn, *axis_up_map[axis]):
                yield facing, *bc

    return [v for axis in 'xyz' for v in options(axis)]


@dataclass(repr=False, frozen=True)
class Scanner:
    id: int
    points: frozenset[Point]

    @classmethod
    def from_str_iter(cls, it: Iterator[str]):
        id = int(next(it).split()[-2])
        points = set()
        for l in it:
            if not l:
                break
            points.add(Point.from_str(l))

        return cls(id, frozenset(points))

    @property
    @cache
    def _canonical(self) -> list[tuple[Point, ...]]:
        return [p.canonical for p in self.points]

    @property
    @cache
    def diffs(self):
        """manhattan distances from each point to every other point"""
        return self._diffs(self.points)

    @staticmethod
    def _diffs(points):
        res = {}
        for p1 in points:
            res[p1] = {(p2 - p1).manhattan for p2 in points}
        return res

    def __getitem__(self, item):
        return frozenset(c[item] for c in self._canonical)

    def __repr__(self):
        return f'Scanner({self.id})'


class SOP(NamedTuple):
    scanner: Scanner
    orientation: int
    point: Point

    @property
    def so(self) -> SO:
        return SO(self.scanner, self.orientation)


class SO(NamedTuple):
    scanner: Scanner
    orientation: int


def find_overlapping_pairs(scanners: list[Scanner]) -> set[tuple[Scanner, Scanner]]:
    pairs = {}
    for s1, s2 in combinations(scanners, 2):
        d1, d2 = s1.diffs, s2.diffs
        for p1, p2 in product(d1, d2):
            if len(d1[p1] & d2[p2]) >= 12:
                pairs[s1, s2] = p1, p2
                break
    for p, v in pairs.items():
        print(*p, len(v))
    return pairs


def _test2():
    scanners = parse_data(debug=True, test_num=None)
    find_overlapping_pairs(scanners).items()


def __main():
    return _test2()
    scanners = parse_data(debug=True)
    print(scanners)
    # print(scanners[0][1])
    # print(Point(10, 1, 2) + Point(1, 1, 1))
    print(len(scanners[-1].points))
    print(scanners[-1].points)
    return
    print('===========')
    pairs = _get_coverage_pairs(scanners)
    exhaust(print, pairs)
    print('=============================')
    universe = _find_possible_orientations(scanners, pairs)
    exhaust(print, universe)
    return
    print(canonical_order())
    print(len(canonical_order()))
    exhaust(print, Point(4, 6, 5).canonical)
    points = {Point(5, 6, -4), Point(-5, 4, -6), Point(4, 6, 5), Point(-4, -6, 5), Point(-6, -4, -5)}
    print(len(points))
    print(points & set(Point(4, 6, 5).canonical) == set(points))

    # print(manual_perms(-4, 5, 6))
    # print(part1(scanners))
    # print(part2(scanners))


if __name__ == '__main__':
    __main()
