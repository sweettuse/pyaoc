from typing import NamedTuple, List

from cytoolz import first

from pyaoc2019.utils import Direction, Coord, read_file

__author__ = 'acushner'


def _turn_right(d: Direction):
    return d.rotated(1)


def _turn_left(d: Direction):
    return d.rotated(0)


turns = dict(R=_turn_right, L=_turn_left)


class Inst(NamedTuple):
    direction: str
    steps: int

    @classmethod
    def from_str(cls, s):
        return cls(first(s), int(s[1:]))


def aoc01_a(insts: List[Inst]):
    cur = Coord(0, 0)
    dir = Direction.up
    for i in insts:
        dir = turns[i.direction](dir)
        cur += dir.value * i.steps

    return cur.manhattan


def aoc01_b(insts: List[Inst]):
    cur = Coord(0, 0)
    dir = Direction.up
    seen = {cur}
    for i in insts:
        dir = turns[i.direction](dir)
        for _ in range(i.steps):
            cur += dir.value
            if cur in seen:
                return cur.manhattan
            seen.add(cur)


def __main():
    strs = first(read_file(1, 2016)).split(',')
    instructions = [Inst.from_str(s.strip()) for s in strs]
    print(instructions)
    print(aoc01_a(instructions))
    print(aoc01_b(instructions))
    pass


if __name__ == '__main__':
    __main()
