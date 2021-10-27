from typing import List

__author__ = 'acushner'


# 8.3 Magic Index: A magic index in an array A [ 0 ••• n -1] is defined to be an index such that A[ i] =
# i. Given a sorted array of distinct integers, write a method to find a magic index, if one exists, in
# array A.
# FOLLOW UP
# What if the values are not distinct?


def magic_index(l: List[int], start=None, end=None):
    if start is None:
        start, end = 0, len(l)
    while start != end:
        mid = (start + end) // 2
        if l[mid] == mid:
            return mid
        if l[mid] > mid:
            end = mid
        else:
            start = mid


def __main():
    l = [0, 2, 3, 4]
    print(magic_index(l))
    l = [4, 4, 4, 4, 4]
    print(magic_index(l))
    pass


if __name__ == '__main__':
    __main()
