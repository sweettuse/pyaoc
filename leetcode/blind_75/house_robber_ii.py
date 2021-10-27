from functools import lru_cache
from typing import List
from collections import deque


# https://leetcode.com/problems/house-robber-ii/

def _wrap(nums: List[int]) -> int:
    @lru_cache()
    def helper(idx=0):
        if idx >= len(nums):
            return 0
        n = nums[idx]

        return max(n + helper(idx + i) for i in range(2, 4))

    return helper()


class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        nums = deque(nums)
        res = 0
        for _ in range(len(nums)):
            t = nums.pop()
            res = max(res, _wrap(nums))
            nums.append(t)
            nums.rotate(1)

        return res
