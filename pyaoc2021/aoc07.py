from typing import Callable

from more_itertools import first

from pyaoc2019.utils import read_file, mapt

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    fn = int(prob_num)
    if debug:
        fn = f'{prob_num}.test'

    return mapt(int, first(read_file(fn, 2021)).split(','))


def part1(data, cost: Callable[[int, int], int]):
    return min(sum(cost(p, target) for p in data)
               for target in range(min(data), max(data) + 1))


def part2(data):
    def cost(p, target):
        n = abs(p - target)
        return n * (n + 1) // 2

    return part1(data, cost)


def __main():
    data = parse_data(debug=False)
    print(part1(data, lambda p, target: abs(p - target)))
    print(part2(data))


if __name__ == '__main__':
    __main()
