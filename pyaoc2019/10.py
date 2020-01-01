__author__ = 'acushner'

import math
from collections import defaultdict
from functools import reduce
from itertools import permutations
from operator import itemgetter
from typing import NamedTuple

from cytoolz import first, memoize

import pyaoc2019.utils as U

test_input = '''.#..#
.....
#####
....#
...##'''

test_input2 = '''.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##'''

test_input3 = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'''


class Coord(NamedTuple):
    c: int
    r: int

    def __sub__(self, other):
        return Coord(self.c - other.c, self.r - other.r)

    def __add__(self, other):
        return Coord(self.c + other.c, self.r + other.r)

    def is_inbounds(self, size):
        return 0 <= self.c < size and 0 <= self.r < size

    @property
    def gcd(self):
        gcd = math.gcd(self.c, self.r)
        return Coord(self.c // gcd, self.r // gcd)


def parse_data(data):
    data = data.splitlines() if isinstance(data, str) else data
    return frozenset(Coord(c_idx, r_idx)
                     for (r_idx, r) in enumerate(data)
                     for (c_idx, v) in enumerate(r)
                     if v == '#')


def parse_file(name=10):
    return parse_data(U.read_file(name))


def _blocked_coords(cur, other, size):
    offset = (other - cur).gcd
    yield cur
    cur = other
    while True:
        cur += offset
        if not cur.is_inbounds(size):
            break
        yield cur


def _get_visible_asteroids(data):
    res = defaultdict(set)
    size = len(data)
    for (c1, c2) in permutations(data, 2):
        res[c1].update(_blocked_coords(c1, c2, size))
    return {k: data - v for k, v in res.items()}


@memoize
def aoc10_a(data):
    visible = _get_visible_asteroids(data)
    by_len = ((k, len(v)) for k, v in visible.items())
    return visible, max(by_len, key=itemgetter(1))


def aoc10_b(data):
    visible, (best, num) = aoc10_a(data)
    asteroids = visible[best]

    def _sort_key(c):
        c = best - c
        at = math.atan2(-c.c, c.r)
        return at + (at < 0.0) * math.tau

    return sorted(asteroids, key=_sort_key)


def __main():
    data = parse_file()
    visible, (best, num) = aoc10_a(data)
    print(best, num)
    print(aoc10_b(data)[199])


if __name__ == '__main__':
    __main()
