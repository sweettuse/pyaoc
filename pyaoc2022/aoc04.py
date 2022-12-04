from __future__ import annotations
from dataclasses import dataclass

from pyaoc2019.utils import read_file


@dataclass
class Range:
    """inclusive range"""

    start: int
    end: int

    @classmethod
    def from_str(cls, s) -> Range:
        return cls(*map(int, s.split('-')))

    def __contains__(self, other):
        return self.start <= other.start and other.end <= self.end

    def __and__(self, other) -> bool:
        return (
            self.start <= other.end <= self.end
            or self.start <= other.start <= self.end
            or self in other
        )


def parse_file(name):
    return [tuple(map(Range.from_str, l.split(','))) for l in read_file(name)]


def part1(name):
    return sum(a in b or b in a for a, b in parse_file(name))


def part2(name):
    return sum(a & b for a, b in parse_file(name))


print(part1(4))
print(part2(4))
