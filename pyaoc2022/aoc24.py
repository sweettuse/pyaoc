from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from functools import cache
from itertools import count, product, starmap

from pyaoc2019.utils import RC, exhaust, read_file, timer
from rich import print


N = RC(-1, 0)
E = RC(0, 1)
S = RC(1, 0)
W = RC(0, -1)

dir_map = dict(zip('^>v<', (N, E, S, W)))

def parse_data(name):
    data = read_file(name)
    first, last = data[0], data[-1]
    res = {
        RC(r, c): dir_map[val]
        for r, row in enumerate(data[1:-1])
        for c, val in enumerate(row[1:-1])
        if val in dir_map
    }
    size = RC(len(data) - 2, len(data[0]) - 2)
    start = RC(-1, first.index('.') - 1)
    end = RC(size.r, last.index('.') - 1)
    return start, end, Blizzards(res, size)


@dataclass
class Blizzards:
    init_pos_map: dict[RC, RC]
    size: RC

    def __post_init__(self):
        self._frozen = frozenset(self.init_pos_map.items())
        self._period = self.size.r * self.size.c
    
    def locations(self, n: int):
        return self._locations(n % self._period)

    def __hash__(self):
        return id(self)
    
    def __eq__(self, other):
        return self is other
    
    @cache
    def _locations(self, n: int):
        return frozenset({(init_pos + d * n) % self.size for init_pos, d in self._frozen})



start, end, blizzards = parse_data('24.test1')
print(blizzards.locations(24))
assert set(blizzards.init_pos_map) == blizzards.locations(24)
assert blizzards.locations(24) is blizzards.locations(0)