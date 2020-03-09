from cytoolz.itertoolz import first
from collections import deque

import pyaoc2019.utils as U

__author__ = 'acushner'

data = list(map(int, first(U.read_file(1, 2017))))


def aoc01(rotate: int):
    if rotate is None:
        rotate = len(data) // 2
    d_r = deque(data)
    d_r.rotate(rotate)
    return sum(i for i, j in zip(data, d_r) if i == j)


def __main():
    print(aoc01(1))
    print(aoc01(None))


if __name__ == '__main__':
    __main()
