from math import prod

from pyaoc2019.colors.tile_utils import RC
from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


def read_data():
    res = set()
    data = read_file(3, 2020)
    for r_idx, row in enumerate(data):
        for c_idx, v in enumerate(row):
            if v == '#':
                res.add(RC(r_idx, c_idx))
    return res, RC(len(data), len(data[0]))


board, size = read_data()


def part1(slope=RC(1, 3)):
    cur = RC(0, 0)
    num_rows = (size.r - 1) // slope.r
    total = 0

    for _ in range(num_rows):
        cur += slope
        total += (cur % size in board)
    return total


def part2():
    slopes = RC(1, 1), RC(1, 3), RC(1, 5), RC(1, 7), RC(2, 1)
    return prod(map(part1, slopes))


@timer
def __main():
    print(part1())
    print(part2())


# 294
# 5774564250
# '__main' took 0.0028050290000000005 seconds


if __name__ == '__main__':
    __main()
