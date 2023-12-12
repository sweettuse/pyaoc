from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from functools import cached_property
from itertools import count
from typing import Iterable, cast
from pyaoc2019.utils import exhaust, identity, mapt, mapl, read_file, timer
from enum import Enum


class Dir(Enum):
    north = "n"
    south = "s"
    east = "e"
    west = "w"

    def __neg__(self) -> Dir:
        if self is self.north:
            return self.south
        if self is self.south:
            return self.north
        if self is self.east:
            return self.west
        if self is self.west:
            return self.east
        raise Exception

    @cached_property
    def point(self) -> Point:
        if self is self.north:
            return Point(0, -1)
        if self is self.south:
            return Point(0, 1)
        if self is self.east:
            return Point(1, 0)
        if self is self.west:
            return Point(-1, 0)
        raise Exception
    
    def __lt__(self, other) -> bool:
        return dir_nums[self] < dir_nums[other]

dir_nums = dict(zip(Dir, count()))


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point | Dir) -> Point:
        if isinstance(other, Dir):
            return self + other.point
        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point | Dir) -> Point:
        if isinstance(other, Dir):
            return self - other.point
        return self.__class__(self.x - other.x, self.y - other.y)


class outputs:
    outputs = {
        "|": {Dir.north, Dir.south},
        "-": {Dir.east, Dir.west},
        "L": {Dir.north, Dir.east},
        "J": {Dir.north, Dir.west},
        "7": {Dir.west, Dir.south},
        "F": {Dir.east, Dir.south},
        "S": set(Dir),
        ".": set(),
    }

    def __class_getitem__(cls, key: str) -> set[Dir]:
        return set(cls.outputs[key])


@dataclass
class System:
    layout: dict[Point, Location]

    def __post_init__(self):
        self._make_connections()

    @classmethod
    def from_fname(cls, fname: str) -> System:
        return cls.from_str(read_file(fname, do_split=False))  # type: ignore

    @classmethod
    def from_str(cls, s: str) -> System:
        return cls(
            {
                (p := Point(x, y)): Location(p, c)
                for y, row in enumerate(s.splitlines())
                for x, c in enumerate(row)
            }
        )

    @property
    def starting_point(self) -> Point:
        return next(p for p, v in self.layout.items() if v.type == "S")

    @property
    def starting_location(self) -> Location:
        return self.layout[self.starting_point]

    @property
    def occupied_locations(self) -> list[Location]:
        return [v for v in self.layout.values() if v.is_occupied]

    def _make_connections(self):
        """add connected neighbors"""
        exhaust(self._connect, self.occupied_locations)

    def _connect(self, loc: Location):
        for d in loc.outputs:
            if not (other := self.layout.get(loc.point + d)):
                continue
            if -d in other.outputs:
                loc.connections[d] = other
                other.connections[-d] = loc


@dataclass
class Location2:
    point: Point
    occupied: bool


@dataclass
class Exploded(System):
    @classmethod
    def from_system(cls, system: System) -> Exploded:
        """expand system from one point into 2x2 points"""
        ...

    @classmethod
    def _exploded(
        cls, location: Location
    ) -> tuple[Location2, Location2, Location2, Location2]:
        match sorted(location.connections):
            case [Dir.north, Dir.south]:
                ...
            case [Dir.east, Dir.west]:
                ...


@dataclass
class Location:
    point: Point
    type: str
    outputs: set[Dir] = field(default_factory=set)
    visited: bool = False
    connections: dict[Dir, Location] = field(default_factory=dict, repr=False)
    distance: int | None = None

    @property
    def is_occupied(self) -> bool:
        return self.type != "."

    def __post_init__(self):
        self.outputs.update(outputs[self.type])  # type: ignore


@timer
def part1(fname: str):
    system = System.from_fname(fname)

    to_check = deque([(system.starting_location, 0)])
    while to_check:
        cur, distance = to_check.popleft()
        if cur.distance is not None and cur.distance < distance:  # type: ignore
            continue
        cur.distance = distance
        for l in cur.connections.values():
            to_check.append((l, distance + 1))  # type: ignore

    return max(l.distance for l in system.occupied_locations if l.distance is not None)


def part2(fname: str):
    print(sorted(Dir))
    ...


if __name__ == "__main__":
    print(part1("10.txt"))
    print(part2(""))
