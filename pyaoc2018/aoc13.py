__author__ = 'acushner'

from copy import copy
from enum import Enum
from functools import partial
from itertools import count
from operator import itemgetter
from typing import NamedTuple, Tuple, Dict

from more_itertools import first

from pyaoc2019.utils import read_file, Coord, exhaust


class Turn(Enum):
    left = -1
    straight = 0
    right = 1


class Dir(Enum):
    up = Coord(0, -1)
    right = Coord(1, 0)
    down = Coord(0, 1)
    left = Coord(-1, 0)


dir_strs = '^>v<'

dirs = dict(zip(dir_strs, Dir))
dirs.update({v: k for k, v in dirs.items()})

curves = {
    '<\\': Dir.up, '</': Dir.down,
    '>/': Dir.up, '>\\': Dir.down,
    '^\\': Dir.left, '^/': Dir.right,
    'v/': Dir.left, 'v\\': Dir.right,
}

turns = list(Turn)

Track = Dict[Coord, str]


class Cart:
    def __init__(self, cur_dir: str):
        self.num_turns = 0
        self.cur_dir = cur_dir
        self._prev_move = None

    def move(self, coord, track: Track) -> Dir:
        cur_track = track[coord]

        if cur_track in set('-|'):
            return dirs[self.cur_dir]
        elif cur_track == '+':
            t = turns[self.num_turns % 3]
            self.num_turns += 1
            self.cur_dir = dir_strs[(dir_strs.index(self.cur_dir) + t.value) % len(dir_strs)]
            return dirs[self.cur_dir]
        elif cur_track in set('\\/'):
            next_dir = curves[f'{self.cur_dir}{cur_track}']
            self.cur_dir = dirs[next_dir]
            return next_dir

    def __str__(self):
        return f'Cart({self.cur_dir}, {self.num_turns})'

    __repr__ = __str__


def parse_map(filename=13):
    track = {Coord(c_num, r_num): v
             for r_num, row in enumerate(read_file(filename, 2018, do_strip=False))
             for c_num, v in enumerate(row)
             if v != ' '}

    carts = {}
    for coord, v in track.items():
        if v in set('<>^v'):
            track[coord] = '|' if v in set('v^') else '-'
            carts[coord] = Cart(v)

    return carts, track


def _update_cart(cart_coord, cart, track) -> Coord:
    return cart.move(cart_coord, track).value


def _avoid_accident(coord, carts, new_carts):
    """return True if no accident happened"""
    if coord in carts:
        carts.pop(coord)
    elif coord in new_carts:
        new_carts.pop(coord)
    else:
        return True


def tick(carts: Dict[Coord, Cart], track: Track, avoid_accidents=False):
    for c in count():
        new_carts = {}
        while carts:
            cart = carts.pop(coord := first(carts))
            coord += _update_cart(coord, cart, track)
            if avoid_accidents and not _avoid_accident(coord, carts, new_carts):
                continue
            elif coord in new_carts or coord in carts:
                return coord
            new_carts[coord] = cart
        if len(new_carts) == 1:
            return first(new_carts)
        carts = dict(sorted(new_carts.items(), key=lambda kv: (kv[0][1], kv[0][0])))


def part1():
    return tick(*parse_map())


def part2():
    return tick(*parse_map(), avoid_accidents=True)


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
