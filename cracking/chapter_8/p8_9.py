__author__ = 'acushner'

# 8.9  Parens: Implement an algorithm to print all valid (e.g., properly opened and closed) combinations
# of n pairs of parentheses.
# EXAMPLE
# Input: 3
# Output: ( ( () ) ) , ( () () ) , ( () ) () , () ( () ) , () () ()
from functools import lru_cache

from pyaoc2019.utils import timer


@timer
def parens(n):
    @lru_cache(None)
    def _parens(left, right) -> list[str]:
        if right == 0:
            return ['']

        res = []

        if left != right:
            res.extend(')' + s for s in _parens(left, right - 1))
        if left > 0:
            res.extend('(' + s for s in _parens(left - 1, right))
        return res

    res = _parens(n, n)
    print(_parens.cache_info())
    return res


def __main():
    prev = 1
    for i in range(2, 17):
        print(i, cur := len(parens(i)), cur / prev)
        prev = cur
    pass


if __name__ == '__main__':
    __main()
