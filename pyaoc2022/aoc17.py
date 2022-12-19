from __future__ import annotations
from collections import defaultdict
from contextlib import suppress
from dataclasses import dataclass
from itertools import cycle
from operator import attrgetter, itemgetter

from rich import print
from pyaoc2019.utils import Coord as OrigCoord, exhaust, read_file, timer


class Coord(OrigCoord):
    def to(self, other) -> set[Coord]:
        """inclusive"""
        get_range = lambda i: range(min(self[i], other[i]), max(self[i], other[i]) + 1)
        if self.x == other.x:
            return {Coord(self.x, y) for y in get_range(1)}
        elif self.y == other.y:
            return {Coord(x, self.y) for x in get_range(0)}
        return {self}


@dataclass
class Shape:
    offset: Coord = Coord(0, 0)  # lower left of bounding box with y pointing down

    @property
    def points(self) -> set[Coord]:
        return {self.offset + p for p in self._points}

    @property
    def _points(self) -> set[Coord]:
        """all the coords for the shape. moved by offset"""
        raise NotImplementedError

    def move_lr(self, d: Coord, occupied):
        next_points = {(p + d) for p in self.points}
        if all(0 <= p.x < 7 for p in next_points) and not next_points & occupied:
            self.offset += d

    def move_down(self, occupied: set[Coord]):
        if any((p - Coord(0, 1)) in occupied for p in self.points):
            return False
        self.offset -= Coord(0, 1)
        return True


@dataclass
class Long(Shape):
    """horizontal bar"""

    @property
    def _points(self) -> set[Coord]:
        return set(Coord(0, 0).to(Coord(3, 0)))


@dataclass
class Tall(Shape):
    """vertical bar"""

    @property
    def _points(self) -> set[Coord]:
        return set(Coord(0, 0).to(Coord(0, 3)))


@dataclass
class L(Shape):
    """backwards L"""

    @property
    def _points(self) -> set[Coord]:
        return set(Coord(0, 0).to(Coord(2, 0))) | set(Coord(2, 0).to(Coord(2, 2)))


@dataclass
class Plus(Shape):
    """+"""

    @property
    def _points(self) -> set[Coord]:
        return set(Coord(0, 1).to(Coord(2, 1))) | set(Coord(1, 2).to(Coord(1, 0)))


move_map = dict(zip('<>', (Coord(-1, 0), Coord(1, 0))))


@dataclass
class Square(Shape):
    @property
    def _points(self) -> set[Coord]:
        return set(Coord(0, 0).to(Coord(1, 0))) | set(Coord(0, 1).to(Coord(1, 1)))


class Chamber:
    def __init__(self, name):
        self.jets = self._jets(read_file(name, do_split=False))
        self.shapes = self._shapes()
        self.occupied = set(Coord(0, 0).to(Coord(6, 0)))
        self.height = 0
        self.num_dropped = 0
        self.seen = defaultdict(list)

    def _shapes(self):
        for s in cycle([Long, Plus, L, Tall, Square]):
            yield s

    def _jets(self, jets):
        e = list(enumerate(jets))
        for i, d in cycle(e):
            yield i, move_map[d]

    def place_next(self):
        shape_type = next(self.shapes)
        s = shape_type(Coord(2, self.height + 4))
        first = True
        self.num_dropped += 1
        # _display(self.occupied | s.points)
        while True:
            idx, jet = next(self.jets)
            if first:
                first = False
                self.seen[shape_type, idx].append((self.num_dropped, self.height))
            s.move_lr(jet, self.occupied)
            if s.move_down(self.occupied):
                continue

            new_points = s.points
            self.occupied.update(s.points)
            new_points_height = max(y for _, y in new_points)
            self.height = max(new_points_height, self.height)
            break

    def display(self):
        _display(self.occupied, self.height)


def _display(points, height=30):
    res = [['.'] * 7 for _ in range(height + 1)]
    for p in points:
        res[p.y][p.x] = '#'
    exhaust(print, map(''.join, reversed(res)))
    print('-------------------------_')


def part1(name):
    c = Chamber(name)
    for _ in range(2022):
        c.place_next()
        # c.display()
    return c.height


@timer
def part2(name):
    c = Chamber(name)
    for _ in range(10000):
        c.place_next()
    s = {(st, idx): v for (st, idx), v in c.seen.items() if st is Square}
    s = {(st, idx): v for (st, idx), v in c.seen.items() if 720 < idx < 800}
    print(sorted(s.items(), key=lambda kv: len(kv[1]), reverse=True)[-200:])
    print(len(c.seen))
    (num_drop_start, height_start), (num_drop_next, height_next) = (3600, 5520), (5330, 8164)
    cycle_len = num_drop_next - num_drop_start
    cycle_height = height_next - height_start
    target = 1000000000000
    ## submissions:
    # too low:  1528323699440
    # too high: 1528323704728
    print((target - num_drop_start) % cycle_len)
    # lol, the `+ 2` below is because i was calculating for the (target - 1) element, so i just looked up
    # the next one and added it back in
    return height_start + 2 + cycle_height * ((target - num_drop_start) // cycle_len)


print(part1(17))
print(part2(17))
