__author__ = 'acushner'

import asyncio
from functools import lru_cache, wraps
from typing import List
from math import factorial
from collections import Counter, defaultdict
from math import prod
from asyncstdlib import lru_cache as alru_cache

# https://leetcode.com/problems/combination-sum-iv/
from pyaoc2019.utils import localtimer, timer


def acache(func):
    cache = {}
    in_progress = object()
    waiting = defaultdict(asyncio.Event)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        key = args, tuple(kwargs.items())
        if key in cache:
            v = cache[key]
            if v is in_progress:
                await waiting[key].wait()
            wrapper.hits += 1
            return cache[key]
        cache[key] = in_progress
        wrapper.misses += 1
        res = cache[key] = await func(*args, **kwargs)
        if ev := waiting.get(key):
            ev.set()
            del waiting[key]
        return res

    wrapper.hits = 0
    wrapper.misses = 0
    wrapper.cache_info = lambda: dict(hits=wrapper.hits, misses=wrapper.misses)

    return wrapper


class Solution:
    @timer
    def combinationSum4(self, nums: List[int], target: int) -> int:
        nums = sorted({n for n in nums if n <= target})
        res = [1] + target * [0]
        for i in range(target + 1):
            for n in nums:
                if n > i:
                    break
                if n == i:
                    res[i] += 1
                else:
                    res[i] += res[i - n]
        return res[target]


class Solution2:
    @timer
    def combinationSum4(self, nums: List[int], target: int) -> int:
        nums = sorted({n for n in nums if n <= target})

        @lru_cache(None)
        def find_combos(t):
            if t == 0:
                return 1
            res = 0
            for n in nums:
                if n > t:
                    break

                if n == t:
                    res += 1
                else:
                    res += find_combos(t - n)
            return res

        res = find_combos(target)
        print(find_combos.cache_info())
        return res


class Solution3:
    @timer
    def combinationSum4(self, nums: List[int], target: int) -> int:
        nums = sorted({n for n in nums if n <= target})

        # @alru_cache(None)
        @acache
        async def find_combos(t):
            if t == 0:
                return 1
            res = 0
            tasks = []
            for n in nums:
                if n > t:
                    break

                if n == t:
                    res += 1
                else:
                    tasks.append(asyncio.create_task(find_combos(t - n)))

            for t in tasks:
                res += await t
            return res

        res = asyncio.run(find_combos(target))
        print(find_combos.cache_info())
        return res


def __main():
    print(Solution().combinationSum4([1, 2, 3], 4))
    print(Solution3().combinationSum4([1, 2, 3], 4))
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
            57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
            84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
    # s2 = Solution2()
    print(80 * '=')
    print(Solution().combinationSum4(nums, 1000))
    print(Solution3().combinationSum4(nums, 1000))


if __name__ == '__main__':
    __main()
