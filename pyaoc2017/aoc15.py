from cytoolz.itertoolz import take

import pyaoc2019.utils as U

__author__ = 'acushner'

A_START = 591
A_FACTOR = 16807
B_START = 393
B_FACTOR = 48271
A_MULT = 4
B_MULT = 8
DIVISOR = 2147483647
COMP_BITS = 0xffff


def value_gen(start: int, factor: int, multiple_of=1):
    res = start
    while True:
        res *= factor
        res %= DIVISOR
        if res % multiple_of == 0:
            yield res & COMP_BITS


def aoc15(a_start=A_START, b_start=B_START, a_mult=A_MULT, b_mult=B_MULT, n=40_000_000):
    a_gen = value_gen(a_start, A_FACTOR, a_mult)
    b_gen = value_gen(b_start, B_FACTOR, b_mult)
    return sum(a == b for (a, b) in take(n, zip(a_gen, b_gen)))


def test():
    print(aoc15(65, 8921, 5, 1, 1))


def __main():
    with U.localtimer():
        print(aoc15(a_mult=1, b_mult=1))
    with U.localtimer():
        print(aoc15(n=5_000_000))


if __name__ == '__main__':
    __main()
