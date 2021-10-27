__author__ = 'acushner'

from functools import lru_cache
from typing import List


# https://leetcode.com/problems/jump-game-ii/

class Solution:
    def jump(self, nums: List[int]) -> int:

        @lru_cache(len(nums))
        def _jump(idx):
            if idx == len(nums) - 1:
                return 0

            if idx >= len(nums):
                return float('inf')

            max_jump = nums[idx]
            if max_jump <= 0:
                return float('inf')

            possible_jumps = (_jump(idx + i) for i in range(1, max_jump + 1))
            return 1 + min(possible_jumps, default=float('inf'))

        return _jump(0)


class Solution2:
    """from leetcode solutions"""

    def jump(self, nums: List[int]) -> int:
        """greedy algorithm"""
        left = right = jumps = 0
        for i in range(len(nums) - 1):
            right = max(right, i + nums[i])
            if i == left:
                jumps += 1
                left = right
        return jumps


class Solution3:
    """from leetcode solutions"""

    def jump(self, A: List[int]) -> int:
        n = len(A)
        i, j = 0, 0
        ans = 0
        while j < n - 1:
            x = max(k + A[k] for k in range(i, j + 1))
            i, j = j + 1, x
            ans += 1
        return ans


def __main():
    nums = [10, 2, 1, 1]
    nums = [2, 3, 1, 1, 4]
    # nums = [100]
    print(Solution().jump(nums))
    print(Solution2().jump(nums))
    pass


if __name__ == '__main__':
    __main()
