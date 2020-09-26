__author__ = 'acushner'

from typing import List


# https://leetcode.com/explore/challenge/card/september-leetcoding-challenge/557/week-4-september-22nd-september-28th/3473/

def findPoisonedDuration(time_series: List[int], duration: int) -> int:
    intervals = ((t, t + duration) for t in time_series)
    total = 0
    (s, e) = next(intervals)
    for cs, ce in intervals:
        if cs > e:
            total += e - s
            s, e = cs, ce
        elif ce <= e:
            continue
        else:
            e = ce

    return total + e - s


# right answer:

def findPoisonedDuration(time_series: List[int], duration: int) -> int:
    if not time_series:
        return 0
    return duration + sum(min(b - a, duration) for a, b in zip(time_series, time_series[1:]))


def __main():
    print(findPoisonedDuration([1, 2, 7], 2))
    pass


if __name__ == '__main__':
    __main()
