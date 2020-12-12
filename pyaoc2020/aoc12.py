from enum import Enum
from typing import NamedTuple

from pyaoc2019.utils import read_file, timer, Coord

__author__ = 'acushner'

data = read_file(12, 2020)


class Dir(Enum):
    N = Coord(0, 1)
    E = Coord(1, 0)
    S = Coord(0, -1)
    W = Coord(-1, 0)

    def rotate(self, dir, units):
        mult = 1 if dir == 'R' else -1
        return _list_dirs[(_list_dirs.index(self) + mult * units // 90) % len(_list_dirs)]


_list_dirs = list(Dir)


class Inst(NamedTuple):
    dir: str
    units: int

    @classmethod
    def from_str(cls, s):
        inst, units = s[0], s[1:]
        return cls(inst, int(units))


def part1():
    cur_dir = Dir.E
    cur_pos = Coord(0, 0)

    for dir, units in map(Inst.from_str, data):
        if dir in 'LR':
            cur_dir = cur_dir.rotate(dir, units)
        elif dir == 'F':
            cur_pos += cur_dir.value * units
        else:
            cur_pos += Dir[dir].value * units

    return cur_pos.manhattan


def part2():
    cur_pos = Coord(0, 0)
    cur_waypoint = Coord(10, 1)

    def _rotate_waypoint(diff):
        num_times = units // 90
        if dir == 'L':
            num_times = (4 - num_times) % 4

        for _ in range(num_times):
            diff = Coord(diff.y, -diff.x)

        return diff

    for dir, units in map(Inst.from_str, data):
        if dir in 'LR':
            cur_waypoint = cur_pos + _rotate_waypoint(cur_waypoint - cur_pos)
        elif dir == 'F':
            waypoint_diff = cur_waypoint - cur_pos
            cur_pos += waypoint_diff * units
            cur_waypoint = cur_pos + waypoint_diff
        else:
            cur_waypoint += Dir[dir].value * units

    return cur_pos.manhattan


@timer
def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
