from copy import deepcopy
from functools import lru_cache
from itertools import product, count

from pyaoc2019.utils import read_file, mapt, exhaust
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    grid = [[int(v) for v in l] for l in read_file(filename, 2021)]

    return grid


def _offsets():
    offs = -1, 0, 1
    offsets = {(r_off, c_off) for r_off in offs for c_off in offs} - {(0, 0)}
    res = {(r, c): {(r + r_off, c + c_off)
                    for r_off, c_off in offsets}
           for r, c in all_points}

    for k in res:
        res[k] &= all_points

    return res


all_points = set(product(range(10), repeat=2))
offsets = _offsets()


def _inc_points(grid, points):
    for r, c in points:
        grid[r][c] += 1


def _reset(grid, points):
    for r, c in points:
        grid[r][c] = 0


def _should_flash(grid, points):
    return {(r, c) for r, c in points if grid[r][c] > 9}


def _one_round(grid):
    _inc_points(grid, all_points)
    possibles = all_points
    already_flashed = set()

    while to_check := possibles - already_flashed:
        possibles = set()
        for rc in (to_flash := _should_flash(grid, to_check)):
            _inc_points(grid, offsets[rc])
            possibles |= offsets[rc]

        already_flashed |= to_flash

    _reset(grid, already_flashed)
    return len(already_flashed)


def part1(grid, num_steps=100):
    grid = deepcopy(grid)
    return sum(_one_round(grid) for _ in range(num_steps))


def part2(grid):
    grid = deepcopy(grid)
    for n in count():
        if _one_round(grid) == 100:
            return n + 1


def __main():
    print(grid := parse_data(debug=False))
    print(part1(grid))
    print(part2(grid))


if __name__ == '__main__':
    __main()
