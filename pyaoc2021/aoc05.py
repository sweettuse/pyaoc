__author__ = 'acushner'

from collections import Counter
from typing import NamedTuple

from pyaoc2019.utils import read_file, Coord


class LineSeg(NamedTuple):
    c1: Coord
    c2: Coord

    @classmethod
    def from_str(cls, s: str):
        c1, c2 = s.split(' -> ')
        return cls(Coord(*eval(c1)), Coord(*eval(c2)))

    @property
    def is_diag(self):
        return (self.c1.x != self.c2.x
                and self.c1.y != self.c2.y)

    def traversed_coords(self, include_diag=False) -> set[Coord]:
        if not include_diag and self.is_diag:
            return set()

        (x1, y1), (x2, y2) = self
        if x1 == x2:  # vertical
            return {Coord(x1, v) for v in range(min(y1, y2), max(y1, y2) + 1)}

        if y1 == y2:  # horizontal
            return {Coord(v, y1) for v in range(min(x1, x2), max(x1, x2) + 1)}

        # diagonal
        x_off = 1 if x2 > x1 else -1
        y_off = 1 if y2 > y1 else -1
        return {self.c1 + m * Coord(x_off, y_off) for m in range(abs(x2 - x1) + 1)}


def parse_data() -> list[LineSeg]:
    if debug:
        data = read_file('05.test', 2021)
    else:
        data = read_file(5, 2021)
    return list(map(LineSeg.from_str, data))


def part1and2(*, include_diag):
    res = Counter(c for ls in parse_data()
                  for c in ls.traversed_coords(include_diag))
    return sum(v > 1 for v in res.values())


debug = False


def __main():
    print(part1and2(include_diag=False))
    print(part1and2(include_diag=True))


if __name__ == '__main__':
    __main()
