__author__ = 'acushner'

# https://leetcode.com/problems/split-array-largest-sum/
from itertools import accumulate


def split_array(nums, m):
    if not nums:
        return 0
    mean_per_split = sum(nums) / m
    acc = [0] + list(accumulate(nums))

    return mean_per_split, acc


def __main():
    nums = [7, 2, 5, 10, 8]
    m = 2
    print(split_array(nums, m))


if __name__ == '__main__':
    __main()
