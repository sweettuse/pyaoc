import time
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations
from typing import Union, NamedTuple, Dict
from operator import add, sub

import numpy as np

import utils as U

__author__ = 'acushner'

identity = lambda x: x


class Coord(NamedTuple):
    x: int = 0
    y: int = 0
    z: int = 0

    @classmethod
    def from_dict(cls, d):
        return cls(d['x'], d['y'], d['z'])

    def __add__(self, other):
        return self._add_sub(other, add)

    def __sub__(self, other):
        return self._add_sub(other, sub)

    def _add_sub(self, other, oper):
        return type(self)(*map(oper, self, other))

    @property
    def value(self):
        return sum(map(abs, self))


def parse_file(name: Union[str, int] = 12):
    return {Coord.from_dict(eval(v.replace('<', 'dict(').replace('>', ')'))): Coord() for v in U.read_file(name)}


def _get_ind_offset_val(v1, v2):
    """for each pair of dimension vals (e.g., x dim, y dim, z dim), return what the offset should be"""
    if v1 == v2:
        return 0
    return 1 if v1 < v2 else -1


def get_offset(c1: Coord, c2: Coord) -> Coord:
    return Coord(*map(_get_ind_offset_val, c1, c2))


def _update_velocity(data: Dict[Coord, Coord]):
    """side effects"""
    for k1, k2 in combinations(data.keys(), 2):
        o = get_offset(k1, k2)
        data[k1] += o
        data[k2] -= o


def update(data: Dict[Coord, Coord]):
    _update_velocity(data)
    return {k + v: v for k, v in data.items()}


def calc_energy(data):
    return sum(k.value * v.value for k, v in data.items())


def aoc12_a(n=1000, name=12):
    data = parse_file(name)
    for _ in range(n):
        data = update(data)
    return calc_energy(data)


def _get_xyz(data, a):
    return tuple((getattr(k, a), getattr(v, a)) for k, v in data.items())


def aoc12_b():
    data = parse_file("12")
    res = defaultdict(set)
    vals = set('xyz')

    while True:
        to_rm = set()
        for v in vals:
            cur = res[v]
            dimension_vals = _get_xyz(data, v)
            if dimension_vals in cur:
                to_rm.add(v)
            else:
                res[v].add(dimension_vals)

        vals -= to_rm
        if not vals:
            break

        data = update(data)

    return np.lcm.reduce([len(v) for v in res.values()])


def __main():
    print(aoc12_a())
    start = time.perf_counter()
    print(aoc12_b())
    print(time.perf_counter() - start)


if __name__ == '__main__':
    __main()
