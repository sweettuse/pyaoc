__author__ = 'acushner'

from itertools import chain

from pyaoc2019.utils import read_file, chunks


def _is_triangle(*args):
    a, b, c = sorted(args)
    return a + b > c


def aoc03_a(triangles):
    return sum(_is_triangle(*t) for t in triangles)


def aoc03_b(triangles):
    by_column = zip(*triangles)
    triangles = chunks(chain.from_iterable(by_column), 3)
    return aoc03_a(triangles)


def __main():
    rows = read_file(3, 2016)
    triangles = [tuple(map(int, t.split())) for t in rows]
    print(aoc03_a(triangles))
    print(aoc03_b(triangles))


if __name__ == '__main__':
    __main()
