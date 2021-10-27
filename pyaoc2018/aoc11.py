__author__ = 'acushner'

from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from itertools import product, accumulate, starmap
from operator import itemgetter
from typing import List

from more_itertools import first

from pyaoc2019.utils import chunks, localtimer

serial = 8979
size = 300


def _cell_power(r, c) -> int:
    x, y = c, r
    rack_id = x + 10
    power = rack_id * (rack_id * y + serial)
    return (power // 100 % 10) - 5


def _create_power_grid() -> List[List[int]]:
    res = [size * [None] for _ in range(size)]
    for r, c in product(range(size), range(size)):
        res[r][c] = _cell_power(r, c)

    return res


def _calc_local_power(r, c, grid, local_size=3):
    return sum(grid[r][c] for r, c in product(range(r, r + local_size), range(c, c + local_size)))


def part1():
    grid = _create_power_grid()
    res = {(c, r): _calc_local_power(r, c, grid) for r, c in product(range(size - 3), range(size - 3))}
    return ','.join(map(str, first(max(res.items(), key=itemgetter(1)))))


def _part2_helper(r, c, grid):
    print(r, c)
    return (c, r), max((_calc_local_power(r, c, grid, ls), ls) for ls in range(1, size - max(r, c)))


def part2():
    """bad, slow, naive implementation"""
    grid = _create_power_grid()
    with ProcessPoolExecutor() as pool:
        futures = [pool.submit(_part2_helper, r, c, grid) for r, c in product(range(size), range(size))]

    res = dict(f.result() for f in futures if not f.exception())
    print(res)
    return first(max(res.items(), key=itemgetter(1)))


def _part_2_calc_area(r, c, grid_accum):
    prev_r = r - 1
    prev_c = c - 1
    add_back = grid_accum[prev_r][prev_c] if prev_r >= 0 and prev_c >= 0 else 0
    cur_max = float('-inf')

    c_sub = lambda: 0
    r_sub = lambda: 0
    if prev_r >= 0:
        c_sub = lambda: grid_accum[prev_r][cur_c]

    if prev_c >= 0:
        r_sub = lambda: grid_accum[cur_r][prev_c]

    res = None
    for diag in range(0, size - max(r, c)):
        cur_r, cur_c = r + diag, c + diag
        if (cur_total := grid_accum[cur_r][cur_c] - c_sub() - r_sub() + add_back) > cur_max:
            cur_max = cur_total
            res = (c, r), (cur_max, diag + 1)

    return res


def part2_smart():
    """
    take an input grid like
    [
       [1, | 2, 3],
       ----|------
       [4, | 5, 6],
       [7, | 8, 9],
    ]

    to find out what that bottom right quadrant square is ((5, 6), (8, 9))
    the simple calc for this is to add up those numbers
    5 + 6 + 8 + 9 -> 28

    but, for larger squares, this can be very time consuming. so,
    first, transform the grid into one cumulatively summed both horizontally and vertically:
    [
       [ 1, |  3,  6],
       -----|--------
       [ 5, | 12, 21],
       [12, | 27, 45],
    ]

    then, you need to subtract the cumulative components that are "outside" the square you're calculating
    [
       [  1, |  3,  -6],
       ------|---------
       [  5, | 12,  21],
       [-12, | 27, +45],
    ]


    however, this doesn't quite work:

    45 - 6 - 12 -> 27

    the reason is is because the accumulated numbers in the upper left square get counted twice.
    add one copy of the duplicated summed square back in...

    [
       [ +1, |  3,  -6],
       ------|---------
       [  5, | 12,  21],
       [-12, | 27, +45],
    ]

    and you get:
    45 - 6 - 12 + 1 -> 28

    ------------------------------------------

     same grid, different sub-square, just the bottom-right cell this time:

    [
       [ 1,   3, |   6],
       [ 5, +12, | -21],
       ----------|-----
       [12, -27, | +45],
    ]

    45 - 21 - 27 + 12 -> 9, same as the single cell in the original input grid

    essentially, i just reinvented this algo from scratch: https://en.wikipedia.org/wiki/Summed-area_table
    """
    grid = _create_power_grid()
    horiz_accum = map(accumulate, grid)
    grid_accum = list(zip(*map(accumulate, zip(*horiz_accum))))

    res = (_part_2_calc_area(r, c, grid_accum) for r, c in product(range(size), range(size)))
    (x, y), (_, diag) = max(res, key=itemgetter(1))
    return f'{x},{y},{diag}'


def __main():
    print(part1())
    with localtimer():
        print(part2_smart())


if __name__ == '__main__':
    __main()
