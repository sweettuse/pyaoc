from __future__ import annotations
from math import prod
import re
from rich import print

from pyaoc2019.utils import read_file


def _read_data(*, test=False) -> dict:
    data = read_file("04.txt" if not test else "04.test.txt")
    return {(r, c): value for r, row in enumerate(data) for c, value in enumerate(row)}


def _get_range(start, r, c, num=4):
    start_r, start_c = start
    return [(start_r + r * offset, start_c + c * offset) for offset in range(num)]


def _get_word(points, data):
    return "".join(data.get(p, "") for p in points)


def part1(data):
    total = 0
    for point in data:
        for r, c in (0, 1), (1, 0), (1, 1), (-1, 1):
            points = _get_range(point, r, c)
            word = _get_word(points, data)
            if word in {"XMAS", "SAMX"}:
                total += 1
    return total


def _get_x_ranges(start):
    start_r, start_c = start
    return (
        [
            (start_r - 1, start_c - 1),
            (start_r, start_c),
            (start_r + 1, start_c + 1),
        ],
        [
            (start_r + 1, start_c - 1),
            (start_r, start_c),
            (start_r - 1, start_c + 1),
        ],
    )


def part2(data):
    total = 0
    for point, value in data.items():
        if value != "A":
            continue
        words = {_get_word(points, data) for points in _get_x_ranges(point)}
        if words <= {"SAM", "MAS"}:
            total += 1
    return total


def _main():
    data = _read_data(test=True)

    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    _main()
