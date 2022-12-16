from __future__ import annotations
from collections import defaultdict
from typing import NamedTuple, Optional
from rich import print

from pyaoc2019.utils import Coord, get_all_ints, read_file, mapt, timer


class Range(NamedTuple):
    """inclusive. represent covered range by sensor on a single axis"""

    start: int
    end: int
    exclude: Optional[int] = None  # if beacon present

    @property
    def num_covered(self) -> int:
        return self.end - self.start + 1 - (self.exclude is not None)

    @staticmethod
    def num_covered_multiple(ranges: list[Range]) -> int:
        excluded = {r.exclude for r in ranges} - {None}
        bounds = defaultdict(int)
        for r in ranges:
            bounds[r.start] += 1
            bounds[r.end] -= 1

        s_bounds = sorted((pos, v) for pos, v in bounds.items() if v)

        cur = 0
        total = 0
        starts, ends = [], []
        for pos, val in s_bounds:
            if cur == 0 and val > 0:
                starts.append(pos)
                start = pos
            if cur != 0 and cur + val == 0:
                ends.append(pos)
                total += pos - start + 1
            cur += val

        return total - len(excluded)

    @staticmethod
    def missing(ranges: list[Range]) -> Optional[int]:
        bounds = defaultdict(int)
        for r in ranges:
            bounds[min(4000000, max(r.start, 0))] += 1
            bounds[min(4000000, max(r.end, 0))] -= 1

        s_bounds = sorted((pos, v) for pos, v in bounds.items() if v)

        cur = 0
        total = 0
        starts, ends = [], []
        for pos, val in s_bounds:
            if cur == 0 and val > 0:
                starts.append(pos)
                start = pos
            if cur != 0 and cur + val == 0:
                ends.append(pos)
                total += pos - start + 1
            cur += val
        if starts != [0] or ends != [4000000]:
            return ends[0] + 1


class SB(NamedTuple):
    sensor: Coord
    beacon: Coord

    @property
    def manhattan(self):
        return (self.sensor - self.beacon).manhattan

    @classmethod
    def from_str(cls, s: str) -> SB:
        x1, y1, x2, y2 = get_all_ints(s)
        sensor = Coord(x1, y1)
        beacon = Coord(x2, y2)
        return cls(sensor, beacon)

    def project(self, y) -> Optional[Range]:
        if (y_diff := abs(self.sensor.y - y)) > self.manhattan:
            return None

        remaining = self.manhattan - y_diff
        return Range(
            self.sensor.x - remaining,
            self.sensor.x + remaining,
            self.beacon.x if self.beacon.y == y else None,
        )


def parse_data(name):
    return mapt(SB.from_str, read_file(name))


def part1(name, row):
    sbs = parse_data(name)
    ranges = list(filter(bool, (sb.project(row) for sb in sbs)))
    return Range.num_covered_multiple(ranges)


@timer
def part2(sbs: tuple[SB, ...]):
    """brute force way through projecting onto each row to find the one missing space

    would take about 3 minutes on my i9 macbook pro from 2019 to scan all 4 million rows

    i'm sure there's a better way.
    """
    for row in range(3100000, 4000001):
        ranges = list(filter(bool, (sb.project(row) for sb in sbs)))
        if (missing := Range.missing(ranges)) is not None:
            return missing * 4000000 + row


sbs = parse_data(15)
print(part1(15, 2000000))
print(part2(sbs))
