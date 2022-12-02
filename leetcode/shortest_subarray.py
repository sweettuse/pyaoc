# https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

__author__ = 'acushner'

from collections import deque
from itertools import accumulate, combinations
from typing import List

from more_itertools import first

from pyaoc2019.utils import localtimer


class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        if k in nums:
            return 1
        nums = [0] + list(accumulate(nums))
        for diff in range(1, len(nums)):
            for end in range(diff, len(nums)):
                if nums[end] - nums[end - diff] >= k:
                    return diff
        return -1


def parse_file(fname):
    with open(fname) as f:
        return list(map(eval, f))


def short_sub(nums, k):
    if k in nums:
        return 1
    pos = [i + 1 for i, n in enumerate(nums) if n > 0]
    pos.reverse()
    nums = [0] + list(accumulate(nums))
    return min(
        (
            (end - prev + 1, prev, end)
            for end, prev in combinations(pos, 2)
            if nums[end] - nums[prev - 1] >= k
        ),
        default=-1,
    )


def short_sub2(nums, k):
    if k in nums:
        return 1

    if len(nums) <= 1:
        return -1

    s, e = 0, 1
    cur = nums[s] + nums[e]
    shortest = float('inf')
    short_e = short_s = None
    while True:
        if cur >= k:
            if e - s < shortest:
                shortest = e - s
                short_e = e
                short_s = s

            cur -= nums[s]
            s += 1
        else:
            if e + 1 >= len(nums):
                break
            e += 1
            cur += nums[e]

    if shortest == float('inf'):
        return -1
    return (short_s, short_e), shortest


def shortestSubarray(A, K):
    d = deque([[0, 0]])
    res, cur = float('inf'), 0
    for i, a in enumerate(A):
        cur += a
        print(cur, d)
        while d and cur - d[0][1] >= K:
            print('>= K:', d)
            res = min(res, i + 1 - d.popleft()[0])
        while d and cur <= d[-1][1]:
            print('cur <= end:', d)
            d = deque()
        d.append([i + 1, cur])
    return res if res < float('inf') else -1


n_test = [1, -200, -400, 2, 3, 1, 1, 1]


def __main():
    with localtimer():
        print(short_sub2([2, -1, 2], 3))
        print(short_sub2([1, 2], 4))
        print(short_sub2([1], 1))
        print(shortestSubarray(n_test, 5))
        # (s, e), shortest = short_sub2(*parse_file('/tmp/in3'))
        # print(short_sub(*parse_file('/tmp/in3')))
        # nums, k = parse_file('/tmp/in3')
        # print()
        # print(e - s, s, e, k, sum(nums[s:e + 1]))


if __name__ == '__main__':
    __main()
