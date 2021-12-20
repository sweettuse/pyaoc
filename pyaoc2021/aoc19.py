from __future__ import annotations
from dataclasses import dataclass
from functools import cache
from itertools import permutations, pairwise, starmap, combinations, product

from pyaoc2019.utils import read_file, mapt, exhaust
from typing import NamedTuple, TypedDict, Iterable, Iterator

__author__ = 'acushner'


def parse_data(*, debug=False) -> list[Scanner]:
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = iter(read_file(filename, 2021))
    res = []
    while True:
        try:
            res.append(Scanner.from_str_iter(data))
        except StopIteration:
            break

    return res


def perms(x, y, z):
    res = set()
    for x1 in x, -x:
        for y1 in y, -y:
            for z1 in z, -z:
                res.update(permutations((x1, y1, z1)))
    exhaust(print, sorted(res))
    return len(res)


@cache
def _p3d_canon(p3d: Point3d):
    return tuple(Point3d(*map(p3d._get, c)) for c in canonical_order())


class Point3d(NamedTuple):
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
        return _p3d_canon(self)

    @classmethod
    def from_str(cls, s):
        return eval(f'cls({s})')

    def __add__(self, other):
        return type(self)(*map(sum, zip(self, other)))

    def __sub__(self, other):
        return type(self)(*(s - o for s, o in zip(self, other)))


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
    points: frozenset[Point3d]

    @property
    @cache
    def _canonical(self) -> list[tuple[Point3d, ...]]:
        return [p.canonical for p in self.points]

    @property
    @cache
    def diffs(self) -> dict[Point3d, set[Point3d]]:
        """diffs from each point to every other point"""
        res = {}
        for p1 in self.points:
            cur = res[p1] = set()
            for p2 in self.points:
                if p1 is p2:
                    continue
                cur.add(p2 - p1)
        return res

    def __getitem__(self, item):
        return frozenset(c[item] for c in self._canonical)

    def __repr__(self):
        return f'Scanner({self.id})'

    @classmethod
    def from_str_iter(cls, it: Iterator[str]):
        id = int(next(it).split()[-2])
        points = set()
        for l in it:
            if not l:
                break
            points.add(Point3d.from_str(l))

        return cls(id, frozenset(points))


class ScanOr(NamedTuple):
    scanner: Scanner
    orientation: int


def _check_scanner_overlap(s1: Scanner, s2: Scanner):
    for p1, d1 in s1.diffs.items():
        for p2, d2 in s2.diffs.items():
            if len(d1 & d2) >= 11:  # 11 + the point in question
                print('overlap')
                return p1, p2

    return None, None

def _get_coverage_pairs(scanners: list[Scanner]) -> set[tuple[ScanOr, ScanOr]]:
    pairs = set()

    for s1, s2 in combinations(scanners, 2):
        p1, p2 = _check_scanner_overlap(s1, s2)
        if p1:
            print(f'for {s1} and {s2}, points {p1} and {p2} are the same')

    return pairs


def part1(data):
    pass


def part2(data):
    pass


def __main():
    scanners = parse_data(debug=True)
    print(scanners)
    print(scanners[0][1])
    print(Point3d(10, 1, 2) + Point3d(1, 1, 1))
    print(len(scanners[-1].points))
    print(_get_coverage_pairs(scanners))
    return
    print(canonical_order())
    print(len(canonical_order()))
    exhaust(print, Point3d(4, 6, 5).canonical)
    points = {Point3d(5, 6, -4), Point3d(-5, 4, -6), Point3d(4, 6, 5), Point3d(-4, -6, 5), Point3d(-6, -4, -5)}
    print(len(points))
    print(points & set(Point3d(4, 6, 5).canonical) == set(points))

    # print(manual_perms(-4, 5, 6))
    # print(part1(scanners))
    # print(part2(scanners))


if __name__ == '__main__':
    __main()
