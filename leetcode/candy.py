__author__ = 'acushner'

# https://leetcode.com/problems/candy/
# Each child must have at least one candy.
# Children with a higher rating get more candies than their neighbors.
from typing import List


class Solution:
    def candy(self, ratings: List[int]) -> int:
        res = [1]
        for r1, r2 in zip(ratings, ratings[1:]):
            if r1 > r2:
                res.append(res[-1] - 1)
            elif r2 > r1:
                res.append(res[-1] - 1)
            else:
                pass

        pass


def __main():
    ratings = [2, 1, 1, 0, 2]
    res = [1, 0, -1, -2]
    pass


if __name__ == '__main__':
    __main()
