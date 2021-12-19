from functools import reduce
from functools import reduce
from itertools import accumulate, product
from operator import add

from pyaoc2019.utils import read_file, chunks, timer

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    res = [[int(c) for c in row] for row in read_file(filename, 2021)]
    return res


def part1(grid):
    end_r, end_c = len(grid), len(grid[0])
    table = [[0] * end_c for _ in range(end_r)]
    table[0] = list(accumulate(grid[0]))
    T = next(zip(*grid))
    for i, v in enumerate(accumulate(T)):
        table[i][0] = v

    for r, c in product(range(1, end_r), range(1, end_c)):
        best = min(table[r - 1][c], table[r][c - 1])
        table[r][c] = best + grid[r][c]

    return table[-1][-1] - grid[0][0]


def _inc_tile(tile, num):
    return [[(c + num - 1) % 9 + 1 for c in row] for row in tile]


def _stitch(tiles: dict):
    res = []
    for ts in chunks(tiles.values(), 5):
        res.extend(reduce(add, (t[r] for t in ts))
                   for r in range(len(ts[0])))
    return res


def _display(grid):
    for l in grid:
        print(''.join(map(str, l)))


@timer
def part2(tile):
    tiles = {(r, c): _inc_tile(tile, r + c)
             for r, c in product(range(5), repeat=2)}
    grid = _stitch(tiles)
    return part1(grid)


def __main():
    # TODO: issue is that you can move up/down/left/right not just down and right
    # TODO: use A*
    # TODO: problem is that down/right only works for test solution
    grid = parse_data(debug=True)
    print(part1(grid))
    print(part2(grid))


if __name__ == '__main__':
    __main()
