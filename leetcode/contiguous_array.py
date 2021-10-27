__author__ = 'acushner'

# https://leetcode.com/problems/contiguous-array/
from collections import defaultdict
from itertools import accumulate, chain


def cont_array(nums):
    nums = chain([0], accumulate(1 if v else -1 for v in nums))
    res = {}
    for i, n in enumerate(nums):
        if n in res:
            res[n][1] = i
        else:
            res[n] = [i, i]
    return max(v[1] - v[0] for v in res.values())


def __main():
    nums = [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    # nums = [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0]
    print(cont_array(nums))
    pass


if __name__ == '__main__':
    __main()
