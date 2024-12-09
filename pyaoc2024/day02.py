from __future__ import annotations
from collections import Counter
from itertools import pairwise
from rich import print

from pyaoc2019.utils import read_file

def _read_data(test=False) -> list[list[int]]:
    return [
        list(map(int, r.split()))
        for r in read_file("02.txt" if not test else "02.test.txt")
    ]


def _is_valid(row: list[int]) -> bool:
    negative = None
    for i1, i2 in pairwise(row):
        diff = i2 - i1
        if abs(diff) > 3 or diff == 0:
            return False
        if negative is None:
            negative = diff < 0
            continue
        if (negative and diff > 0) or (not negative and diff < 0):
            return False
    return True
    

def part1(data):
    return sum(map(_is_valid, data))
    

def _gen_rows(row):
    yield row
    for i in range(len(row)):
        yield row[:i] + row[i + 1:]

def _any_is_valid(row):
    for r in _gen_rows(row):
        if _is_valid(r):
            return True
    return False


def part2(data):
    return sum(map(_any_is_valid, data))

def _main():
    data = _read_data()

    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    _main()