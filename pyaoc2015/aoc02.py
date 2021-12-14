from itertools import starmap

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    parse = lambda l: tuple(sorted(map(int, l.split('x'))))
    return [parse(l) for l in read_file(filename, 2015)]


def part1(data):
    def _area(l, w, h):
        return 3 * l * w + 2 * l * h + 2 * w * h

    return sum(starmap(_area, data))


def part2(data):
    def _ribbon(l, w, h):
        return 2 * l + 2 * w + l * w * h
    return sum(starmap(_ribbon, data))


def __main():
    data = parse_data(debug=False)
    print(data)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
