from itertools import count

import pyaoc2019.utils as U

__author__ = 'acushner'


def get_data():
    return [int(v) for v in U.read_file(5, 2017)]


def calc_offset1(offset):
    return offset + 1


def calc_offset2(offset):
    return offset + (-1 if offset >= 3 else 1)


def aoc05(data, calc_offset=calc_offset1):
    cur_idx = 0
    for c in count():
        try:
            offset = data[cur_idx]
        except IndexError:
            return c
        data[cur_idx], cur_idx = calc_offset(offset), cur_idx + offset


def __main():
    print(aoc05(get_data()))
    print(aoc05(get_data(), calc_offset2))


if __name__ == '__main__':
    __main()
