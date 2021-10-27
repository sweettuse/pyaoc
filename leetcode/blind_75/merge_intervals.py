__author__ = 'acushner'

# https://leetcode.com/problems/merge-intervals/
from typing import List


class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        if not intervals:
            return intervals
        intervals = iter(intervals)
        res = []
        cur_s, cur_e = next(intervals)
        for s, e in intervals:
            if cur_e < s:
                res.append([cur_s, cur_e])
                cur_s = s
            cur_e = max(cur_e, e)
        res.append([cur_s, cur_e])
        return res


def __main():
    intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
    print(Solution().merge(intervals))
    intervals = [[1, 4], [4, 5]]
    print(Solution().merge(intervals))
    intervals = [[1, 4], [2, 3]]
    print(Solution().merge(intervals))


if __name__ == '__main__':
    __main()
