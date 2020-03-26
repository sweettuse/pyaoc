from collections import Counter

import pyaoc2019.utils as U

__author__ = 'acushner'


def aoc02_a(data):
    num_twos = num_threes = 0
    for c in map(Counter, data):
        num_twos += (2 in c.values())
        num_threes += (3 in c.values())
    return num_twos * num_threes


def aoc02_b(data):
    for i, w1 in enumerate(data, 1):
        for w2 in data[i:]:
            diffs = 0
            for c1, c2 in zip(w1, w2):
                diffs += c1 != c2
                if diffs > 1:
                    break
            if diffs == 1:
                return ''.join(c1 for c1, c2 in zip(w1, w2) if c1 == c2)


def __main():
    data = U.read_file(2, 2018)
    print(aoc02_a(data))
    print(aoc02_b(data))
    pass


if __name__ == '__main__':
    __main()
