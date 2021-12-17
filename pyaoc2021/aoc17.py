from collections import defaultdict
from functools import cache
from itertools import count
from operator import itemgetter

from pyaoc2019.utils import read_file, mapt, timer
from typing import NamedTuple, Counter

__author__ = 'acushner'


def parse_data(*, debug=False):
    xs, xe = 20, 30
    ys, ye = -10, -5
    if not debug:
        xs, xe = 185, 221
        ys, ye = -122, -74

    return {(x, y) for x in range(xs, xe + 1) for y in range(ys, ye + 1)}


def _gauss_sum(n):
    return n * (n + 1) // 2


def _max_height(top, bottom):
    res = -float('inf')
    for starting_v in range(1000):
        cur = max_height = _gauss_sum(starting_v)
        for n in count(-1, -1):
            cur += n
            if bottom <= cur <= top:
                res = max(res, max_height)
                break
            if cur < bottom:
                break
    return res


def part1(target):
    ys = {y for _, y in target}
    bottom, top = min(ys), max(ys)
    return _max_height(top, bottom)


@cache
def _y_pos(vel, n):
    return _gauss_sum(vel) - _gauss_sum(vel - n)


@cache
def _x_pos(vel, n):
    return _gauss_sum(vel) - _gauss_sum(max(vel - n, 0))


@timer
def part2(target):
    right = max(x for x, _ in target)
    bottom = min(y for _, y in target)

    total = 0
    seen = set()
    for n in range(1, 248):  # number loosely derived from previous step
        for x_vel in range(1, right + 1):
            xp = _x_pos(x_vel, n)
            for y_vel in range(bottom, 124):  # number loosely derived from previous step
                yp = _y_pos(y_vel, n)
                if (xp, yp) in target and (x_vel, y_vel) not in seen:
                    total += 1
                    seen.add((x_vel, y_vel))
    return total


def __main():
    data = parse_data(debug=False)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
