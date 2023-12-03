from __future__ import annotations
from dataclasses import dataclass, field
from itertools import count, product
from math import prod
import re

from pyaoc2019.utils import read_file


@dataclass(frozen=True)
class RC:
    r: int
    c: int


ids = count()


@dataclass(frozen=True, slots=True)
class Num:
    value: int
    id: int = field(default_factory=lambda: next(ids))

    def __int__(self):
        return self.value


@dataclass
class Engine:
    data: dict[RC, str]

    @classmethod
    def from_str(cls, s: str) -> Engine:
        return cls(cls._get_base_map(s) | cls._get_numbers_map(s))

    @classmethod
    def _get_base_map(cls, s: str) -> dict[RC, str]:
        return {
            RC(r, c): col
            for r, row in enumerate(s.splitlines())
            for c, col in enumerate(row)
        }

    @classmethod
    def _get_numbers_map(cls, s: str) -> dict[RC, str]:
        p = re.compile(r"\d+")
        res = {}
        for r, row in enumerate(s.splitlines()):
            for m in p.finditer(row):
                val = Num(int(m.group()))
                for c in range(*m.span()):
                    res[RC(r, c)] = val
        return res
        ...

    def get_surrounding(self, rc: RC) -> set[str | Num]:
        rcs = (
            coord
            for r, c in product(range(rc.r - 1, rc.r + 2), range(rc.c - 1, rc.c + 2))
            if (coord := RC(r, c)) != rc
        )
        return {val for coord in rcs if (val := self.data.get(coord))}


def part1(path):
    engine = _get_data(path)
    return sum(
        int(n)
        for rc, v in engine.data.items()
        if not isinstance(v, Num) and v != "."
        for n in engine.get_surrounding(rc)
        if isinstance(n, Num)
    )


def part2(path):
    def _get_symbol_value(coord: RC) -> int:
        surrounding = {v for v in engine.get_surrounding(coord) if isinstance(v, Num)}
        if len(surrounding) != 2:
            return 0
        return prod(map(int, surrounding))

    engine = _get_data(path)
    symbol_coords = (coord for coord, v in engine.data.items() if v == "*")
    return sum(map(_get_symbol_value, symbol_coords))


def _get_data(path: str) -> Engine:
    return Engine.from_str(read_file(path, do_split=False))


def __main():
    print(part1("03.txt"))
    print(part2("03.txt"))


if __name__ == "__main__":
    __main()
