from __future__ import annotations
from collections import Counter

from pyaoc2019.utils import read_file

def _read_data() -> tuple[list[int], list[int]]:
    l1, l2 = [], []
    for r in read_file("01.txt"):
        i1, i2 = map(int, r.split())
        l1.append(i1)
        l2.append(i2)
    return l1, l2

def part1(data):
    l1, l2 = data
    l1 = sorted(l1)
    l2 = sorted(l2)
    return sum(abs(i2 - i1) for i1, i2 in zip(l1, l2))

def part2(data):
    l1, l2 = data
    c = Counter(l2)
    return sum(i1 * c.get(i1, 0) for i1 in l1)

def _main():
    data = _read_data()

    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    _main()