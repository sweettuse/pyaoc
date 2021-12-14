from collections import Counter
from itertools import pairwise

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'



def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    return read_file(filename, 2015)


def _gt3_vowels(s):
    c = Counter(s)
    return sum(c[v] for v in 'aeiou') >= 3


bad = set('ab cd pq xy'.split())


def _double_letter(s):
    return any(c1 == c2 for c1, c2 in pairwise(s))


def _excludes(s):
    return not any(b in s for b in bad)


def part1(data):
    def good(s):
        return _gt3_vowels(s) and _double_letter(s) and _excludes(s)

    return sum(1 for _ in filter(good, data))


def _two_pairs(s):
    for t in pairwise(s):
        if s.count(''.join(t)) == 2:
            return True

def _three(s):
    for a, _, c in zip(s, s[1:], s[2:]):
        if a == c:
            return True

def part2(data):
    good = lambda s: _three(s) and _two_pairs(s)
    return sum(1 for _ in filter(good, data))


def __main():
    data = parse_data(debug=False)
    # print(part1(['haegwjzuvuyypxyu']))
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
