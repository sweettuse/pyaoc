from collections import defaultdict
from itertools import count
from operator import itemgetter

from pyaoc2019.utils import read_file, mapt
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


def _min_max_steps(left, right):
    min_steps = max_steps = None
    print(left, right)

    for i, n in enumerate(count()):
        total = _gauss_sum(n)
        if not min_steps and total >= left:
            min_steps = i
        if not max_steps and total > right:
            max_steps = i - 1
            break

    return min_steps, max_steps


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


def _y_pos(vel, n):
    neg_comp = n - vel
    return _gauss_sum(vel) - _gauss_sum(-neg_comp)


def _valid_x_steps(left, right):
    res = defaultdict(int)
    for vel in range(1, right + 1):
        cur_vel = vel
        pos = 0
        for n in count(1):
            pos += cur_vel
            if left <= pos <= right:
                res[n] += 1
            if pos > right:
                break
            cur_vel -= 1
            if cur_vel < 0:
                break
    return res


def _x_pos(vel, n):
    return _gauss_sum(vel) - _gauss_sum(max(vel - n, 0))


def part2(target):
    xs = {x for x, _ in target}
    ys = {y for _, y in target}
    left, right = min(xs), max(xs)
    top, bottom = max(ys), min(ys)
    print('lr', left, right)
    print('tb', top, bottom)

    total = 0
    print(_valid_x_steps(left, right))

    seen = set()
    for n in range(1, 300):
        for x_vel in range(1, right + 1):
            for y_vel in range(bottom, 130):
                xp = _x_pos(x_vel, n)
                yp = _y_pos(y_vel, n)
                if (xp, yp) in target and (x_vel, y_vel) not in seen:
                    total += 1
                    seen.add((x_vel, y_vel))
    return total


def _test():
    # for n in range(12):
    #     print(_x_pos(7, n))

    # print(_gauss_sum(0))
    # print(_gauss_sum(0 - 3))
    for n in range(13):
        print(_y_pos(5, n))


def __main():
    # return _test()
    data = parse_data(debug=False)
    # print(data)

    print(part1(data))
    print(part2(data))
    print(_gauss_sum(-1))


if __name__ == '__main__':
    __main()
