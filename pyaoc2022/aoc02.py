from itertools import starmap
from typing import Literal

from pyaoc2019.utils import read_file


scores = dict(
    A=1,
    B=2,
    C=3,
    W=6,
    L=0,
    D=3,
)

vals = 'ABC'
convert = dict(zip('XYZABC', 'ABCABC'))
outcomes = dict(zip('XYZ', 'LDW'))


def outcome(opp, you) -> Literal['W', 'L', 'D']:
    opp, you = convert[opp], convert[you]

    if opp == you:
        return 'D'
    if vals[vals.index(you) - 1] == opp:
        return 'W'
    return 'L'


def score1(opp, you) -> int:
    you = convert[you]
    return scores[you] + scores[outcome(opp, you)]


def parse_file(name):
    return [v.split() for v in read_file(name)]


def part1():
    return sum(starmap(score1, parse_file(2)))


def which_object(opp, condition):
    offset = dict(zip('LDW', range(-1, 2)))[condition]
    opp_idx = vals.index(opp)
    return vals[(opp_idx + offset) % 3]


def score2(opp, you):
    wld = outcomes[you]
    you = which_object(opp, wld)

    return scores[you] + scores[wld]


def part2():
    return sum(starmap(score2, parse_file(2)))


print(part1())
print(part2())
