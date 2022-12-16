from __future__ import annotations
from dataclasses import dataclass
from itertools import repeat

from pyaoc2019.utils import read_file, Coord as CoordOrig, mapt


def _sign(v):
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


class Coord(CoordOrig):
    @property
    def signed(self):
        return type(self)(*map(_sign, self))


dirs = dict(
    u=Coord(0, 1),
    d=Coord(0, -1),
    l=Coord(-1, 0),
    r=Coord(1, 0),
)


@dataclass
class Inst:
    dir: Coord
    num: int

    @classmethod
    def from_str(cls, s) -> Inst:
        d, n = s.split()
        return cls(dirs[d.lower()], int(n))


# . a b c .
# d . . . e
# f . H . g
# h . . . i
# . j k l .

# b, f, g, h - same row OR same col, move in that direction
# d, e, h, i - col off by 2, mv diag toward
# a, c, j, l - row off by 2, mv diag toward


def move_tail(head: Coord, tail: Coord) -> Coord:
    """return offset to move tail"""
    diff = head - tail
    if max(map(abs, diff)) == 1:
        return tail

    return tail + (head - tail).signed


assert move_tail(Coord(0, 0), Coord(0, 0)) == Coord(0, 0)
assert move_tail(Coord(0, 2), Coord(0, 0)) == Coord(0, 1)
assert move_tail(Coord(2, 2), Coord(1, 1)) == Coord(1, 1)
assert (res := move_tail(Coord(2, 2), Coord(4, 2))) == Coord(3, 2), res
assert (res := move_tail(Coord(1, 1), Coord(3, 2))) == Coord(2, 1), res
assert (res := move_tail(Coord(1, 1), Coord(3, 2))) == Coord(2, 1), res
assert (res := move_tail(Coord(4, 2), Coord(3, 0))) == Coord(4, 1), res


def parse_data(name):
    return mapt(Inst.from_str, read_file(name))


def _offsets(insts: tuple[Inst, ...]):
    for inst in insts:
        yield from repeat(inst.dir, inst.num)


def part1(insts):
    head = tail = Coord(0, 0)
    seen = {tail}
    for offset in _offsets(insts):
        head += offset
        tail = move_tail(head, tail)
        seen.add(tail)
    return len(seen)


insts = parse_data(9)


def parts1and2(insts, num_knots):
    knots = [Coord(0, 0)] * num_knots
    visited = {knots[-1]}
    total_insts = 0
    for offset in _offsets(insts):
        total_insts += 1
        knots[0] += offset
        for i in range(len(knots) - 1):
            h, t = knots[i], knots[i + 1]
            knots[i + 1] = move_tail(h, t)
        visited.add(knots[-1])
    return len(visited)


print(parts1and2(insts, 2))
print(parts1and2(insts, 10))
