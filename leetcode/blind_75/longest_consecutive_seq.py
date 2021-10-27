__author__ = 'acushner'

from collections import defaultdict
from typing import List


# https://leetcode.com/problems/longest-consecutive-sequence/

def _add(n, nums, res):
    t = res[n]
    if n - 1 in nums:
        t[0] = n - 1
    if n + 1 in nums:
        t[1] = n + 1


def _count(res):
    max_chain = 0
    while res:
        stack = [res.popitem()[1]]
        cur = 0
        while stack:
            cur += 1
            for v in stack.pop():
                if v is not None and v in res:
                    stack.append(res.pop(v))
        max_chain = max(cur, max_chain)
    return max_chain


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums = set(nums)
        res = defaultdict(lambda: [None, None])
        for n in nums:
            _add(n, nums, res)
        return _count(res)


class Solution2:
    def longestConsecutive(self, nums: List[int]) -> int:
        nums = set(nums)
        res = defaultdict(int)

        while nums:
            start = n = nums.pop()
            count = 1
            while True:
                n = n + 1
                if n in res:
                    count += res[n]
                    break

                if n in nums:
                    count += 1
                    nums.remove(n)
                else:
                    break
            res[start] = count
        return max(res.values(), default=0)


class Solution3:
    """with help from https://leetcode.com/problems/longest-consecutive-sequence/discuss/41057/Simple-O(n)-with-Explanation-Just-walk-each-streak"""

    def longestConsecutive(self, nums: List[int]) -> int:
        nums = set(nums)
        max_chain = 0
        for start in nums:
            if start - 1 not in nums:
                end = start + 1
                while end in nums:
                    end += 1
                max_chain = max(max_chain, end - start)
        return max_chain


def __main():
    nums = [100, 4, 200, 1, 3, 2]
    nums = [2]
    # nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
    print(Solution3().longestConsecutive(nums))
    pass


if __name__ == '__main__':
    __main()
