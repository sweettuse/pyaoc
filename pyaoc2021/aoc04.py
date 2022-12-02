__author__ = 'acushner'

from collections import defaultdict
from itertools import chain, count
from typing import Iterable

from pyaoc2019.utils import read_file, mapt

data = read_file('04.test', 2021)
data = read_file(4, 2021)


def parse_data():
    d = iter(data)
    nums = mapt(int, next(d).split(','))
    Board.called.clear()

    cur = []
    res = set()
    next(d)

    def add():
        if cur:
            res.add(Board.from_ints(cur))
            cur.clear()

    for l in d:
        if not l:
            add()
            continue

        cur.append(map(int, l.split()))

    add()
    return nums, res


class Board:
    called = set()

    def __init__(self, rows, cols, nums):
        self.rows = rows
        self.cols = cols
        self.nums = nums

    @classmethod
    def from_ints(cls, s: list[Iterable[int]]):
        rows = list(map(list, s))
        nums = set(chain.from_iterable(rows))
        cols = list(map(set, zip(*rows)))
        rows = list(map(set, rows))
        return cls(rows, cols, nums)

    @property
    def is_winner(self) -> bool:
        for r_or_c in chain(self.rows, self.cols):
            if not r_or_c - self.called:
                return True
        return False

    @property
    def value(self) -> int:
        return sum(self.nums - self.called)


def part1():
    nums, boards = parse_data()
    for n in nums:
        Board.called.add(n)
        for b in boards:
            if b.is_winner:
                return b.value * n


def part2():
    nums, boards = parse_data()
    to_rm = set()
    for n in nums:
        Board.called.add(n)
        to_rm.clear()
        for b in boards:
            if b.is_winner:
                if len(boards) == 1:
                    return b.value * n
                to_rm.add(b)
        boards -= to_rm


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
