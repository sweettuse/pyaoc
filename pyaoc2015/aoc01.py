from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    replace = {'(': 1, ')': -1}
    return [replace[c] for c in read_file(filename, 2015)[0]]


def part1(data):
    return sum(data)


def part2(data):
    cur = 0
    for i, v in enumerate(data, 1):
        cur += v
        if cur == -1:
            return i



def __main():
    data = parse_data(debug=False)
    print(data)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
