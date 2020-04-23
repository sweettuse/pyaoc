import string
from enum import Enum
from itertools import count

from cytoolz.itertoolz import first

import pyaoc2019.utils as U
from pyaoc2019.utils import Coord

__author__ = 'acushner'


class Direction(Enum):
    up = Coord(0, -1)
    right = Coord(1, 0)
    down = Coord(0, 1)
    left = Coord(-1, 0)

    def rotated(self, val):
        """
        0: rotate 90 deg counter-clockwise
        1: rotate 90 deg clockwise
        """
        dirs = list(Direction)
        val = 2 * val - 1
        new_idx = (dirs.index(self) + val) % len(dirs)
        return dirs[new_idx]


def parse_file(fn):
    rows = U.read_file(fn, 2017, do_strip=False)
    return {Coord(c_num, r_num): v
            for r_num, r in enumerate(rows)
            for c_num, v in enumerate(r)
            if v not in set(' \n')}


def aoc19(network):
    cur_pos, cur_val = first(network.items())
    cur_dir = Direction.down
    letter_path = []
    target_letters = set(string.ascii_uppercase) & set(network.values())
    straight = set('-|') | target_letters
    for step_total in count(1):
        if cur_val in straight:
            # continue straight
            if cur_val in target_letters:
                letter_path.append(cur_val)
                if cur_pos + cur_dir.value not in network:
                    return ''.join(letter_path), step_total

        elif cur_val == '+':
            # turn
            for v in 0, 1:
                next_dir = cur_dir.rotated(v)
                if cur_pos + next_dir.value in network:
                    cur_dir = next_dir
                    break

        cur_pos += cur_dir.value
        cur_val = network[cur_pos]


def __main():
    network = parse_file(19)
    print(aoc19(network))

    pass


if __name__ == '__main__':
    __main()
