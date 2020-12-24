from collections import defaultdict
from itertools import starmap, combinations, permutations, product
from math import prod
from typing import List, NamedTuple, Dict

from cytoolz import memoize
from more_itertools import first

from pyaoc2019.utils import read_file, timer, exhaust, Coord

__author__ = 'acushner'


def _to_int(s, reverse=False):
    repl = {'.': '0', '#': '1'}
    if reverse:
        s = reversed(s)
    return int((''.join(repl[c] for c in s)), 2)


class Border(NamedTuple):
    n: int
    e: int
    s: int
    w: int

    @classmethod
    def from_strs(cls, borders: List[str]):
        n, s = borders[0], borders[-1]
        borders = _transpose(borders)
        w, e = borders[0], borders[-1]
        return cls(_to_int(n), _to_int(e), _to_int(s, True), _to_int(w, True))


class Tile(NamedTuple):
    id: int
    orig: Border
    flipped: Border

    @classmethod
    def from_data(cls, id: int, borders: List[str]):
        orig = Border.from_strs(borders)
        flipped = Border.from_strs(_flip_ew(borders))
        return cls(id, orig, flipped)

    @memoize
    def all_borders(self):
        s, *rest = map(set, self[1:])
        return s.union(*rest)


def _parse_data(fname='20.test'):
    res = defaultdict(list)
    cur_img = None
    for line in read_file(fname, 2020):
        if line.startswith('Tile'):
            cur_img = res[int(line.split()[-1][:-1])]
        elif line:
            cur_img.append(line)

    return list(starmap(Tile.from_data, res.items()))


# ======================================================================================================================
# array funcs
def _flip_ew(b: List[str]):
    return [''.join(reversed(r)) for r in b]


def _flip_ns(b: List[str]):
    b = list(zip(*b))
    b = _flip_ew(b)
    return list(map(''.join, zip(*b)))


def _rotate(b: List[str]):
    return list(map(''.join, zip(*reversed(b))))


def _transpose(b: List[str]):
    return list(map(''.join, zip(*b)))


# t = ['123', '456', '789']
# print(t)
# print('ew', _flip_ew(t))
# print('ns', _flip_ns(t))
# print('trans', _transpose(t))
# print('rot', _rotate(_rotate(t)))
# print('flip_both', _flip_ns(_flip_ew(t)))

# ======================================================================================================================


def _num_borders(edge: int):
    return 2 * edge * (edge + 1)


def _shared_borders(edge: int):
    return _num_borders(edge) - 4 * edge


def _get_connections(fname='20.test'):
    data = _parse_data(fname)
    res = defaultdict(set)
    for t1, t2 in permutations(data, 2):
        for o1, o2 in product(('orig', 'flipped'), repeat=2):
            if set(getattr(t1, o1)) & set(getattr(t2, o2)):
                res[t1, o1].add((t2, o2))
                res[t2, o2].add((t1, o1))
    return res


def part1():
    conns = _get_connections(20)
    corners = set()
    for (t1, o1), v in conns.items():
        if len(v) == 2:
            corners.add(t1.id)
            # print(t1.id, o1, [(t2.id, o2) for t2, o2 in v])
    return prod(corners)


# part2

def _stitch_image():
    # TODO: have all tiles in place with exact conns - need to create full image
    class Cell(NamedTuple):
        tile: Tile
        orientation: str
        rotation: int

    fname = '20.test'
    data = _parse_data(fname)
    conns = _get_connections(fname)

    # need tile, orientation (border), rotation
    cur_rot = 0

    (t1, o1), neighbors = first(conns.items())
    starter_cell = Cell(t1, o1, 0)
    used = {t1}

    # def _place(cur_cell: Cell, neighbor: )


def part2():
    pass


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
