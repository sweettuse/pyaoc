__author__ = 'acushner'

from bisect import bisect_left
from itertools import product
from random import randint

from pyaoc2019.utils import timer


def my_bisect(l, target):
    start, end = 0, len(l)
    while start < end:
        mid = (start + end) // 2
        if target <= l[mid]:
            end = mid
        else:
            start = mid + 1
    return (start + end) // 2


print(my_bisect([1, 3, 5, 7], 7))


@timer
def smallest_diff(l1, l2):
    return min(abs(v1 - v2) for (v1, v2) in product(*map(set, (l1, l2))))


@timer
def smallest_diff2(l1, l2):
    l1, l2 = map(sorted, map(set, (l1, l2)))
    res = float('inf')
    for v in l1:
        idx = my_bisect(l2, v)
        if idx:
            res = min(abs(v - l2[idx - 1]), res)
        if idx < len(l2):
            res = min(abs(v - l2[idx]), res)
    return res


@timer
def smallest_diff3(l1, l2):
    # note: from solution, only need to sort one, the smaller one
    l1, l2 = map(set, (l1, l2))

    if len(l2) > len(l1):
        l1, l2 = l2, l1
    l2 = sorted(l2)
    print(len(l1), len(l2))

    res = float('inf')
    for v in l1:
        idx = bisect_left(l2, v)
        if idx:
            res = min(abs(v - l2[idx - 1]), res)
        if idx < len(l2):
            res = min(abs(v - l2[idx]), res)
    return res


def gen_vals(size):
    return [randint(-1000000, 1000000) for _ in range(size)]


def __main():
    size = 3
    l1 = gen_vals(10000)
    l2 = gen_vals(1000)
    print(smallest_diff(l1, l2))
    print(smallest_diff2(l1, l2))
    print(smallest_diff3(l1, l2))
    pass


if __name__ == '__main__':
    __main()
