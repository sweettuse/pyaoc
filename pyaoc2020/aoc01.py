from itertools import combinations, product

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'

data = list(map(int, read_file(1, 2020)))
assert len(data) == len(data := frozenset(data)), 'will not work if there are duplicates'


def part1(target=2020):
    for n in data:
        if (other := target - n) in data:
            return n * other


def part2():
    for n in data:
        if (other := part1(2020 - n)) is not None:
            return n * other


def slowp1():
    for x in data:
        for y in data:
            if x + y == 2020:
                return x * y


def slowp2():
    for x in data:
        for y in data:
            for z in data:
                if x + y + z == 2020:
                    return x * y * z


@timer
def slow():
    print(slowp1())
    print(slowp2())


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    slow()
    __main()
