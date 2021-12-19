from copy import copy
from dataclasses import dataclass
from itertools import count

from pyaoc2019.utils import read_file, mapt
from typing import NamedTuple

__author__ = 'acushner'

weapon_str = \
    """
    Dagger        8     4       0
    Shortsword   10     5       0
    Warhammer    25     6       0
    Longsword    40     7       0
    Greataxe     74     8       0
    """

armor_str = \
    """
    Leather      13     0       1
    Chainmail    31     0       2
    Splintmail   53     0       3
    Bandedmail   75     0       4
    Platemail   102     0       5
    """

ring_str = \
    """
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

    def equip(self, item: Item):
        self.dmg += item.dmg
        self.armor += item.armor


boss = C('boss', 109, 8, 2)
player = C('player', 100, 0, 0)


def _parse(item_str):
    return [Item.from_str(s) for s in filter(bool, map(str.strip, item_str.splitlines()))]


weapons = _parse(weapon_str)
armor = _parse(armor_str)
rings = _parse(ring_str)


def _round(*items) -> bool:
    b, p = map(copy, (boss, player))
    for it in items:
        p.equip(it)

    a, d = p, b
    while True:
        if d.hp <= 0:
            return d.name == 'boss'
        a, d = d, a


        break


def part1():
    # print(b, p)

    pass


def part2():
    pass


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
