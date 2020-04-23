from itertools import starmap
from operator import mul

from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


def parse_data(data):
    return dict(map(int, kv.split(':')) for kv in data)


def period(r):
    return 2 * (r - 1)


def calc_detections(data, offset=0):
    return [(d, r) for d, r in data.items() if (d + offset) % period(r) == 0]


def delay(data, upper=10000000):
    # TODO: calc using lcm
    return first(offset for offset in range(upper) if not calc_detections(data, offset))


def __main():
    data = parse_data(U.read_file(13, 2017))
    print(sum(starmap(mul, calc_detections(data))))
    with U.localtimer():
        print(delay(data))


if __name__ == '__main__':
    __main()
