__author__ = 'acushner'

# https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
from functools import lru_cache


def longest_inc_path(mat):
    num_rows = len(mat)
    num_cols = len(mat[0])

    def _get_next(r, c):
        val = mat[r][c]
        around = (r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)
        for r, c in around:
            if 0 <= r < num_rows and 0 <= c < num_cols and mat[r][c] > val:
                yield r, c

    @lru_cache(None)
    def _lip(r, c):
        return 1 + max((_lip(*rc) for rc in _get_next(r, c)), default=0)

    return max(_lip(r, c) for r in range(num_rows) for c in range(num_cols))


def __main():
    matrix = [[9, 9, 4], [6, 6, 8], [2, 1, 1]]
    matrix = [[3, 4, 5], [3, 2, 6], [2, 2, 1]]
    print(longest_inc_path(matrix))
    pass


if __name__ == '__main__':
    __main()
