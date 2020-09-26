from more_itertools import first

from pyaoc2019.utils import read_file, localtimer
from string import ascii_letters, ascii_lowercase

__author__ = 'acushner'

poly = first(read_file(5, 2018))
anti_map = dict(zip(ascii_letters, ascii_letters.swapcase()))


def part1(ignored=None):
    res = []
    ignored = ignored or set()
    for c in poly:
        if c in ignored:
            continue

        if not res or anti_map[c] != res[-1]:
            res.append(c)
        else:
            res.pop()

    return len(res)


def part2():
    return min(part1({c, c.upper()}) for c in ascii_lowercase)


def __main():
    with localtimer():
        print(part1())
        print(part2())


if __name__ == '__main__':
    __main()
