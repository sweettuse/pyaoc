from collections import Counter

from cytoolz.functoolz import juxt
from cytoolz.itertoolz import rest

import pyaoc2019.utils as U

__author__ = 'acushner'

puzzle_bounds = range(402328, 864248)


def has_double(num: str):
    return any(n1 == n2 for n1, n2 in zip(num, rest(num)))


def is_monotonic(num: str):
    return all(n2 >= n1 for n1, n2 in zip(num, rest(num)))


def has_exact_double(num: str):
    return is_monotonic(num) and 2 in Counter(num).values()


def aoc4(*validators):
    validator = juxt(*validators)
    return sum(all(validator(n)) for n in map(str, puzzle_bounds))


def aoc4_faster_on_more_than_one_validator(*validators):
    return sum(all(v(n) for v in validators) for n in map(str, puzzle_bounds))


def __main():
    with U.localtimer():
        print(aoc4(has_double, is_monotonic))
    with U.localtimer():
        print(aoc4_faster_on_more_than_one_validator(has_double, is_monotonic))
    with U.localtimer():
        print(aoc4(has_exact_double))
    with U.localtimer():
        print(aoc4_faster_on_more_than_one_validator(has_exact_double))


if __name__ == '__main__':
    __main()
