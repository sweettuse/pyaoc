__author__ = 'acushner'

# 17 .8 Circus Tower: A circus is designing a tower routine consisting of people standing atop one another's shoulders. For practical and aesthetic reasons, e
# than the person below him or her. Given the heights and weights of each person in the circus, write
# a method to compute the largest possible number of people in such a tower.
# EXAMPLE
# input(ht,wt): (65, 100) (70, 150) (56, 90) (75, 190) (60, 95) (68, 110)
# Output: The longest tower is length 6 and includes from top to bottom:
# (56, 90) (60,95) (65,100) (68,110) (70,150) (75,190)
# Hints: #638, #657, #666, #682, #699
from bisect import bisect_left, bisect_right
from functools import lru_cache
from itertools import count


def _can_stack(hw_low, hw_high):
    return hw_low[0] > hw_high[0] and hw_low[1] > hw_high[1]


def tallest_tower(heights_weights):
    heights_weights.sort(reverse=True)

    @lru_cache
    def _tallest_tower(idx=0):
        if idx >= len(heights_weights):
            return 0

        cur_hw = heights_weights[idx]
        totals = (_tallest_tower(i)
                  for i in range(idx + 1, len(heights_weights))
                  if _can_stack(cur_hw, heights_weights[i]))
        return 1 + max(totals, default=0)

    return max(map(_tallest_tower, range(len(heights_weights))))


def tallest_tower2(heights_weights):
    heights_weights = sorted(heights_weights)
    n = len(heights_weights)
    res = (n + 1) * [0]

    def _find_next_stackable(i):
        cur = heights_weights[i]
        for j in count(bisect_left(heights_weights, cur, 0, i)):
            print('count', cur, i, j)
            if j >= len(heights_weights):
                break
            if _can_stack(cur, heights_weights[j]):
                return j

    for i in range(n - 1, -1, -1):
        above = _find_next_stackable(i)
        print(heights_weights[i], above)
        if above is None:
            res[i] = 1
        else:
            res[i] = 1 + max(res[above], 1)

    print(res)
    return res[0]


def __main():
    hws = [(65, 100), (70, 150), (56, 90), (75, 190), (60, 95), (68, 110)]
    hws = [(65, 100 + n) for n in range(2)]
    hws.append((66, 106))
    hws.sort()
    print(hws)
    hws.sort(reverse=True)
    print(hws)
    # print(bisect_left(hws, (65, 105)))
    # print(bisect_right(hws, (65, 105)))
    # print(tallest_tower(hws))
    # print(tallest_tower2(hws))


if __name__ == '__main__':
    __main()
