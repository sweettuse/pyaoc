from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from itertools import pairwise, combinations, product
from operator import itemgetter

from pyaoc2019.utils import read_file, exhaust
from typing import NamedTuple, Iterator

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
        return self._diffs(self.points)

    @staticmethod
    def _diffs(points) -> dict[Point3d, set[Point3d]]:
        res = {}
        for p1 in points:
            res[p1] = {p2 - p1 for p2 in points if p1 is not p2}
        return res

    @property
    @cache
    def all_orient_diffs(self):
        """ orientation -> point -> diffs"""
        res = {}
        for orient in range(24):
            cur_points = list(map(itemgetter(orient), self._canonical))
            res[orient] = self._diffs(cur_points)
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


def _check_overlap(diffs1, diffs2):
    for p1, d1 in diffs1.items():
        for p2, d2 in diffs2.items():
            if len(d1 & d2) >= 11:  # 11 + the point in question
                return p1, p2

    return None, None


def _check_scanner_overlap_full(s1: Scanner, s2: Scanner):
    """check diffs in all possible orientations"""
    for o1, o2 in product(range(24), repeat=2):
        diffs1 = s1.all_orient_diffs[o1]
        diffs2 = s2.all_orient_diffs[o2]
        p1, p2 = _check_overlap(diffs1, diffs2)
        if p1:
            yield (o1, p1), (o2, p2)


class SOP(NamedTuple):
    scanner: Scanner
    orientation: int
    point: Point3d

    @property
    def so(self) -> SO:
        return SO(self.scanner, self.orientation)


class SO(NamedTuple):
    scanner: Scanner
    orientation: int


def _get_coverage_pairs(scanners: list[Scanner]) -> set[tuple[SOP, SOP]]:
    pairs = set()

    for s1, s2 in combinations(scanners, 2):
        for p1, p2 in _check_scanner_overlap_full(s1, s2):
            if p1:
                o1, p1 = p1
                o2, p2 = p2
                pairs.add((SOP(s1, o1, p1), SOP(s2, o2, p2)))
                print(f'for {o1:2}:{s1} and {o2:2}:{s2}, points {p1} and {p2} are the same')

    return pairs


ScanOr = tuple[Scanner, int]


def _find_possible_orientations(scanners: list[Scanner], pairs: set[tuple[SOP, SOP]]):
    """scanner, orientation -> {(scanner, orientation matches)}

    chain together (orientation, scanner) pairs to find a cohesive universe
    """
    start = scanners[0]
    scanners = set(scanners)
    sop_map = defaultdict(set)
    for sop1, sop2 in pairs:
        sop_map[sop1.so].add(sop2.so)

    def _find(possible: set[SOP], seen: frozenset[Scanner] = frozenset()):
        for sop in possible:
            if sop.scanner in seen:
                return

            seen |= {sop.scanner}
            if not scanners - seen:
                return seen

            matches = sop_map.get(sop)
            if not matches:
                return

            if res := _find(matches, seen):
                return res

    for sop, matches in sop_map.items():
        if sop.scanner is not start:
            continue
        print('trying')
        if res := _find(matches, frozenset({sop.scanner})):
            return res


def _normalize_points(pairs: set[tuple[SOP, SOP]]):
    pass


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
    print(pairs := _get_coverage_pairs(scanners))
    print('=============================')
    print(_find_possible_orientations(scanners, pairs))
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
