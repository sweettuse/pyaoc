from more_itertools import first

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'


def parse_data(*, debug=False):
    prob_num = __file__[-5:-3]
    filename = int(prob_num)
    if debug:
        filename = f'{prob_num}.test'

    data = read_file(filename, 2021)
    return data


l_pairs = dict(zip('<([{', '>)]}'))
r_pairs = {v: k for k, v in list(l_pairs.items())}

char_scores_1 = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


def _get_corrupt_or_incomplete(l) -> list[str] | str:
    """return remaining stack if incomplete
    return failed match str if corrupt"""
    stack = []
    for i, c in enumerate(l):
        if c in l_pairs:
            stack.append(c)
        elif c in r_pairs and (not stack or stack[-1] != r_pairs[c]):
            return c
        else:
            stack.pop()

    return stack


def part1(data):
    return sum(char_scores_1[c]
               for c in filter(lambda v: isinstance(v, str),
                               map(_get_corrupt_or_incomplete, data)))


char_scores_2 = dict(zip(')]}>', range(1, 5)))


def _score(stack: list[str]):
    res = 0
    for c in reversed(stack):
        res *= 5
        res += char_scores_2[l_pairs[c]]
    return res


def part2(data):
    scores = sorted(_score(stack)
                    for stack in filter(lambda v: isinstance(v, list),
                                        map(_get_corrupt_or_incomplete, data)))
    return scores[len(scores) // 2]


def __main():
    data = parse_data(debug=False)
    print(part1(data))
    print(part2(data))


if __name__ == '__main__':
    __main()
