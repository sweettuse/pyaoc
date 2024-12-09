
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from enum import Enum
from functools import partial
from itertools import pairwise
from operator import add, mul
from typing import NamedTuple

from rich import print

from pyaoc2019.utils import read_file

@dataclass
class Eq:
    target: int
    nums: list[int]

    def __getitem__(self, idx) -> int | None:
        if idx >= len(self.nums):
            return None
        return self.nums[idx]

def _read_data(*, test: bool) -> list[Eq]:
    fname = "07.test.txt" if test else "07.txt"
    res = []
    for row in read_file(fname):
        t, rest = row.split(':')
        res.append(Eq(int(t), list(map(int, rest.split()))))
    return res


ops = ()
def _is_valid(eq: Eq, ops=(add, mul)) -> bool:
    def _helper(cur, idx) -> bool:
        if cur > eq.target:
            return False
        if (nxt := eq[idx]) is None:
            return cur == eq.target
        return any(_helper(op(cur, nxt), idx + 1) for op in ops)
    
    return _helper(eq[0], 1)

    

def part1(data) -> int:
    return sum(eq.target for eq in filter(_is_valid, data))


    
def part2(data) -> int:
    def _concat(a, b):
        return int(str(a) + str(b))
    
    _iv = partial(_is_valid, ops=(add, mul, _concat))
    return sum(eq.target for eq in filter(_iv, data))


def _main():
    data = _read_data(test=False)
    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    _main()
