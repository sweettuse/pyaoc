import math
from itertools import chain
from textwrap import dedent

import pyaoc2019.utils as U
from typing import List

__author__ = 'acushner'


def rotate(v):
    res = zip(*reversed(v))
    return [''.join(v) for v in res]


class Patterns(dict):
    @staticmethod
    def _create_rotations(v):
        rows = v.split('/')
        return chain.from_iterable(((rows := rotate(rows)), rows[::-1]) for _ in range(4))

    def __setitem__(self, key, value):
        keys = self._create_rotations(key)
        self.update(('/'.join(k), value) for k in keys)

    @classmethod
    def from_strs(cls, strs: List[str]):
        res = cls()
        for s in strs:
            k, v = s.split(' => ')
            res[k] = v
        return res


class Art:
    def __init__(self, grid, patterns):
        self.grid = grid.copy()
        self.ps = patterns

    @property
    def _chunks(self):
        cs = 2 + len(self.grid) % 2
        r = range(0, len(self.grid), cs)
        for n_rows in r:
            for n_cols in r:
                yield [v[n_cols: n_cols + cs] for v in self.grid[n_rows: n_rows + cs]]

    @staticmethod
    def _reassemble(chunks):
        size = math.isqrt(len(chunks))
        return [''.join(words)
                for c in U.chunks(chunks, size)
                for words in zip(*(s.split('/') for s in c))]

    def update(self):
        updated = [self.ps['/'.join(c)] for c in self._chunks]
        self._reassemble(updated)
        self.grid = self._reassemble(updated)

    def __str__(self):
        return '\n'.join(self.grid) + '\n'

    __repr__ = __str__


def aoc21(n_iter=5):
    start = '.#. ..# ###'.split()
    art = Art(start, Patterns.from_strs(U.read_file(21, 2017)))
    for _ in range(n_iter):
        art.update()
    return str(art).count('#')


def __main():
    with U.localtimer():
        print(aoc21())
    with U.localtimer():
        print(aoc21(18))


if __name__ == '__main__':
    __main()
