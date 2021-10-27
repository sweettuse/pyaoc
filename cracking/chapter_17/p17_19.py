__author__ = 'acushner'

# 17.19 Missing Two: You are given an array with all the numbers from 1 to N appearing exactly once,
# except for one number that is missing. How can you find the missing number in O(N) time and
# 0(1) space? What if there were two numbers missing?
# Hints: #503, #590, #609, #626, #649, #672, #689, #696, #702, #717
from random import choice
from typing import NamedTuple


def missing_one(l: list[int]):
    total = sum(l)
    n = len(l) + 1
    return (n * (n + 1)) // 2 - total


def missing_two(l: list[int]):
    return missing_m(l, 2)


def fix(l, m):
    mod = len(l) + 1
    for _ in range(m + 1):
        l.pop()
    for i, v in enumerate(l):
        l[i] = v % mod


def missing_m(l: list[int], m):
    l.extend((m + 1) * [0])
    mod = len(l) + 1
    for v in l:
        l[v % mod] += mod
    print(mod, l)

    res = [i for i, v in enumerate(l) if v < mod]
    fix(l, m)
    return res


def __main():
    l = [4, 1]
    print(l)
    print(missing_m(l, 16))
    print(l)
    return
    for _ in range(20):
        l = list(range(1, 11))
        to_rm1 = choice(l)
        l.remove(to_rm1)
        # print(to_rm1, missing_one(l))

        to_rm2 = choice(l)
        l.remove(to_rm2)
        # missing_two(l)
        t1, t2 = sorted((to_rm1, to_rm2)), missing_m(l, 2)

        print(t1 == t2, t1, t2)
        to_rm3 = choice(l)
        l.remove(to_rm3)
        t1, t2 = sorted((to_rm1, to_rm2, to_rm3)), missing_m(l, 3)
        print(t1 == t2, t1, t2)
        t1, t2 = sorted((to_rm1, to_rm2, to_rm3)), missing_m(l, 3)

    print(missing_m([], 4))
    pass


if __name__ == '__main__':
    __main()
