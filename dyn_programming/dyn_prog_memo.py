__author__ = 'acushner'

# https://www.youtube.com/watch?v=oBt53YbR9Kk
import sys
from functools import lru_cache


@lru_cache(None)
def grid_traveler(m, n):
    if 0 in {m, n}:
        return 0
    elif m == n == 1:
        return 1

    return grid_traveler(m - 1, n) + grid_traveler(m, n - 1)


def can_sum(target, nums):
    @lru_cache(None)
    def _can_sum(target):
        if target == 0:
            return True
        if target < 0:
            return False

        for n in nums:
            if _can_sum(target - n):
                return True
        return False

    nums = set(nums)
    return _can_sum(target)


def how_sum(target, nums):
    @lru_cache(None)
    def _how_sum(target):
        if target == 0:
            return []
        if target < 0:
            return

        for n in nums:
            res = _how_sum(target - n)
            if res is not None:
                return [n] + res
        return

    nums = set(nums)
    return _how_sum(target)


def best_sum(target, nums):
    @lru_cache(None)
    def _best_sum(target):
        if target == 0:
            return []
        if target < 0:
            return None

        res = []
        for n in nums:
            if (cur := _best_sum(target - n)) is not None:
                res.append([n] + cur)
        return min(res, key=len, default=None)

    nums = set(nums)
    return _best_sum(target)


def can_construct(target, words):
    @lru_cache(None)
    def _can_construct(target):
        if not target:
            return True

        for w in words:
            if target.startswith(w) and _can_construct(target[len(w):]):
                return True

        return False

    return _can_construct(target)


def count_construct(target, words):
    @lru_cache(None)
    def _count_construct(target):
        if not target:
            return 1

        return sum(target.startswith(w) and _count_construct(target[len(w):])
                   for w in words)

    return _count_construct(target)


def all_construct(target, words):
    @lru_cache(None)
    def _all_construct(target):
        if not target:
            return [[]]

        res = []
        for w in words:
            if target.startswith(w):
                cur = _all_construct(target[len(w):])
                res.extend([w, *c] for c in cur)
        return res

    return _all_construct(target)


# def test_ac():
#     assert all_construct('jeb', ''.split()) == []
#     assert all_construct('', 'a b c'.split()) == [[]]


def __main():
    # sys.setrecursionlimit(10000)
    # print(grid_traveler(2048, 1024))
    # print(grid_traveler.cache_info())
    print(can_sum(7, [5, 3, 4, 7]))
    print(can_sum(7, [2, 4]))
    print(how_sum(7, [5, 3, 4, 7]))
    print('==========')
    print(best_sum(7, [7, 3, 4]))
    print(best_sum(100, [1, 2, 5, 25]))
    print('==========')
    print(can_construct('abcdef', 'ab abc cd def abcd'.split()))
    print(count_construct('abcdef', 'ab abc cd def abcd abcdef ef'.split()))
    print('==========')
    print(all_construct('abcdef', 'ab abc cd def abcd abcdef ef'.split()))
    print(all_construct('abcdef', 'ab abc cd def abcd'.split()))
    print(all_construct('a', ''.split()))


if __name__ == '__main__':
    __main()
