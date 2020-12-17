from collections import Counter
from itertools import product
from typing import NamedTuple

from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


class Coord(NamedTuple):
    x: int
    y: int
    z: int = 0
    w: int = 0

    def __add__(self, other):
        return Coord(*(v1 + v2 for v1, v2 in zip(self, other)))


def parse_data(fname=17):
    return {Coord(y, x)
            for y, row in enumerate(reversed(read_file(fname, 2020)))
            for x, v in enumerate(row)
            if v == '#'}


def _get_surrounding(num_dims):
    return {Coord(*v) for v in product(range(-1, 2), repeat=num_dims)} - {Coord(0, 0)}


def _update(actives, surrounding):
    num_living_neighbors = Counter(c + offset for c in actives for offset in surrounding)
    # get those that are born
    active_next = {c for c, num_neighbs in num_living_neighbors.items() if num_neighbs == 3} - actives
    # add those that survive
    active_next |= {c for c in actives if num_living_neighbors[c] in {2, 3}}
    return active_next


def part1and2(num_dims):
    actives = parse_data()
    surrounding = _get_surrounding(num_dims)
    for _ in range(6):
        actives = _update(actives, surrounding)
    return len(actives)


@timer
def __main():
    print(part1and2(num_dims=3))
    print(part1and2(num_dims=4))


# 382
# 2552
# '__main' took 0.49714007200000004 seconds


if __name__ == '__main__':
    __main()
