from collections import defaultdict
from enum import Enum
from functools import cache
from itertools import starmap, combinations, product
from math import prod
from typing import List, NamedTuple, Dict, Set, Tuple

from frozendict import frozendict
from more_itertools import first

from pyaoc2019.utils import read_file, Coord

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


# ======================================================================================================================
def _flip_ew(b: List[str]):
    return [''.join(reversed(r)) for r in b]


def _rotate(b: List[str]):
    return list(map(''.join, zip(*reversed(b))))


def _transpose(b: List[str]):
    return list(map(''.join, zip(*b)))


# ======================================================================================================================

def _to_int(s, reverse=False):
    repl = {'.': '0', '#': '1'}
    if reverse:
        s = reversed(s)
    return int((''.join(repl[c] for c in s)), 2)


BorderDict = Dict[Dir, int]


def _to_border_dict(borders: List[str]) -> BorderDict:
    n, s = borders[0], borders[-1]
    borders = _transpose(borders)
    w, e = borders[0], borders[-1]
    ints = _to_int(n), _to_int(e), _to_int(s, True), _to_int(w, True)
    return frozendict(zip(Dir, ints))


class Tile(NamedTuple):
    id: int
    orig: BorderDict
    flipped: BorderDict

    @classmethod
    def from_data(cls, id: int, borders: List[str]):
        orig = _to_border_dict(borders)
        flipped = _to_border_dict(_flip_ew(borders))
        return cls(id, orig, flipped)

    @cache
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
# PART 1
# ======================================================================================================================
class Tile2(NamedTuple):
    id: int
    orientation: BorderDict


def _get_connections(fname='20.test') -> Dict[Tile2, Tile2]:
    data = _parse_data(fname)
    res = defaultdict(set)
    for t1, t2 in combinations(data, 2):
        for o1, o2 in product(('orig', 'flipped'), repeat=2):
            nt1 = Tile2(t1.id, getattr(t1, o1))
            nt2 = Tile2(t2.id, getattr(t2, o2))
            if set(nt1.orientation.values()) & set(nt2.orientation.values()):
                res[nt1].add(nt2)
                res[nt2].add(nt1)
    return res


def part1():
    conns = _get_connections(20)
    corners = set()
    for t1, v in conns.items():
        if len(v) == 2:
            corners.add(t1.id)
    return prod(corners)


# ======================================================================================================================
# PART 2
# ======================================================================================================================


def part2():
    class DirTile(NamedTuple):
        dir: Dir
        tile: Tile2

        def __str__(self):
            return f'DirTile({self.dir}, {self.tile.id})'

        __repr__ = __str__

    class Cell:
        def __init__(self, tile: Tile2):
            self.tile = tile
            self.conns: Dict[Dir, DirTile] = self.get_neighbors(tile)

        @staticmethod
        def get_neighbors(tile):
            res = {}
            my_vals = {v: k for k, v in tile.orientation.items()}
            for n in conns[tile]:
                other_vals = {v: k for k, v in n.orientation.items()}
                for k in my_vals.keys() & other_vals.keys():
                    res[my_vals[k]] = DirTile(other_vals[k], n)

            return res

        def __hash__(self):
            return hash(self.tile)

        def __eq__(self, other):
            return self.tile == other.tile

        def __str__(self):
            return f'Cell({self.tile.id}, {self.conns})'

        __repr__ = __str__

    def _get_other_rotation(cur_rot: Dir, cur_to_other: Dir, other_to_cur: Dir) -> Dir:
        """
        cur_to_other -> other_to_cur: rot
        n -> n: +2 / 0
        n -> e: +1 / -1
        n -> s: +0 / -2
        n -> w: +3 / -3
        """
        return cur_rot.from_offset((rot_map[cur_to_other] - rot_map[other_to_cur] + 2) % 4)

    def _get_dir_to_other(t1: Tile2, t2: Tile2, rot: Dir):
        pass

    def _add_to_grid(cell: Cell, coord: Coord = Coord(0, 0), rot: Dir = Dir.n):
        if cell in processed:
            return

        processed.add(cell)
        grid[coord] = rot, cell
        for cur_to_other, (other_to_cur, other_tile) in cell.conns.items():
            abs_dir_to_other = _get_dir_to_other(cell.tile, other_tile, rot)
            other_rot = _get_other_rotation(rot, cur_to_other, other_to_cur)
            _add_to_grid(Cell(other_tile), coord + abs_dir_to_other.value, other_rot)

    grid: Dict[Coord, Tuple[Dir, Tile2]] = {}
    conns = _get_connections('20.test')
    cells: Set[Cell] = set(map(Cell, conns))
    start = first(cells)
    processed: Set[Cell] = set()
    print(start)


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
