from __future__ import annotations
from dataclasses import dataclass
from math import prod

from pyaoc2019.utils import read_file


@dataclass
class Game:
    id: int
    cube_sets: list[CubeSet]

    @classmethod
    def from_str(cls, s: str) -> Game:
        game_str, rest = s.split(":")
        id = int(game_str[5:])
        cube_sets = map(CubeSet.from_str, rest.split(";"))
        return Game(id, list(cube_sets))

    @property
    def is_valid(self) -> bool:
        return all(cs.is_valid for cs in self.cube_sets)

    @property
    def bounding_cube_set(self) -> CubeSet:
        cur = CubeSet()
        for cs in self.cube_sets:
            cur = CubeSet(*(max(a, b) for a, b in zip(cur, cs)))
        return cur


@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_str(cls, s: str) -> CubeSet:
        res = cls()
        for pair in s.split(","):
            num, color = pair.split()
            setattr(res, color, int(num))
        return res

    @property
    def is_valid(self) -> bool:
        return all(a <= b for a, b in zip(self, MAX_CUBE_SET))

    @property
    def power(self):
        return prod(self)

    def __iter__(self):
        for f in self.__dataclass_fields__:
            yield getattr(self, f)


MAX_CUBE_SET = CubeSet(12, 13, 14)


def _parse_data(fname: str) -> list[Game]:
    return list(map(Game.from_str, read_file(fname)))


def part1(fname: str) -> int:
    return sum(g.id for g in _parse_data(fname) if g.is_valid)


def part2(fname: str) -> int:
    return sum(g.bounding_cube_set.power for g in _parse_data(fname))


def __main():
    print(part1("02.txt"))
    print(part2("02.txt"))


if __name__ == "__main__":
    __main()


def _parse_line(s: str) -> Game:
    ...
