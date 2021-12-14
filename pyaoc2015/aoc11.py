from functools import lru_cache
from itertools import pairwise

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple
import string

__author__ = 'acushner'

data = 'cqjxjnds'
letters = ''.join(c for c in string.ascii_lowercase if c not in set('iol'))
letter_idx = dict(zip(letters, range(len(letters))))


@lru_cache
def _get3s():
    return {a + b + c for a, b, c in zip(letters, letters[1:], letters[2:])}


def baseN(num, b=23):
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + letters[num % b])


@lru_cache
def _get2s():
    return {(c, c) for c in letters}


def _contains_monotonic(p):
    return any(three in p for three in _get3s())


def _two_diff_pairs(p):
    return len(set(pairwise(p)) & _get2s()) >= 2


def _inc_letter(s) -> tuple[int, str]:
    n = letter_idx[s] + 1
    carry, idx = divmod(n, 23)
    return carry, letters[idx]


def _inc_p(p: str):
    res = []
    for c in (r := reversed(p)):
        carry, l = _inc_letter(c)
        res.append(l)
        if not carry:
            break
    res.extend(r)
    return ''.join(reversed(res))


def iterate(fn, val):
    while True:
        yield (val := fn(val))


def _is_valid(p):
    return _contains_monotonic(p) and _two_diff_pairs(p)


def _find_next_valid(p):
    return next(filter(_is_valid, iterate(_inc_p, p)))


def part1(data):
    return _find_next_valid(data)


def _test():
    assert _contains_monotonic('abc')
    assert not _contains_monotonic('abbceffg')
    assert _two_diff_pairs('abbceaag')
    assert _inc_letter('h') == (0, 'j')
    assert _inc_letter('z') == (1, 'a')
    assert _find_next_valid('abcaaba') == 'abcaabb'


def __main():
    _test()
    next_p = part1(data)
    print(next_p)
    print(part1(next_p))


if __name__ == '__main__':
    __main()
