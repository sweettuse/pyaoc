from itertools import accumulate, cycle

import pyaoc2019.utils as U

__author__ = 'acushner'


def aoc01_a(data):
    return sum(map(int, data))


def aoc01_b(data):
    seen = {0}
    for v in accumulate(map(int, cycle(data))):
        if v in seen:
            return v
        seen.add(v)


def __main():
    data = U.read_file(1, 2018)
    print(aoc01_a(data))
    print(aoc01_b(data))


if __name__ == '__main__':
    __main()
