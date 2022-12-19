from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from functools import cache

from pyaoc2019.utils import read_file, mapt, timer
from rich import print


@dataclass(unsafe_hash=True)
class Valve:
    name: str
    flow_rate: int
    connected: frozenset[str]

    @classmethod
    def from_str(cls, s: str) -> Valve:
        first, second = s.split(';')
        _, name, *_ = first.split()
        rate = int(first.split('=')[-1])

        tunnels = second.replace(',', '').split('to ')[-1]
        return cls(name, rate, frozenset(tunnels.split(' ')[1:]))

    @property
    @cache
    def links(self) -> frozenset[tuple[str, str]]:
        return frozenset((self.name, l) for l in self.connected)

def parse_data(name):
    return mapt(Valve.from_str, read_file(name))


total_opened = set()
@timer
def part1(name):
    valves = parse_data(name)
    valve_map: dict[str, Valve] = {v.name: v for v in valves}

    print(valve_map)

    def _helper(
        location: str,
        remaining: int = 30,
        accounted_venting: int = 0,
        traversed: frozenset[tuple[str, str]] = frozenset(),
        opened: frozenset[str] = frozenset(),
    ) -> int:
        if remaining <= 1:
            return accounted_venting

        cur = valve_map[location]
        to_traverse = cur.links - traversed

        if not to_traverse:
            return accounted_venting

        res = []
        if cur.name not in opened and cur.flow_rate > 0:
            # we should open this
            with_this_opened = opened | {location}
            total_opened.update(with_this_opened)
            for _, l in to_traverse:
                res.append(
                    _helper(
                        l,
                        remaining - 2,
                        accounted_venting + cur.flow_rate * (remaining - 1),
                        traversed | {(cur.name, l)},
                        with_this_opened,
                    ),
                )
        for _, l in to_traverse:
            res.append(
                _helper(
                    l,
                    remaining - 1,
                    accounted_venting,
                    traversed | {(cur.name, l)},
                    opened,
                ),
            )
        return max(res)

    res = _helper('AA')
    return res


print(part1('16.test'))

    # def _helper(
    #     location: str,
    #     remaining: int = 30,
    #     flow_rate: int = 0,
    #     total_vented: int = 0,
    #     traversed: frozenset[tuple[str, str]] = frozenset(),
    #     opened: frozenset[str] = frozenset(),
    # ) -> int:
    #     if remaining <= 1:
    #         return remaining * flow_rate + total_vented

    #     cur = valve_map[location]
    #     to_traverse = cur.links - traversed

    #     if not to_traverse:
    #         return remaining * flow_rate + total_vented

    #     res = []
    #     if cur.name not in opened and cur.flow_rate > 0:
    #         # we should open this
    #         with_this_opened = opened | {location}
    #         total_opened.update(with_this_opened)
    #         for _, l in to_traverse:
    #             res.append(
    #                 _helper(
    #                     l,
    #                     remaining - 2,
    #                     flow_rate + cur.flow_rate,
    #                     total_vented + 2 * flow_rate + cur.flow_rate,
    #                     traversed | {(cur.name, l)},
    #                     with_this_opened,
    #                 ),
    #             )
    #     for _, l in to_traverse:
    #         res.append(
    #             _helper(
    #                 l,
    #                 remaining - 1,
    #                 flow_rate,
    #                 total_vented + flow_rate,
    #                 traversed | {(cur.name, l)},
    #                 opened,
    #             ),
    #         )
    #     return max(res)