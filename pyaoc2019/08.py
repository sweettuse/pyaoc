from collections import Counter
from itertools import dropwhile

from cytoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'

data = [int(v) for v in first(U.read_file('08'))]
width = 25
height = 6
layer_size = width * height
layers = list(U.chunks(data, layer_size))


def aoc8_a():
    least_zeroes = min((Counter(l) for l in layers), key=lambda c: c[0])
    return least_zeroes[1] * least_zeroes[2]


def aoc8_b():
    pixels = (first(dropwhile(lambda v: v == 2, pixel_vals)) for pixel_vals in zip(*layers))
    return U.chunks(pixels, width)


def __main():
    print(aoc8_a())
    print()
    for row in aoc8_b():
        print(''.join('X' if v else ' ' for v in row))


if __name__ == '__main__':
    __main()
