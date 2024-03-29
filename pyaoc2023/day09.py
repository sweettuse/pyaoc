from __future__ import annotations
from itertools import cycle, pairwise
from typing import Iterable

from pyaoc2019.utils import exhaust, identity, mapl, read_file


def _get_data(fname, *, reverse=False):
    res = [mapl(int, line.split()) for line in read_file(fname)]
    if reverse:
        exhaust(l.reverse() for l in res)
    return res


def _get_diffs(ints: list[int]) -> Iterable[list[int]]:
    while any(ints):
        yield ints
        ints = [v2 - v1 for v1, v2 in pairwise(ints)]


def part1(fname: str) -> int:
    return sum(
        diff[-1]
        for row_diffs in map(_get_diffs, _get_data(fname))
        for diff in row_diffs
    )


def part2(fname: str) -> int:
    return sum(
        sign * diff[0]
        for row_diffs in map(_get_diffs, _get_data(fname))
        for sign, diff in zip(cycle((1, -1)), row_diffs)
    )


def both(fname: str, *, reverse: bool) -> int:
    return sum(
        diff[-1]
        for row_diffs in map(_get_diffs, _get_data(fname, reverse=reverse))
        for diff in row_diffs
    )


if __name__ == "__main__":
    print(part1("09.txt"))
    print(part2("09.txt"))
    print(both("09.txt", reverse=False))
    print(both("09.txt", reverse=True))
