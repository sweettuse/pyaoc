from __future__ import annotations
from collections import Counter
from functools import cache
from math import floor, log10
from typing import Iterable, Sequence
import sys

from pyaoc2019.utils import mapl, read_file


def _read_data(*, test: bool) -> list[int]:
    fname = "11.test.txt" if test else "11.txt"
    return mapl(int, read_file(fname)[0].split())


def _num_digits(n) -> int:
    return floor(log10(n)) + 1


def _new_nums(n: int) -> Sequence[int]:
    if n == 0:
        return [1]

    if (num_digits := _num_digits(n)) % 2 == 0:
        return divmod(n, 10 ** (num_digits // 2))

    return [n * 2024]


@cache
def _transform_stones(n: int, num_blinks: int) -> int:
    if num_blinks <= 0:
        return 0
    new_nums = _new_nums(n)
    return (
        len(new_nums)
        - 1
        + sum(_transform_stones(new, num_blinks - 1) for new in new_nums)
    )


def part1_and_2(data, num_blinks) -> int:
    return len(data) + sum(_transform_stones(n, num_blinks) for n in data)


def _main():
    data = _read_data(test=False)
    print(part1_and_2(data, 25))
    print(part1_and_2(data, 75))


if __name__ == "__main__":
    _main()
