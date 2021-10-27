__author__ = 'acushner'

# 8.11 Coins: Given an infinite number of quarters (25 cents), dimes (10 cents), nickels (5 cents), and
# pennies (1 cent), write code to calculate the number of ways of representing n cents.
# Hints: #300, #324, #343, #380, #394
from functools import lru_cache

from pyaoc2019.utils import timer


@timer
def make_change(cents, coins=(25, 10, 5, 1)) -> int:
    @lru_cache(None)
    def _make_change(cur, idx=0):
        if cur < 0:
            return 0

        if cur == 0:
            return 1

        c = coins[idx]

        if idx == len(coins) - 1:
            return int(not cur % c)

        return _make_change(cur - c, idx) + _make_change(cur, idx + 1)

    return _make_change(cents)


def __main():
    import sys
    sys.setrecursionlimit(5000)
    print(make_change(100, coins=(5, 1)))
    print(make_change(4, coins=(5,)))
    print(make_change(5))
    pass


if __name__ == '__main__':
    __main()
