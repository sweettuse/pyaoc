from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from enum import Enum
from itertools import pairwise
from typing import NamedTuple

from rich import print

from pyaoc2019.utils import read_file


class Point(NamedTuple):
    r: int
    c: int


    def between(self, a: Point, b: Point) -> bool:
        if len({self.r, a.r, b.r}) == 1:
            start, end = sorted((a.c, b.c))
            p = self.c
        elif len({self.c, a.c, b.c}) == 1:
            start, end = sorted((a.r, b.r))
            p = self.r
        else:
            raise Exception
        return start < p < end


    def __add__(self, other: tuple[int, int] | Point) -> Point:
        s_r, s_c = self
        o_r, o_c = other
        return Point(s_r + o_r, s_c + o_c)

    def __sub__(self, other: tuple[int, int] | Point) -> Point:
        s_r, s_c = self
        o_r, o_c = other
        return Point(s_r - o_r, s_c - o_c)



@dataclass
class Guard:
    location: Point
    direction: Point

    @property
    def next_location(self) -> Point:
        return self.location + self.direction

    def rotate_right(self):
        if self.direction == Point(-1, 0):
            d = Point(0, 1)
        elif self.direction == Point(0, 1):
            d = Point(1, 0)
        elif self.direction == Point(1, 0):
            d = Point(0, -1)
        elif self.direction == Point(0, -1):
            d = Point(-1, 0)
        self.direction = d

    def move(self):
        self.location = self.next_location


@dataclass
class Lab:
    layout: dict[Point, str]
    starting_point: Point

    def __contains__(self, p: Point) -> bool:
        return p in self.layout
    
    def __getitem__(self, p: Point) -> str:
        return self.layout[p]

    def is_occupied(self, p: Point) -> bool:
        if p not in self:
            return True
        if p == self.starting_point:
            return True
        return self[p] == '#'



def _get_dir(c) -> Point:
    if c == '^':
        return Point(-1, 0)
    raise Exception('unhandled')

def _read_data(*, test: bool) -> tuple[Guard, Lab]:
    fname = "06.test.txt" if test else "06.txt"
    guard: Guard
    layout = {}
    for r, row in enumerate(read_file(fname)):
        for c, char in enumerate(row):
            p = Point(r, c)
            if char not in '.#':
                guard = Guard(p, _get_dir(char))
                char = '.'

            layout[p] = char
    return guard, Lab(layout, guard.location)


class ActionPoint(NamedTuple):
    p: Point
    num_rotations: int
    @property
    def r(self) -> int: 
        return self.r
    @property
    def c(self) -> int: 
        return self.c

def part1(guard: Guard, lab: Lab) -> tuple[set[Point], list[ActionPoint]]:
    seen: set[Point] = set()
    action_points: list[ActionPoint] = []

    while True:
        seen.add(guard.location)

        if guard.next_location not in lab:
            return seen, action_points
        for i in range(4):
            if lab[guard.next_location] == '.':
                break
            guard.rotate_right()
        if i:
            action_points.append(ActionPoint(guard.location, i))
        guard.move()


    
def fourwise(it):
    it = iter(it)
    d = deque([next(it), next(it), next(it)], maxlen=3)
    while (n := next(it, None)) is not None:
        yield *d, n
        d.append(n)
    yield *d, n

def _sign(n: int) -> int:
    if n == 0:
        return 0
    if n < 0:
        return -1
    return 1

def _obstacle_location(aps: list[ActionPoint]) -> Point | None:
    # get bounds
    *known_aps, nxt = aps
    known = [ap.p for ap in known_aps]
    min_r = min(ap.r for ap in known)
    max_r = max(ap.r for ap in known)
    min_c = min(ap.c for ap in known)
    max_c = max(ap.c for ap in known)


    box = {
        Point(min_r, min_c),
        Point(max_r, min_c),
        Point(min_r, max_c),
        Point(max_r, max_c),
    }

    missing = (box - set(known)).pop()
    
    if nxt is None or missing.between(known[-1], nxt.p):
        r, c = missing - known[-1]
        return missing + Point(_sign(r), _sign(c))

    return None



def part2(lab: Lab, starting_point: Point, traversed: set[Point], aps: list[ActionPoint]) -> int:
    res = set()
    for v in fourwise(aps):
        potential = _obstacle_location(v)
        if potential is None:
            continue
        if not lab.is_occupied(potential):
            res.add(potential)
    return len(res)
        


def _main():
    guard, lab = _read_data(test=True)
    starting_point = guard.location

    traversed, aps = part1(guard, lab)
    # print(len(traversed))
    # print(len(aps))
    # print(max(ap.num_rotations for ap in aps))
    aps_test = (
        ActionPoint(p=Point(r=8, c=6), num_rotations=1),
        ActionPoint(p=Point(r=8, c=1), num_rotations=1),
        ActionPoint(p=Point(r=7, c=1), num_rotations=1),
        ActionPoint(p=Point(r=7, c=7), num_rotations=1)
    )
    print(part2(lab, starting_point, traversed, aps))


if __name__ == "__main__":
    _main()
