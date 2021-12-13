from itertools import starmap

from pyaoc2019.utils import read_file, mapt, exhaust
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = iter(read_file(filename, 2021))
    points = set()
    while l := next(data):
        points.add(eval(l))

    folds = []
    for l in data:
        s = l.rsplit(' ')[-1]
        fold_line, val = s.split('=')
        folds.append((fold_line, int(val)))
    return points, folds


def fold_x(points, v):
    for x, y in points:
        if x == v:
            continue
        if x < v:
            yield x, y
        else:
            yield 2 * v - x, y


def fold_y(points, v):
    for x, y in points:
        if y == v:
            continue

        if y < v:
            yield x, y
        else:
            yield x, 2 * v - y


fold_funcs = dict(x=fold_x, y=fold_y)


def part1(points, folds):
    axis, val = folds[0]
    return len(set(fold_funcs[axis](points, val)))


def _display(points):
    max_x = max(x for x, _ in points)
    max_y = max(y for _, y in points)
    board = [[' '] * (max_x + 1) for _ in range(max_y + 1)]
    for x, y in points:
        board[y][x] = '\u2589'
    exhaust(print, map(''.join, board))


def part2(points, folds):
    for axis, val in folds:
        points = set(fold_funcs[axis](points, val))
    _display(points)


def __main():
    points, folds = parse_data(debug=False)
    print(part1(points, folds))
    part2(points, folds)


if __name__ == '__main__':
    __main()
