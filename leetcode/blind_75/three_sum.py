from collections import defaultdict
from itertools import combinations
from typing import List
from collections import Counter

__author__ = 'acushner'


# https://leetcode.com/problems/3sum/


def compress_nums(nums):
    c = Counter(nums)
    res = []
    for v, n in c.items():
        res.extend([v] * min(n, 3 if v == 0 else 2))
    return res


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums) < 3:
            return []
        nums = compress_nums(nums)
        c = Counter(nums)
        res = set()
        for n1, n2 in combinations(nums, 2):
            target = -(n1 + n2)
            if target in c:
                used = Counter((n1, n2, target))
                if all(used[n] <= c[n] for n in used):
                    res.add(tuple(sorted((n1, n2, target))))

        return [list(v) for v in res]


def __main():
    nums = [-1, 0, 1, 2, -1, -4]
    print(Solution().threeSum(nums))

    pass


if __name__ == '__main__':
    __main()
