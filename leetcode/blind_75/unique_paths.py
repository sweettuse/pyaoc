__author__ = 'acushner'

# https://leetcode.com/problems/unique-paths/
from functools import lru_cache


@lru_cache(None)
def unique_paths(m, n):
    if m == 0 or n == 0:
        return 0
    if m == 1 or n == 1:
        return 1
    return unique_paths(m - 1, n) + unique_paths(m, n - 1)


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        return unique_paths(m, n)


def __main():
    print(Solution().uniquePaths(3, 2))
    print(Solution().uniquePaths(3, 7))
    pass


if __name__ == '__main__':
    __main()
