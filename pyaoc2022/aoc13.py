from __future__ import annotations
from dataclasses import dataclass
from itertools import zip_longest
from math import prod
from typing import Any

from more_itertools import always_iterable

from pyaoc2019.utils import read_file, mapt

make_list = lambda v: list(always_iterable(v))


def in_order(l1, l2):
    for e1, e2 in zip_longest(l1, l2):
        if isinstance(e1, int) and isinstance(e2, int):
            if e1 != e2:
                return e1 < e2
        elif e1 is None:
            return True
        elif e2 is None:
            return False
        else:
            res = in_order(make_list(e1), make_list(e2))
            if res is not None:
                return res


def parse_data(name):
    return [mapt(eval, pair.splitlines()) for pair in read_file(name, do_split=False).split('\n\n')]


def part1(name):
    return sum(i for i, pair in enumerate(parse_data(name), 1) if in_order(*pair))


# ==============================================================================
# part 2
# ==============================================================================


@dataclass
class Packet:
    t: Any

    def __lt__(self, other):
        return in_order(self.t, other.t)

    def __eq__(self, other):
        return self.t == other.t


def part2(name):
    pairs = parse_data(name)
    divider_pair = [[2]], [[6]]
    pairs.append(divider_pair)

    packets = sorted(Packet(p) for pair in pairs for p in pair)
    divider_packets = mapt(Packet, divider_pair)

    return prod(i for i, p in enumerate(packets, 1) if p in divider_packets)


print(part1(13))
print(part2(13))
