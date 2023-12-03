from __future__ import annotations
from dataclasses import dataclass
from math import prod

from pyaoc2019.utils import mapt, read_file, timer

frozen = True
slots = True


@dataclass(frozen=frozen, slots=slots)
class Game:
    id: int
    cube_sets: tuple[CubeSet, ...]

    @classmethod
    def from_str(cls, s: str) -> Game:
        game_str, rest = s.split(":")
        return Game(int(game_str[5:]), mapt(CubeSet.from_str, rest.split(";")))

    @property
    def is_valid(self) -> bool:
        return all(cs.is_valid for cs in self.cube_sets)

    def calc_bounding_cube_set(self) -> CubeSet:
        cur = CubeSet()
        for cs in self.cube_sets:
            cur = CubeSet(*(max(a, b) for a, b in zip(cur, cs)))
        return cur


@dataclass(frozen=frozen, slots=slots)
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_str(cls, s: str) -> CubeSet:
        num_colors = (num_color.split() for num_color in s.split(","))
        return cls(**dict((color, int(num)) for num, color in num_colors))

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


def _parse_data(fname: str) -> tuple[Game]:
    return mapt(Game.from_str, read_file(fname))


def part1(fname: str) -> int:
    return sum(g.id for g in _parse_data(fname) if g.is_valid)


def part2(fname: str) -> int:
    return sum(g.calc_bounding_cube_set().power for g in _parse_data(fname))


@timer
def __main():
    print(part1("02.txt"))
    print(part2("02.txt"))


if __name__ == "__main__":
    __main()
