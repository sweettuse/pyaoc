import sys
from functools import reduce
from itertools import starmap
from operator import add

from pyaoc2019.utils import read_file, Coord, mapt

__author__ = 'acushner'


def parse_inst(inst):
    cmd, val = inst.split()
    return cmd, int(val)


insts = mapt(parse_inst, read_file(2, 2021))


# insts = mapt(parse_inst, read_file('02.test', 2021))


def part1():
    def to_coord(cmd, val):
        match cmd:
            case 'forward':
                return Coord(val, 0)
            case 'down':
                return Coord(0, val)
            case 'up':
                return Coord(0, -val)

    res = reduce(add, starmap(to_coord, insts))
    return res.x * res.y


def part2():
    aim = 0
    x = depth = 0
    for cmd, val in insts:
        match cmd:
            case 'forward':
                x += val
                depth += aim * val
            case 'down':
                aim += val
            case 'up':
                aim -= val

    return x * depth


def __main():
    print(part1())
    print(part2())


if __name__ == '__main__':
    __main()
