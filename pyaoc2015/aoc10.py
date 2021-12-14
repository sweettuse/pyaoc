from itertools import groupby

from pyaoc2019.utils import read_file, mapt, timer
from typing import NamedTuple

__author__ = 'acushner'

data = '1113222113'


def _get_next(s):
    res = []
    for n, g in groupby(s):
        res.append(str(sum(1 for _ in g)))
        res.append(n)
    return ''.join(res)


@timer
def parts1and2(num):
    s = data
    for _ in range(num):
        s = _get_next(s)
    return len(s)


def __main():
    print(parts1and2(40))
    print(parts1and2(50))


if __name__ == '__main__':
    __main()
