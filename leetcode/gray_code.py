__author__ = 'acushner'

# https://leetcode.com/problems/gray-code/
from functools import lru_cache
from itertools import chain, permutations, accumulate
from operator import mul
from typing import List


def _to_bit_str(v, n):
    return bin(v)[2:].zfill(n)


print(list(accumulate(range(1, 8), mul)))


def gray_code(n: int) -> List[int]:
    print(sorted('00 01 10 11'.split()))
    print(sorted('000 001 010 011 100 101 110 111'.split()))
    two_n_1 = 2 ** (n - 1)

    res = chain(range(two_n_1), reversed(range(two_n_1, 2 * two_n_1)))
    print([_to_bit_str(v, n) for v in res])


def factorials(n):
    res = list(accumulate(range(1, n + 1), mul))
    res.reverse()
    return res


def perms(n):
    for i, v in enumerate(permutations(range(0, n)), 1):
        print(i, v)



def __main():
    print(factorials(2))
    return perms(2)
    return gray_code(4)


if __name__ == '__main__':
    __main()
