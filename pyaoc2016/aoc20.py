from __future__ import annotations
from typing import Iterable, NamedTuple
from pyaoc2019.utils import read_file
from rich import print

SAMPLE = list(
    filter(
        bool,
        """
919958672-920375477
886049087-888249849
3081919777-3120089489
3572627395-3574552561
""".splitlines(),
    )
)

DATA = read_file(20, 2016)


class Range(NamedTuple):
    start: int
    end: int

    @classmethod
    def from_str(cls, s: str) -> Range:
        return cls(*map(int, s.split('-')))

    def __or__(self, other) -> Range | None:
        s1, e1 = self
        s2, e2 = other

        if s2 <= s1 and e2 >= e1:
            return other
        if s2 >= s1 and e2 <= e1:
            return self
        if s2 <= s1 and e2 >= s1:
            return Range(s2, e1)
        if s2 <= e1 and e2 >= e1:
            return Range(s1, e2)

        if s2 == e1 + 1:
            return Range(s1, e2)
        elif s1 == e2 + 1:
            return Range(s2, e1)

        return None

    def __gt__(self, other):
        return self.start > other.end

    @property
    def num_disallowed(self) -> int:
        return self.end - self.start + 1



def _parse(data: Iterable[str]) -> list[tuple[int, int]]:
    return sorted(map(Range.from_str, data))


print(_parse(SAMPLE))


def _test():
    # overlap start
    print(Range(2, 4) | Range(3, 5))
    # overlap end
    print(Range(3, 5) | Range(2, 4))
    # subsume
    print(Range(1, 5) | Range(2, 3))
    # within
    print(Range(2, 3) | Range(1, 5))
    # adjacent
    print(Range(1, 2) | Range(3, 4))
    # unrelated
    print(Range(1, 2) | Range(4, 5))


def coalesce(data):
    res = []
    rngs = _parse(data)
    for rng in rngs:
        for i, r in enumerate(res):
            if (m := rng | r):
                res[i] = m
                break
        else:
            res.append(rng)
    return sorted(res)


def part1(data):
    return coalesce(data)[0].end + 1


def part2(data):
    return 2 ** 32 - sum(r.num_disallowed for r in coalesce(data))

def __main():
    _test()
    print(part1(DATA))
    print(part2(DATA))



__main()
