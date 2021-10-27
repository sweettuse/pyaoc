__author__ = 'acushner'

# https://leetcode.com/problems/perfect-squares/
from functools import lru_cache
from itertools import count, takewhile

from pyaoc2019.utils import timer


@timer
def num_squares(n):
    squares = (v ** 2 for v in count(1))
    squares = list(takewhile(lambda s: s <= n, squares))
    squares.reverse()

    @lru_cache(None)
    def _num_squares(cur=n, idx=0):
        res = []
        for i in range(idx, len(squares)):
            if squares[i] <= cur:
                mult, rem = divmod(cur, squares[i])
                res.append(mult + _num_squares(rem, i))
        return min(res, default=0)

    try:
        return _num_squares()
    finally:
        print(_num_squares.cache_info())


def __main():
    print(num_squares(72839))
    pass


if __name__ == '__main__':
    __main()
