from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import product
from math import ceil
from operator import attrgetter

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = "acushner"

weapon_str = """
    Dagger        8     4       0
    Shortsword   10     5       0
    Warhammer    25     6       0
    Longsword    40     7       0
    Greataxe     74     8       0
    """

armor_str = """
    null_armor    0     0       0
    Leather      13     0       1
    Chainmail    31     0       2
    Splintmail   53     0       3
    Bandedmail   75     0       4
    Platemail   102     0       5
    """

ring_str = """
    null_ring1   0     0       0
    null_ring2   0     0       0
    Damage+1    25     1       0
    Damage+2    50     2       0
    Damage+3   100     3       0
    Defense+1   20     0       1
    Defense+2   40     0       2
    Defense+3   80     0       3
    """


class Item(NamedTuple):
    name: str
    cost: int
    dmg: int
    armor: int

    @classmethod
    def from_str(cls, s):
        name, *rest = s.split()
        return cls(name, *map(int, rest))


@dataclass
class C:
    name: str
    hp: int
    dmg: int
    armor: int
    cost: int = 0
    items: list[Item] = field(default_factory=list)

    def equip(self, *items: Item):
        for item in items:
            self.dmg += item.dmg
            self.armor += item.armor
            self.cost += item.cost
        self.items.extend(items)

    def to_beat(self, other: C):
        """num rounds for self to beat other"""
        if (inflicted := self.dmg - other.armor) <= 0:
            return float("inf")
        return ceil(other.hp / inflicted)

    def beats(self, other: C):
        num_self = self.to_beat(other)
        num_other = other.to_beat(self)
        # print(self, num_self, num_other)
        if self.name == "player":
            return num_self <= num_other
        return num_self < num_other


boss = C("boss", 109, 8, 2)
player = C("player", 100, 0, 0)


def _parse(item_str):
    return [Item.from_str(s) for s in filter(bool, map(str.strip, item_str.splitlines()))]


weapons = _parse(weapon_str)
armor = _parse(armor_str)
rings = _parse(ring_str)


def _rings():
    for i, r1 in enumerate(rings[:-1]):
        for r2 in rings[i + 1 :]:
            yield r1, r2


def part1():
    def _winning_costs():
        for w, a, rings in product(weapons, armor, _rings()):
            p = deepcopy(player)
            p.equip(w, a, *rings)
            if p.beats(boss):
                yield p

    return min(_winning_costs(), key=attrgetter('cost'))


def part2():
    def _losing_costs():
        for w, a, rings in product(weapons, armor, _rings()):
            p = deepcopy(player)
            p.equip(w, a, *rings)
            if boss.beats(p):
                yield p

    return max(_losing_costs(), key=attrgetter('cost'))


from rich import print


def __main():
    print(part1())
    print(part2())
    # print(weapons)


if __name__ == "__main__":
    __main()
