__author__ = 'acushner'

# https://leetcode.com/problems/the-skyline-problem/
from collections import Counter, defaultdict
from heapq import heapify, heappop, heappush


def skyline(buildings):
    counts = defaultdict(Counter)
    for l, r, h in buildings:
        counts[l][h] += 1
        counts[r][h] -= 1

    res = []
    cur = Counter()
    cur_y = None

    for k in sorted(counts):
        cur += counts[k]
        height = max(cur, default=0)
        if height != cur_y:
            res.append([k, height])
            cur_y = height

    return res


def skyline2(buildings):
    points = sorted(p for l, r, h in buildings
                    for p in ((l, h), (r, -h)))
    print(points)
    cur = []
    cur_y = None
    for p in points:
        heappush(cur, p)


def __main():
    buildings = [[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]]
    # buildings = [[0, 2, 3], [2, 5, 3]]
    # buildings = [[0, 2, 3], [2, 5, 3]]
    print(skyline(buildings))
    print(skyline2(buildings))
    pass


if __name__ == '__main__':
    __main()
