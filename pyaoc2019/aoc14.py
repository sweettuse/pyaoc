from collections import defaultdict
from itertools import chain
from typing import Union, NamedTuple

import pyaoc2019.utils as U

__author__ = 'acushner'


class Compound(NamedTuple):
    qty: int
    name: str

    @classmethod
    def from_str(cls, s):
        q, n = s.split()
        return cls(int(q), n)


def _parse_line(l):
    inputs, output = l.split(' => ')
    return [Compound.from_str(s) for s in chain([output], inputs.split(', '))]


def parse_file(name: Union[int, str] = 14):
    res = defaultdict(dict)
    for l in U.read_file(name):
        out, *ins = _parse_line(l)
        res[out] = ins
    return res


def __main():
    print(Compound.from_str('7 A'))
    print(parse_file('14.test'))
    pass


if __name__ == '__main__':
    __main()
