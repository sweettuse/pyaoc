from collections import Counter
from itertools import product, count
from typing import NamedTuple

from pyaoc2019.colors.tile_utils import RC
from pyaoc2019.utils import read_file, timer

__author__ = 'acushner'


def _get_landscape():
    return {RC(r, c): val
            for r, row in enumerate(read_file(18, 2018))
            for c, val in enumerate(row)}


surrounding = {RC(r, c) for r, c in product(range(-1, 2), range(-1, 2))} - {RC(0, 0)}


class Around(NamedTuple):
    num_ground: int
    num_trees: int
    num_lumber: int
    val: str
    rc: RC

    @classmethod
    def from_landscape_loc(cls, landscape, rc):
        res = Counter(landscape.get(rc + s) for s in surrounding)
        return Around(*(res.get(v, 0) for v in '.|#'), landscape[rc], rc)

    def update(self):
        if self.val == '.':
            return '|' if self.num_trees >= 3 else '.'

        if self.val == '|':
            return '#' if self.num_lumber >= 3 else '|'

        if self.val == '#':
            return '#' if self.num_lumber >= 1 and self.num_trees >= 1 else '.'


print(Around.from_landscape_loc(_get_landscape(), RC(0, 0)))


def _update_landscape(landscape, num_times=10):
    f = lambda rc: Around.from_landscape_loc(landscape, rc)
    for _ in range(num_times):
        landscape = {rc: f(rc).update() for rc in landscape}
    return landscape


def part1():
    landscape = _get_landscape()
    c = Counter(_update_landscape(landscape).values())
    return c['|'] * c['#']


def part2():
    num_iter = 1000000000
    landscape = _get_landscape()
    cache = {}

    for i in count():
        if (s_land := frozenset(landscape.items())) in cache:
            break
        cache[s_land] = i
        print(i)
        landscape = _update_landscape(landscape, 1)

    start = cache[s_land]
    cycle = len(cache) - start
    offset = (num_iter - len(cache)) % cycle

    landscape = dict(list(cache)[offset + start])
    c = Counter(landscape.values())
    return c['|'] * c['#']


@timer
def __main():
    print(part1())
    print(part2())
    pass


if __name__ == '__main__':
    __main()
