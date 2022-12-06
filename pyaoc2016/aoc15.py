from __future__ import annotations
from math import prod
from operator import attrgetter
from typing import NamedTuple

from pyaoc2019.utils import timer

discs_real = """
Disc #1 has 7 positions; at time=0, it is at position 0.
Disc #2 has 13 positions; at time=0, it is at position 0.
Disc #3 has 3 positions; at time=0, it is at position 2.
Disc #4 has 5 positions; at time=0, it is at position 2.
Disc #5 has 17 positions; at time=0, it is at position 0.
Disc #6 has 19 positions; at time=0, it is at position 7.
"""

discs_test = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""
from rich import print


class Disc(NamedTuple):
    depth: int
    num_pos: int
    start: int

    @classmethod
    def from_str(cls, s: str):
        _, depth, _, num_pos, *_, start = s.split()
        depth, num_pos, start = int(depth[1]), int(num_pos), int(start[0])
        return cls(depth, num_pos, start)

    def pos_at(self, offset):
        return (self.start + self.depth + offset) % self.num_pos


class Discs:
    def __init__(self, discs: list[Disc]):
        self.discs = discs

    @classmethod
    def from_str(cls, s: str):
        return cls([Disc.from_str(l) for l in s.splitlines() if l])

    def success(self, time) -> bool:
        return not any(d.pos_at(time) for d in self.discs)

    @timer
    def parts1and2(self):
        max_disc = max(self.discs, key=attrgetter('num_pos'))
        for time in range(10_000_000):
            if self.success(time):
                print(time)
                break

    @property
    def pretty(self) -> None:
        print(self.discs)


def __main():
    discs = Discs.from_str(discs_real)
    discs.parts1and2()
    discs.discs.append(Disc(7, 11, 0))
    discs.pretty
    discs.parts1and2()


if __name__ == '__main__':
    __main()
