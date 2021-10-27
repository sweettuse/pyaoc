__author__ = 'acushner'

# 17 .23 Max Black Square: Imagine you have a square matrix, where each cell (pixel) is either black or white
# Design an algorithm to find the maximum subsquare such that all four borders are filled with black
# pixels.
# Hints: #684, #695, #705, #714, #721, #736
from itertools import product, accumulate, chain
from typing import NamedTuple


class Point(NamedTuple):
    r: int
    c: int

    def __add__(self, other):
        return Point(self.r + other[0], self.c + other[1])


class Corners:
    def __init__(self, ul, ll, lr, ur):
        self.ul = ul
        self.ll = ll
        self.lr = lr
        self.ur = ur


def _get_corners(ul, size):
    s1 = size - 1
    ll = ul + (s1, 0)
    lr = ll + (0, s1)
    ur = ul + (0, s1)
    return ll, lr, ur


def _is_square(ul, size):
    pass


def crappy_mbs(m):
    cur_max_size = 0
    s = len(m)

    def _iter_points():
        yield from product(range(s), repeat=2)

    blacks = {(r, c) for r, c in _iter_points() if m[r][c]}

    def _check_square(p, size):
        r, c = p
        if r + size >= s or c + size >= s:
            return False

    pass


def good_mbs(m):

    def _rotate(m):
        return [[row[c] for row in reversed(m)] for c in range(s)]

    def _count_rotated_blacks(m):
        res = [[0] * s for _ in range(s)]
        for i in range(4):
            for r, c in product(range(s), repeat=2):
                res[r][c] += m[r][c]
            m = _rotate(m)
        return res

    def _find_max_square(m):
        return max(v
                   for row in m
                   for v in accumulate(chain([0], row),
                                       lambda cur, nxt: (cur + 1) if nxt == 4 else 0))

    m = [[1, 0],
         [1, 1]]
    s = len(m)
    counted = _count_rotated_blacks(m)
    print(counted)
    return _find_max_square(counted)


def __main():
    print(good_mbs(None))
    pass


if __name__ == '__main__':
    __main()
