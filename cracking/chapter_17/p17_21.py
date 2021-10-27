__author__ = 'acushner'

# 17.21 Volume of Histogram: Imagine a histogram (bar graph). Design an algorithm to compute the
# volume of water it could hold if someone poured water across the top. You can assume that each
# histogram bar has width 1.
# EXAMPLE (Black bars are the histogram. Gray is water.)
# Input:{0, 0, 4, 0, 0, 6, 0, 0, 3, 0, 5, 0, 1, 0, 0, 0}
# Output: 26
# Hints:#629,#640,#657,#658,#662,#676,#693,#734,#742
from itertools import accumulate
from operator import itemgetter


def volume(bars):
    def _calc_volume(bars, p_left, p_right):
        min_height = min(p_left[1], p_right[1])
        to_subtract = sum(min(min_height, y) for x, y in bars if p_left[0] <= x < p_right[0])
        return min(p_left[1], p_right[1]) * (p_right[0] - p_left[0]) - to_subtract

    def _volume(bars):
        if len(bars) <= 1:
            return 0

        p_left, p_right = sorted(bars, key=itemgetter(1), reverse=True)[:2]
        if p_left > p_right:
            p_left, p_right = p_right, p_left

        return (_calc_volume(bars, p_left, p_right)
                + _volume(bars[:bars.index(p_left) + 1])
                + _volume(bars[bars.index(p_right):]))

    bars = [(x, y) for x, y in enumerate(bars) if y]
    return _volume(bars)


def volume2(heights):
    l_max = accumulate(heights, max)
    r_max = accumulate(reversed(heights), max)
    return sum(min(l, r) - h for h, l, r in zip(heights, l_max, reversed(list(r_max))))


def __main():
    bars = [0, 0, 4, 0, 0, 6, 0, 0, 3, 0, 5, 0, 1, 0, 0, 0]
    print(bars)
    print(volume(bars))
    print(volume2(bars))
    pass


if __name__ == '__main__':
    __main()
