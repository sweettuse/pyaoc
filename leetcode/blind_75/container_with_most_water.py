from typing import List

__author__ = 'acushner'


# https://leetcode.com/problems/container-with-most-water/

def area(h_s, h_e, idx_s, idx_e):
    return min(h_s, h_e) * (idx_e - idx_s)


class Solution:
    def maxArea(self, height: List[int]) -> int:
        return max((idx_e - idx_s) * min(h_s, h_e)
                   for idx_s, h_s in enumerate(height)
                   for idx_e, h_e in enumerate(height))

    def maxArea(self, height: List[int]) -> int:
        res = 0
        for idx_s, h_s in enumerate(height):
            for idx_e in range(idx_s + 1, len(height)):
                h_e = height[idx_e]
                res = max(res, (idx_e - idx_s) * min(h_s, h_e))

        return res

    def maxArea3(self, height: List[int]) -> int:
        idx_s, idx_e = 0, len(height) - 1
        res = 0
        while idx_s < idx_e:
            h_s, h_e = height[idx_s], height[idx_e]
            res = max(res, min(h_s, h_e) * (idx_e - idx_s))
            print(res)
            if h_s < h_e:
                idx_s += 1
            else:
                idx_e -= 1
        return res


# maximize (idx_e - idx_s) * min(height[idx_s], height[idx_e])

def __main():
    print(Solution().maxArea3([1, 2, 4, 3]))
    pass


if __name__ == '__main__':
    __main()
