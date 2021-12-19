from functools import cache
from itertools import count
from math import floor

from pyaoc2019.utils import read_file, mapt, timer
from typing import NamedTuple

__author__ = 'acushner'


def _sum_factors1(n):
    if n == 1:
        return 1
    if n == 2:
        return 3

    total = 0
    s = floor(n ** .5)
    for cur in range(1, s + 1):
        mul, rem = divmod(n, cur)
        if not rem:
            total += cur + mul
    return total * 10


@timer
def parts1and2(num_presents, sum_factors):
    for n in count(10000):
        sf = sum_factors(n)
        if not n % 100000:
            print('.', end='', flush=True)
        if not n % 1000000:
            print()
        if sf > num_presents:
            print()
            return n


def _is_valid(div, n):
    return div * 50 >= n


def _sum_factors2(n):
    if n == 1:
        return 1
    if n == 2:
        return 3

    total = 0
    s = floor(n ** .5)
    for cur in range(1, s + 1):
        mul, rem = divmod(n, cur)
        if not rem:
            total += _is_valid(cur, n) * cur + _is_valid(mul, n) * mul
    return total * 11


def __main():
    num_presents = 29000000
    # print(parts1and2(num_presents, _sum_factors1))
    print(parts1and2(num_presents, _sum_factors2))


if __name__ == '__main__':
    __main()
