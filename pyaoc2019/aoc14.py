from __future__ import annotations

import math
from collections import defaultdict
from itertools import chain, count
from typing import Union, NamedTuple, Dict, Set

from cytoolz import memoize

import pyaoc2019.utils as U

__author__ = 'acushner'


class Ingredient(NamedTuple):
    name: str
    qty: int

    @classmethod
    def from_str(cls, s):
        q, n = s.split()
        return cls(n, int(q))


class Compound(NamedTuple):
    out: Ingredient
    ins: Set[Ingredient]

    @property
    def names(self):
        return [e.name for e in self.ins]

    @property
    def name(self):
        return self.out.name

    @property
    def min_qty(self):
        return self.out.qty

    @classmethod
    def from_str(cls, s):
        inputs, output = s.split(' => ')
        out, *ins = map(Ingredient.from_str, chain([output], inputs.split(', ')))
        return cls(out, set(ins))

    def cost(self, compounds: Compounds, amount_needed=1):
        num_compound_needed = self._calc_amount_needed(compounds, amount_needed)

        for ing in self.ins:
            if comp := compounds.name_compound_map.get(ing.name):
                comp.cost(compounds, num_compound_needed * ing.qty)
            else:
                compounds.amount_needed[self.name] += amount_needed
                compounds.amount_needed[ing.name] += num_compound_needed * ing.qty

    def _calc_amount_needed(self, compounds: Compounds, amount_needed) -> int:
        """side effect, updates bank"""
        leftover = compounds.from_bank(self.name, amount_needed)

        amount_needed -= leftover
        num_compound_needed = math.ceil(amount_needed / self.min_qty)
        compounds.to_bank(self.name, num_compound_needed * self.min_qty - amount_needed)
        return num_compound_needed


CompoundMap = Dict[str, Compound]


class Compounds:
    def __init__(self, filename: str):
        self.name_compound_map: CompoundMap = parse_file(filename)
        self._bank = defaultdict(int)
        self.amount_needed = defaultdict(int)

    def from_bank(self, name: str, amount):
        res = min(self._bank[name], amount)
        self._bank[name] -= res
        return res

    def to_bank(self, name, val):
        self._bank[name] += val

    def cost(self, amount_needed=1):
        cm = self.name_compound_map
        cm['FUEL'].cost(self, amount_needed)
        return self.amount_needed['ORE']


def with_total_ore(filename, total=1e12):
    start_hint = _calc_start_hint(filename, total)
    for t in count(start_hint):
        if Compounds(filename).cost(t) > total:
            print(t - start_hint)
            return t - 1


def _calc_start_hint(filename, total) -> int:
    start_guess = total // Compounds(filename).cost()
    return int(start_guess * (total / (Compounds(filename).cost(start_guess))))


@memoize
def parse_file(name: Union[int, str] = 14) -> CompoundMap:
    return {c.name: c for c in map(Compound.from_str, U.read_file(name))}


def __main():
    c = Compounds('14')
    print(c.cost())
    print(c.amount_needed)
    print(c._bank)
    print(with_total_ore(14))


if __name__ == '__main__':
    __main()
