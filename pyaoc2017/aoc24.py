from collections import defaultdict
from operator import itemgetter
from typing import NamedTuple, FrozenSet, Iterable, Callable

import pyaoc2019.utils as U

__author__ = 'acushner'


class Comp(NamedTuple):
    left: int
    right: int

    @classmethod
    def from_str(cls, s):
        return cls(*map(int, s.split('/')))

    @property
    def value(self):
        return self.left + self.right

    def other(self, value):
        return self[self[0] == value]


class CompMap(defaultdict):
    def add(self, comp: Comp):
        self[comp.left].add(comp)
        self[comp.right].add(comp)

    @classmethod
    def from_comps(cls, comps: Iterable[Comp]):
        res = cls(set)
        U.exhaust(map(res.add, comps))
        return res


def calc_longest_bridge(fname, maxkey: Callable, start: int = 0):
    comps = map(Comp.from_str, U.read_file(fname, 2017))
    comp_map = CompMap.from_comps(comps)

    def _helper(cur: int, already_used: FrozenSet[Comp], length=0):
        matches = comp_map[cur] - already_used

        if not matches:
            return length, sum(c.value for c in already_used)

        return max((_helper(c.other(cur), already_used | {c}, length + 1) for c in matches), key=maxkey)

    return _helper(start, frozenset())


def __main():
    print(calc_longest_bridge('24', maxkey=itemgetter(1)))
    print(calc_longest_bridge('24', maxkey=U.identity))


if __name__ == '__main__':
    __main()
