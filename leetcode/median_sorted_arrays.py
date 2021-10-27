__author__ = 'acushner'

# https://leetcode.com/problems/median-of-two-sorted-arrays/
from bisect import bisect_left
from random import randint, seed


def create_sorted(size=4):
    return sorted(randint(10, 99) for _ in range(size))


from statistics import median


def __main():
    seed(-14)
    size = 9
    l1 = create_sorted(size)
    l2 = create_sorted(size)
    mid1 = l1[size // 2]
    mid2 = l2[size // 2]

    for val in l2:
        for v in (val, val + .5):
            idx1 = bisect_left(l1, v)
            idx2 = bisect_left(l2, v)
            print(idx1, idx2)
            if idx1 + idx2 == 9:
                print('success', idx1, idx2, v)
                break
    else:
        print('missed')

    print('=============')

    print(l1)
    print(l2)
    print(median(l1), median(l2), median(sorted(l1 + l2)))
    print(sorted(l1 + l2))

    pass


if __name__ == '__main__':
    __main()
