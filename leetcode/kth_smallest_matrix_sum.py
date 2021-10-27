__author__ = 'acushner'

from functools import lru_cache
from heapq import heapify, heappop, heappush
from itertools import accumulate, combinations, chain
from math import prod
from operator import sub


def kth_smallest_sum(mat, k):
    cur = [r[0] for r in mat]
    diffs = [[r2 - r1 for r1, r2 in zip(row, row[1:])] for row in mat]
    diff_len = len(diffs[0])
    cur_sum = sum(cur)
    if k == 1:
        return cur_sum
    # (next increase, row, col)
    heap = [(row[0], i, 0) for i, row in enumerate(diffs)]
    for _ in range(1, k):
        diff, r, c = heappop(heap)
        cur_sum += diff
        if c + 1 < diff_len:
            heappush(heap, (diffs[r][c + 1], r, c + 1))

    return cur_sum


def gen_perms(num):
    r = list(range(num))

    def _gen_perms(size=len(r)):
        if size == 1:
            yield r.copy()
        else:
            yield from _gen_perms(size - 1)
            for i in range(size - 1):
                offset = 0 if size & 1 else i
                r[offset], r[size - 1] = r[size - 1], r[offset]
                yield from _gen_perms(size - 1)

    return _gen_perms()


def permute_unique(nums):
    return {tuple(nums[i] for i in perm)
            for perm in gen_perms(len(nums))}


def kth_smallest_sum2(mat, k):
    for _, combo in zip(range(k), combinations(*mat)):
        pass
    return sum(combo)


def num_combos(num: str):
    res = [0] * (len(num) + 1)

    @lru_cache(None)
    def _num_combos(idx=0):
        if num[idx] == '0':
            return 0

        pass


def integer_break(n):
    if n <= 3:
        return n - 1
    if n == 4:
        return 4

    threes, rem = divmod(n, 3)

    if rem <= 1:
        return 3 ** (threes - 1) * (3 + rem)
    return 3 ** threes * rem







def __main():
    # return integer_break(8)
    # print(list(gen_perms(3)))
    for i in range(1, 18):
        print(i, integer_break(i))

    # mat = [[1, 3, 11],
    #        [2, 4, 6]]
    # print(kth_smallest_sum2(mat, 5))
    pass


if __name__ == '__main__':
    __main()
