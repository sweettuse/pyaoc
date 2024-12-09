from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from functools import partial, total_ordering
from itertools import combinations, pairwise
from operator import add, mul
from typing import Iterator, NamedTuple

from rich import print

from pyaoc2019.utils import read_file, RC


@dataclass
class Grid:
    max_r: int
    max_c: int
    antennae: dict[str, list[RC]]

    def is_point_valid(self, point: RC) -> bool:
        r, c = point
        if r < 0 or r > self.max_r:
            return False
        if c < 0 or c > self.max_c:
            return False
        return True


def _read_data(*, test: bool) -> Grid:
    fname = "08.test.txt" if test else "08.txt"
    res = defaultdict(list)
    for r, row in enumerate(read_file(fname)):
        for c, char in enumerate(row):
            if char != ".":
                res[char].append(RC(r, c))

    return Grid(r, c, dict(res))


def _get_antinodes(antennae: list[RC]) -> Iterator[RC]:
    for a1, a2 in combinations(antennae, 2):
        diff = a1 - a2
        yield a1 + diff
        yield a2 - diff


def part1(grid: Grid) -> int:
    antinodes = {
        rc
        for locations in grid.antennae.values()
        for rc in _get_antinodes(locations)
        if grid.is_point_valid(rc)
    }
    return len(antinodes)


def _get_antinodes2(grid: Grid, name: str) -> Iterator[RC]:
    def _antinodes(p, offset) -> Iterator[RC]:
        yield p
        while True:
            p += offset
            yield p

    for a1, a2 in combinations(grid.antennae[name], 2):
        diff = a1 - a2
        for d in diff, -diff:
            for p in _antinodes(a1, d):
                if not grid.is_point_valid(p): 
                    break
                yield p


def part2(grid: Grid) -> int:
    antinodes = {
        rc
        for name in grid.antennae
        for rc in _get_antinodes2(grid, name)
    }
    return len(antinodes)


def _main():
    grid = _read_data(test=False)
    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    _main()
