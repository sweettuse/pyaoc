from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import starmap, combinations, permutations, product
from math import prod
from typing import List, NamedTuple, Dict, Set, Tuple

from cytoolz import memoize
from more_itertools import first

from pyaoc2019.aoc13 import cached_property
from pyaoc2019.utils import read_file, timer, exhaust, Coord

__author__ = 'acushner'


class Dir(Enum):
    n = Coord(0, 1)
    e = Coord(1, 0)
    s = Coord(0, -1)
    w = Coord(-1, 0)

    def from_offset(self, offset: int):
        return rot_map[(rot_map[self] + offset) % 4]


rot_map = dict(zip(Dir, range(4)))
rot_map.update({v: k for k, v in rot_map.items()})


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


def _rotate(b: List[str]):
    return list(map(''.join, zip(*reversed(b))))


def _transpose(b: List[str]):
    return list(map(''.join, zip(*b)))


# ======================================================================================================================


def _num_borders(edge: int):
    return 2 * edge * (edge + 1)


def _shared_borders(edge: int):
    return _num_borders(edge) - 4 * edge


def _get_connections(fname='20.test'):
    data = _parse_data(fname)
    res = defaultdict(set)
    for t1, t2 in combinations(data, 2):
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
    return prod(corners)


# part2
class Cell:
    def __init__(self, tile: Tile, orientation: str):
        self.tile = tile
        self.orientation = orientation
        self.conns: Dict[Dir, Tuple[Dir, Cell]] = {}

    def stitch(self, other: 'Cell'):
        my_bord, other_bord = self.border, other.border
        for my_dir, other_dir in product('nesw', repeat=2):
            if getattr(my_bord, my_dir) == getattr(other_bord, other_dir):
                my_dir, other_dir = Dir[my_dir], Dir[other_dir]
                self.conns[my_dir] = other_dir, other
                other.conns[other_dir] = my_dir, self

    def __hash__(self):
        return hash(self.tile) ^ hash(self.orientation)

    def __eq__(self, other):
        return self.tile == other.tile and self.orientation == other.orientation

    def __str__(self):
        return f'Cell({self.tile.id}, {self.orientation}, {len(self.conns)})'

    __repr__ = __str__

    @property
    def border(self):
        return getattr(self.tile, self.orientation)


def _stitch_image():
    fname = '20.test'
    conns = _get_connections(fname)

    def _add_neighbors(cur: Cell, res: Set[Cell]):
        if cur in res:
            return
        res.add(cur)

        neighbors = conns.get((cur.tile, cur.orientation))
        if not neighbors:
            raise ValueError('should have neighbors!')

        for other in starmap(Cell, neighbors):
            cur.stitch(other)
            _add_neighbors(other, res)

    res_a, res_b = set(), set()
    t, o = first(conns)
    _add_neighbors(Cell(t, o), res_a)
    _add_neighbors(Cell(t, 'flipped' if o == 'orig' else 'orig'), res_b)

    return res_a, res_b


class Dir(Enum):
    n = Coord(0, 1)
    e = Coord(1, 0)
    s = Coord(0, -1)
    w = Coord(-1, 0)

    def from_offset(self, offset: int):
        return rot_map[(rot_map[self] + offset) % 4]


rot_map = dict(zip(Dir, range(4)))
rot_map.update({v: k for k, v in rot_map.items()})


def _transform_to_grid(image: Set[Cell]):
    def _get_other_rotation(cur_rot: Dir, cur_to_other: Dir, other_to_cur: Dir) -> Dir:
        """
        cur_to_other -> other_to_cur: rot
        n -> n: +2 / 0
        n -> e: +1 / -1
        n -> s: +0 / -2
        n -> w: +3 / -3
        """
        return cur_rot.from_offset((rot_map[cur_to_other] - rot_map[other_to_cur] + 2) % 4)

    def _add_to_grid(cur_cell: Cell, cur_coord: Coord = Coord(0, 0), cur_rot: Dir = Dir.n):
        if cur_cell in processed:
            return

        processed.add(cur_cell)
        if cur_coord in grid:
            a = 4
        grid[cur_coord] = cur_rot, cur_cell
        for dir, (other_dir, other_cell) in cur_cell.conns.items():
            mod_rot = rot_map[(rot_map[dir] + rot_map[cur_rot]) % 4]
            print(cur_cell.tile.id, dir, cur_rot)
            other_coord = cur_coord + mod_rot.value
            _add_to_grid(other_cell, other_coord, _get_other_rotation(cur_rot, dir, other_dir))

    grid: Dict[Coord, Tuple[Dir, Cell]] = {}
    processed: Set[int] = set()
    _add_to_grid(first(image))
    # for cell in image:
    #     print(cell.tile.id)
    #     for _, v in cell.conns.values():
    #         print('\t', v.tile.id)
    # print((image - processed).pop().tile.id)
    # print(_get_other_rotation(Dir.n, Dir.n, Dir.n))
    print(len(image), len(grid), len(processed), processed)
    print('=============')
    # print(min(grid.keys()), max(grid.keys()))
    return grid


def part2():
    image_a, image_b = _stitch_image()
    # grid = _transform_to_grid(image_a)
    grid = _transform_to_grid(image_b)


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
