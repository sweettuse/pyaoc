from operator import itemgetter
from typing import NamedTuple, List, Set, FrozenSet, Iterable

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


class CompMap(dict):
    def __missing__(self, key):
        s = self[key] = set()
        return s

    def add(self, comp: Comp):
        self[comp.left].add(comp)
        self[comp.right].add(comp)

    @classmethod
    def from_comps(cls, comps: Iterable[Comp]):
        res = cls()
        U.exhaust(map(res.add, comps))
        return res


def calc_longest_bridge(fn, start=0, maxkey=itemgetter(1)):
    comp_map = CompMap.from_comps(map(Comp.from_str, U.read_file(fn, 2017)))

    def _calc_longest_bridge_helper(cur, already_used: FrozenSet[Comp], depth=0):
        comps = comp_map[cur] - already_used
        if not comps:
            return depth, sum(c.value for c in already_used)

        return max((_calc_longest_bridge_helper(c.other(cur), already_used | {c}, depth + 1) for c in comps),
                   key=maxkey)

    return _calc_longest_bridge_helper(start, frozenset())


def __main():
    print(calc_longest_bridge('24'))
    print(calc_longest_bridge('24', maxkey=U.identity))


if __name__ == '__main__':
    __main()
