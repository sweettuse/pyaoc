__author__ = 'acushner'

from functools import lru_cache
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        @lru_cache()
        def helper(idx=0):
            if idx >= len(nums):
                return 0
            n = nums[idx]

            return max(n + helper(idx + i) for i in range(2, 4))

        return max(helper(0), helper(1))

def __main():
    pass


if __name__ == '__main__':
    __main()
