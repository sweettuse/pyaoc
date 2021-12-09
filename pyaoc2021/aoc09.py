import heapq
from functools import partial
from math import prod

from pyaoc2019.utils import read_file, mapt, exhaust
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    fn = int(prob_num)
    if debug:
        fn = f'{prob_num}.test'

    topo = [[9] + list(map(int, l.strip())) + [9] for l in read_file(fn, 2021)]
    num_cols = len(topo[0])
    return [[9] * num_cols, *topo, [9] * num_cols]


def _get_surrounding_coords(r, c):
    return {(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}


def _get_minima(data):
    num_rows, num_cols = len(data), len(data[0])
    for r in range(1, num_rows - 1):
        for c in range(1, num_cols - 1):
            if all(data[r][c] < data[nr][nc] for nr, nc in _get_surrounding_coords(r, c)):
                yield r, c


def part1(data):
    return sum(data[r][c] + 1 for r, c in _get_minima(data))


def _get_basin_size(rc, coords):
    to_process = [rc]
    coords.remove(rc)
    size = 0

    while to_process:
        size += 1
        r, c = to_process.pop()
        extant = coords & _get_surrounding_coords(r, c)
        coords -= extant
        to_process.extend(extant)

    return size


def part2(data):
    coords = {(r_idx, c_idx)
              for r_idx, row in enumerate(data)
              for c_idx, v in enumerate(row)
              if v < 9}
    basin_sizes = map(partial(_get_basin_size, coords=coords), _get_minima(data))
    return prod(heapq.nlargest(3, basin_sizes))


def __main():
    data = parse_data(debug=False)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
