__author__ = 'acushner'

from typing import List


# https://leetcode.com/problems/missing-number/


class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        return (n * (n + 1)) // 2 - sum(nums)


def __main():
    pass


if __name__ == '__main__':
    __main()
