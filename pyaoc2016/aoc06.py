from collections import Counter

__author__ = 'acushner'

from pyaoc2019.utils import read_file


def aoc06(columns, idx=0):
    return ''.join(Counter(c).most_common()[idx][0] for c in columns)


def __main():
    columns = list(zip(*read_file(6, 2016)))
    print(aoc06(columns))
    print(aoc06(columns, -1))
    pass


if __name__ == '__main__':
    __main()
