from collections import Counter

from cytoolz.functoolz import juxt
from cytoolz.itertoolz import rest

__author__ = 'acushner'

puzzle_bounds = range(402328, 864248)


def has_double(num: str):
    return any(n1 == n2 for n1, n2 in zip(num, rest(num)))


def is_monotonic(num: str):
    return all(n2 >= n1 for n1, n2 in zip(num, rest(num)))


def has_exact_double(num: str):
    return 2 in Counter(num).values()


def aoc4(*validators):
    validator = juxt(*validators)
    return sum(1 for n in puzzle_bounds if all(validator(str(n))))


def __main():
    print(aoc4(has_double, is_monotonic))
    print(aoc4(has_exact_double, is_monotonic))


if __name__ == '__main__':
    __main()
