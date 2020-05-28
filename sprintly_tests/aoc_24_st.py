from functools import lru_cache
from typing import NamedTuple, FrozenSet, Callable

__author__ = 'acushner'

from pyaoc2019.utils import read_file, localtimer


class Comp(NamedTuple):
    left: int
    right: int

    @classmethod
    def from_str(cls, s):
        return cls(*map(int, s.split('/')))

    @property
    def strength(self):
        return self.left + self.right

    def other(self, no_pins):
        return self.left if no_pins == self.right else self.right

    def __hash__(self):
        return id(self)


class CompMap(dict):
    """map number of ports to components that contain at least one matching port"""

    def __missing__(self, key):
        res = self[key] = set()
        return res

    def add(self, comp: Comp):
        self[comp.left].add(comp)
        self[comp.right].add(comp)


class BridgeInfo(NamedTuple):
    length: int
    strength: int


def calc_strongest_bridge(comp_map: CompMap, max_key: Callable = lambda t: t[1]) -> BridgeInfo:
    """
    take a component with at least one 0-pin port
    check all its connections
    recurse
    """

    @lru_cache(None)
    def _helper(cur_no_pins: int = 0, used_components: FrozenSet[Comp] = frozenset(), length: int = 0):
        available_connections = comp_map[cur_no_pins] - used_components

        if not available_connections:
            return length, sum(c.strength for c in used_components)

        return max((_helper(c.other(cur_no_pins), used_components | {c}, length + 1) for c in available_connections),
                   key=max_key)

    res = _helper()
    print(_helper.cache_info())
    return BridgeInfo(*res)


def __main():
    comps = [Comp.from_str(s) for s in read_file(24, 2017)]
    comps = [Comp(0, 2), Comp(2, 2), Comp(2, 2)]
    cm = CompMap()
    for c in comps:
        cm.add(c)
    with localtimer():
        print(calc_strongest_bridge(cm))
        print(calc_strongest_bridge(cm, lambda x: x))


if __name__ == '__main__':
    __main()
