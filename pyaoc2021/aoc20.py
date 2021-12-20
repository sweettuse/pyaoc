from itertools import product

from pyaoc2019.utils import read_file, mapt, exhaust, timer
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = iter(read_file(filename, 2021))
    l = next(data)
    algo = [1 if c == '#' else 0 for c in l]
    next(data)
    img = list(data)

    on = {(r, c)
          for r, row in enumerate(img)
          for c, v in enumerate(row)
          if v == '#'}

    num_rows, num_cols = len(img), len(img[0])
    return algo, on, num_rows, num_cols


offsets = list(product(range(-1, 2), repeat=2))


def _display(start_r, start_c, end_r, end_c, on):
    res = []
    for r in range(start_r, end_r + 1):
        res.append([])
        cur = res[-1]
        for c in range(start_c, end_c + 1):
            cur.append('.#'[(r, c) in on])
    print('===========')
    exhaust(print, map(''.join, res))
    print('===========')


def _process_round(algo, on, num_rows, num_cols, origin_r=0, origin_c=0, outside_default=0):
    add = 1
    start_r = origin_r - add
    end_r = num_rows + add
    start_c = origin_c - add
    end_c = num_cols + add

    def _point_val():
        cur_r, cur_c = r + r_off, c + c_off
        if (outside_default
                and (cur_r < origin_r
                     or cur_c < origin_c
                     or cur_r >= num_rows
                     or cur_c >= num_cols)):
            return 1
        return (cur_r, cur_c) in on

    new_ons = set()
    for r in range(start_r, end_r + 1):
        for c in range(start_c, end_c + 1):
            idx = 0
            for r_off, c_off in offsets:
                idx <<= 1
                idx += _point_val()
            if algo[idx]:
                new_ons.add((r, c))

    return new_ons


@timer
def parts1and2(algo, on, num_rows, num_cols, repeat=2):
    cur_outside = 0
    start_r = start_c = 0
    for _ in range(repeat):
        on = _process_round(algo, on, num_rows, num_cols, start_r, start_c, cur_outside)
        cur_outside ^= algo[0]
        num_rows += 1
        num_cols += 1
        start_r -= 1
        start_c -= 1

    return len(on)


def __main():
    t = algo, on, num_rows, num_cols = parse_data(debug=False)
    print(parts1and2(*t, 2))
    print(parts1and2(*t, 50))
    # 4942 too low
    # print(on, num_rows, num_cols)
    # print(part1(data))
    # print(part2(data))


if __name__ == '__main__':
    __main()
