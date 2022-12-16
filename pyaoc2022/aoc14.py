from __future__ import annotations
from collections import defaultdict
from heapq import heapify
from itertools import count, pairwise
from typing import Iterable

from pyaoc2019.utils import Coord as OrigCoord, read_file


class Coord(OrigCoord):
    def to(self, other) -> set[Coord]:
        get_range = lambda i: range(min(self[i], other[i]), max(self[i], other[i]) + 1)
        if self.x == other.x:
            return {Coord(self.x, y) for y in get_range(1)}
        elif self.y == other.y:
            return {Coord(x, self.y) for x in get_range(0)}
        return {self}


def parse_data(name) -> set[Coord]:
    """return mapping of x coord to all rock occurrences at that x coord, sorted"""

    def _to_terminals(l):
        return [Coord(*eval(s)) for s in l.split(' -> ')]

    def _to_coords(coords: list[Coord]) -> Iterable[set[Coord]]:
        if not coords:
            return [set()]
        if len(coords) == 1:
            return [{coords[0]}]

        return (c1.to(c2) for c1, c2 in pairwise(coords))

    sets = (s for l in read_file(name) for s in _to_coords(_to_terminals(l)))
    return set.union(*sets)


dirs = down, down_left, down_right = Coord(0, 1), Coord(-1, 1), Coord(1, 1)
start = Coord(500, 0)


def place_brute(coords: set[Coord], max_y: int):
    cur = start
    while True:
        if cur in coords:
            return None
        for d in dirs:
            nxt = cur + d
            if nxt not in coords:
                cur = nxt
                break
        else:
            coords.add(cur)
            return cur

        if cur == start or cur.y >= max_y:
            return None


def part1(name, add_floor: bool = False):
    coords = parse_data(name)
    max_y = max(c.y for c in coords)
    if add_floor:
        coords.update(Coord(x, max_y + 2) for x in range(-1000, 2000))
        max_y = max_y + 2

    for i in count():
        if not place_brute(coords, max_y):
            break
    return i


print(part1(14, add_floor=False))
print(part1(14, add_floor=True))
