from itertools import product, permutations

from cytoolz.itertoolz import first

import pyaoc2019.utils as U
import pandas as pd
from io import StringIO

__author__ = 'acushner'


def read_data(fn=2):
    return pd.read_table(StringIO('\n'.join(U.read_file(fn, 2017))), header=None)


def to_sets(df):
    return [set(r) for _, r in df.iterrows()]


def aoc02_a(df):
    return (df.max(1) - df.min(1)).sum()


def _calc_equal_div(s):
    for n1, n2 in permutations(s, 2):
        div = n1 / n2
        if div.is_integer():
            return div


def aoc02_b(df):
    return sum(map(_calc_equal_div, to_sets(df)))


def __main():
    df = read_data()
    print(aoc02_a(df))
    print(aoc02_b(df))


if __name__ == '__main__':
    __main()
