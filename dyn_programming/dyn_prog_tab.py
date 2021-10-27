__author__ = 'acushner'

# https://www.youtube.com/watch?v=oBt53YbR9Kk
# tabulation version vs prev memoize version
from math import prod
from operator import getitem, itemgetter
from typing import Optional

from pyaoc2019.utils import exhaust


def fib(n):
    res = [0, 1, *[None] * (n - 1)]
    for i in range(2, n + 1):
        res[i] = res[i - 1] + res[i - 2]

    return res


def grid_traveler(m, n):
    table = [[0] * (n + 1)
             for _ in range(m + 1)]
    table[1][1] = 1
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            table[r][c] += table[r - 1][c] + table[r][c - 1]

    return table[-1][-1]


def can_sum(target, nums):
    table = [0] * (target + 1)
    table[0] = 1
    nums = sorted(nums)
    for t in range(1, target + 1):
        for n in nums:
            rem = t - n
            if rem < 0:
                break
            table[t] |= table[rem]
    return table


def can_sum_right(target, nums):
    table = [0] * (target + 1)
    table[0] = 1
    nums = sorted(nums)
    for i in range(0, target + 1):
        if table[-1]:
            return True

        if not table[i]:
            continue

        for n in nums:
            if (cur := i + n) > target:
                break
            table[cur] |= table[i]

    return table


def how_sum(target, nums):
    table = [None for _ in range(target + 1)]
    table[0] = []
    nums = sorted(nums)
    for i in range(target + 1):
        if table[-1]:
            return table

        if table[i] is None:
            continue

        for n in nums:
            if (cur := i + n) > target:
                break
            table[cur] = table[i] + [n]
    return table


def best_sum(target, nums):
    table: list[Optional[list[int]]] = [None] * (target + 1)
    table[0] = []
    nums = sorted(nums)
    for i in range(target + 1):
        if table[-1]:
            return table[-1]

        if table[i] is None:
            continue

        for n in nums:
            if (cur := i + n) > target:
                break
            if table[cur] is None or len(table[cur]) > len(table[i]):
                table[cur] = table[i] + [n]

    return table[-1]


def can_construct(target, words):
    table = [0] * (len(target) + 1)
    table[0] = 1
    for i in range(len(target)):
        if table[-1]:
            return True

        if not target[i]:
            continue

        cur = target[i:]

        for w in words:

            if cur.startswith(w) and (end_idx := i + len(w)) <= len(target):
                table[end_idx] = 1

    return table


def count_construct(target, words):
    table = [0] * (len(target) + 1)
    table[0] = 1
    for i in range(len(target)):
        if not table[i]:
            continue

        cur = target[i:]

        for w in words:

            if cur.startswith(w) and (end_idx := i + len(w)) <= len(target):
                table[end_idx] += table[i]

    return table


def all_construct(target, words):
    table = [None] * (len(target) + 1)
    table[0] = []
    for i in range(len(target)):
        if table[i] is None:
            continue

        cur = target[i:]

        for w in words:
            if cur.startswith(w) and (end_idx := i + len(w)) <= len(target):
                if table[end_idx] is None:
                    table[end_idx] = [[w]]
                else:
                    table[end_idx] += [[*c, w] for c in table[i]]

    return table[-1]


def len_of_lis(nums):
    """https://leetcode.com/problems/longest-increasing-subsequence"""
    tab = [1] * len(nums)
    for cur in range(len(nums)):
        for i in range(cur):
            if nums[cur] > nums[i] and tab[i] >= tab[cur]:
                tab[cur] = tab[i] + 1
            # print(cur, i, nums[cur], nums[i], nums, tab)
    return max(tab)


# print(len_of_lis([3, 4, 1, 2, 3]))
print(len_of_lis([3, 5, 8, 6, 7]))


def burst_balloons(nums):
    """https://leetcode.com/problems/burst-balloons/"""

    def _calc_val(idx):
        pre = nums[idx - 1] if idx > 0 else 1
        post = nums[idx + 1] if idx < len(nums) - 1 else 1
        cur = nums[idx]
        return pre * post * cur

    res = 0
    while nums:
        v, i = min((v, i) for i, v in enumerate(nums))
        res += _calc_val(i)
        nums.pop(i)
    return res


print(burst_balloons([3, 1, 5, 8]))


def sat(mat):
    num_r = len(mat)
    num_c = len(mat[0])
    tab = [[0] * (num_c + 1) for _ in range(num_r + 1)]


def __main():
    return
    print(fib(6))
    print(grid_traveler(18, 18))
    print(can_sum(7, [3, 4, 7]))
    print(can_sum_right(7, [5, 3, 4]))
    print(how_sum(7, [5, 3, 4]))
    print(how_sum(8, [5, 3, 4, 2]))
    print('=======================')
    print(best_sum(100, [1, 2, 5, 25]))
    print('=======================')
    print(can_construct('abcdef', 'ab abc cd def abcd'.split()))
    print(count_construct('abcdef', 'ab abc cd def abcd abcdef'.split()))
    print(all_construct('abcdef', 'ab abc c cd def abcd ef abcdef'.split()))
    nums = [4, 3, 2, 3, 5, 2, 1]

    print(sum(nums) / len(nums))


if __name__ == '__main__':
    __main()
