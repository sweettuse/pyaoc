from functools import lru_cache
from itertools import count
from operator import itemgetter
from typing import NamedTuple, FrozenSet, Iterable, Callable

import pyaoc2019.utils as U

__author__ = 'acushner'

_id_counter = count()


class Comp(NamedTuple):
    left: int
    right: int
    id_: int  # this field is here to allow "duped" components in a set

    @classmethod
    def from_str(cls, s):
        return cls(*map(int, s.split('/')), next(_id_counter))

    @property
    def value(self):
        return self.left + self.right

    def other(self, value):
        return self[self[0] == value]


class CompMap(dict):
    def __missing__(self, key):
        res = self[key] = set()
        return res

    def add(self, comp: Comp):
        self[comp.left].add(comp)
        self[comp.right].add(comp)

    @classmethod
    def from_comps(cls, comps: Iterable[Comp]):
        res = cls()
        U.exhaust(map(res.add, comps))
        return res


class BridgeInfo(NamedTuple):
    length: int
    strength: int


def calc_longest_bridge(comp_map: CompMap, maxkey: Callable) -> BridgeInfo:
    @lru_cache(None)
    def _helper(cur: int = 0, already_used: FrozenSet[Comp] = frozenset(), length=0):
        available_comps = comp_map[cur] - already_used

        if not available_comps:
            return length, sum(c.value for c in already_used)

        return max((_helper(c.other(cur), already_used | {c}, length + 1) for c in available_comps), key=maxkey)

    return BridgeInfo(*_helper())


def __main():
    strs = U.read_file(24, 2017)
    comps = [Comp.from_str(s) for s in strs]
    comp_map = CompMap.from_comps(comps)

    with U.localtimer():
        print(calc_longest_bridge(comp_map, maxkey=itemgetter(1)))
        print(calc_longest_bridge(comp_map, maxkey=U.identity))


if __name__ == '__main__':
    __main()
