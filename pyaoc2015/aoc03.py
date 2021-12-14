from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    return read_file(filename, 2015)[0]


move = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


def part1(data):
    cx, cy = (0, 0)
    points = {(cx, cy)}
    for x, y in map(move.__getitem__, data):
        cx += x
        cy += y
        points.add((cx, cy))
    return len(points)


def part2(data):
    points = {(0, 0)}
    for start in range(2):
        cx, cy = (0, 0)
        for x, y in map(move.__getitem__, data[start::2]):
            cx += x
            cy += y
            points.add((cx, cy))
    return len(points)


def __main():
    data = parse_data(debug=False)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
