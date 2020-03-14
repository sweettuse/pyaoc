__author__ = 'acushner'

from pyaoc2019.utils import Coord

from itertools import count, product

from cytoolz.itertoolz import first

location = 312051


def get_square_side(data):
    return first(i for i in count(1, 2) if i ** 2 >= data)


def aoc03_a(location):
    """only works where the location doesn't 'wrap around' from the bottom of the square

    e.g., based on this input:

    17  16  15  14  13
    18   5   4   3  12
    19   6   1   2  11
    20   7   8   9  10
    21  22  23---> ...

    [21, 25], [7, 9], and [1] would work, but 17, e.g, would not
    """
    side = get_square_side(location)
    end = side ** 2
    ec = side // 2
    end_coord = Coord(ec, ec)
    end_coord -= Coord(end - location, 0)
    return end_coord.manhattan


def _gen_coords():
    """
    create coords in the order they would appear in the data structure in the docstring in aoc03_a
    coords:
    0, 0

    1, 0
    1, 1
    0, 1
    -1, 1
    -1, 0
    -1, -1,
    0, -1
    1, -1

    """
    for i, size in zip(count(1), count(3, 2)):
        cur = Coord(i, 1 - i)  # the start of the next outer square (bottom right corner)
        cur_offset = Coord(0, 1)
        offset_dict = {
            Coord(i, i): Coord(-1, 0),
            Coord(-i, i): Coord(0, -1),
            Coord(-i, -i): Coord(1, 0),
        }
        yield cur
        n_elements = size ** 2 - (size - 2) ** 2
        for _ in range(n_elements - 1):
            cur += cur_offset
            yield cur
            cur_offset = offset_dict.get(cur, cur_offset)


def aoc03_b(value):
    """generate square with neighbors to figure out first > value occurrence

    represent square as dict of {coord: value}
    """
    offsets = {Coord(x, y) for x, y in product(range(-1, 2), range(-1, 2))}
    grid = {Coord(0, 0): 1}

    def _get_neighbor_vals(_c):
        return sum(grid.get(_c + o, 0) for o in offsets)

    for c in _gen_coords():
        v = grid[c] = _get_neighbor_vals(c)
        if v > value:
            return v


def __main():
    print(aoc03_a(location))
    print(aoc03_b(location))


if __name__ == '__main__':
    __main()
