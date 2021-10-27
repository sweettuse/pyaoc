__author__ = 'acushner'

# https://leetcode.com/problems/minimum-path-sum/
from functools import lru_cache


def _get_valid_neighbors(r, c):
    if r > 0:
        yield r - 1, c
    if c > 0:
        yield r, c - 1


def min_path_sum(g) -> int:
    @lru_cache(None)
    def _path_sum(r, c):
        cur = g[r][c]
        if r == c == 0:
            return g[r][c]
        return cur + min((_path_sum(*p) for p in _get_valid_neighbors(r, c)), default=0)

    n_r = len(g)
    n_c = len(g[0])
    return _path_sum(n_r - 1, n_c - 1)


def __main():
    grid = [[1, 3, 1], [1, 5, 1], [4, 2, 1]]
    print(min_path_sum(grid))
    pass


if __name__ == '__main__':
    __main()
