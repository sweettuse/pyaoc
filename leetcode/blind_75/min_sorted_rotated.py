__author__ = 'acushner'

# https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
from typing import List


def _find_min_orig(nums, li, ri):
    n = ri - li
    if n <= 1:
        return nums[li]
    if n == 2:
        return min(nums[li:ri])

    mi = (li + ri) // 2
    l, m, r = map(nums.__getitem__, (li, mi, ri - 1))

    if m > r:
        return _find_min_orig(nums, mi, ri)
    return _find_min_orig(nums, li, mi + 1)


def _find_min(nums, l, r):
    if l >= r:
        return nums[l]

    m = (l + r) // 2
    if nums[m] > nums[r]:
        return _find_min(nums, m + 1, r)
    return _find_min(nums, l, m)


class Solution:
    def findMin(self, nums: List[int]) -> int:
        return _find_min(nums, 0, len(nums) - 1)

    def findMinOrig(self, nums: List[int]) -> int:
        return _find_min_orig(nums, 0, len(nums))


def __main():
    vals = [[0, 1, 2, 4, 5, 6, 7],
            [1, 2, 4, 5, 6, 7, 0],
            [2, 4, 5, 6, 7, 0, 1],
            [4, 5, 6, 7, 0, 1, 2],
            [5, 6, 7, 0, 1, 2, 4],
            [6, 7, 0, 1, 2, 4, 5],
            [7, 0, 1, 2, 4, 5, 6]]
    for v in vals:
        print(v, Solution().findMinOrig(v))


if __name__ == '__main__':
    __main()
