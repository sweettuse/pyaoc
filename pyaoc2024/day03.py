from __future__ import annotations
from math import prod
import re
from rich import print

from pyaoc2019.utils import read_file

def _read_data(*, test=False) -> str:
    return '\n'.join(read_file("03.txt" if not test else "03.test.txt"))


    
pattern = r"mul\((\d{1,4}),(\d{1,4})\)"
# pattern = r"mul\("
# pattern = r"mul"

def part1(data):
    return sum(prod(map(int, match.groups())) for match in re.finditer(pattern, data))


def part2(data):
    p = r"don't\(\)|do\(\)|" + pattern
    enabled = True
    res = 0
    for m in re.finditer(p, data):
        s = m.group()
        if s == "do()":
            enabled = True
            continue
        if s == "don't()":
            enabled = False
            continue

        if enabled:
            res += prod(map(int, m.groups()))

    return res

def _main():
    data = _read_data(test=False)

    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    _main()