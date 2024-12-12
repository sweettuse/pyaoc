from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import groupby, pairwise

from more_itertools import first
from rich import print as rprint

from pyaoc2019.utils import Direction, read_file, RC


def _read_data(*, test: bool) -> dict[RC, str]:
    fname = "12.test.txt" if test else "12.txt"
    return {
        RC(r, c): v for r, row in enumerate(read_file(fname)) for c, v in enumerate(row)
    }


@dataclass
class Fill:
    veggie: str
    rcs: set[RC]
    fences: dict[RC, set[RC]]

    @property
    def cost(self):
        return self.area * self.perimeter

    @property
    def discounted_cost(self):
        return self.area * self.sides

    @property
    def perimeter(self) -> int:
        return sum(map(len, self.fences.values()))

    @property
    def area(self) -> int:
        return len(self.rcs)

    @property
    def sides(self) -> int:
        """calc sides by first grouping by offset then figuring out contiguous lengths"""

        # group by offset
        offset_rc_map = defaultdict(set)
        for rc, offsets in self.fences.items():
            for offset in offsets:
                offset_rc_map[offset].add(rc)
        return sum(_calc_sides(*e) for e in offset_rc_map.items())


def _calc_sides(offset: RC, rcs: set[RC]) -> int:
    if offset.r == 0:
        first_gb, second_gb = 1, 0  # by col then row
    else:
        first_gb, second_gb = 0, 1  # by row then col

    # figure out contiguous lengths
    fs_map = defaultdict(list)
    for rc in rcs:
        fs_map[rc[first_gb]].append(rc[second_gb])

    return sum(map(_num_contiguous_groups, fs_map.values()))


def _num_contiguous_groups(vals: list[int]) -> int:
    return 1 + sum(v2 - v1 != 1 for v1, v2 in pairwise(sorted(vals)))


def _fill(garden: dict[RC, str], rc: RC) -> Fill:
    """fill a la ms paint contiguous areas"""
    points = [rc]
    seen = set()
    target = garden[rc]
    matches: set[RC] = set()
    fences: defaultdict[RC, set[RC]] = defaultdict(set)
    while points:
        cur = points.pop()
        if cur in seen:
            continue
        seen.add(cur)

        if garden[cur] != target:
            continue

        matches.add(cur)
        for d in Direction:
            offset = d.value.rc
            nxt = cur + offset
            if garden.get(nxt) == target:
                points.append(nxt)
            else:
                fences[cur].add(offset)
        points.append(cur)
    return Fill(target, matches, dict(fences))


def _get_fills(data) -> list[Fill]:
    garden = data.copy()
    points = set(garden)

    res = []
    while points:
        cur = points.pop()
        f = _fill(garden, cur)
        res.append(f)
        points -= f.rcs

    return res


def part1(fills: list[Fill]) -> int:
    return sum(f.cost for f in fills)


def part2(fills: list[Fill]) -> int:
    return sum(f.discounted_cost for f in fills)


def _main():
    data = _read_data(test=False)
    fills = _get_fills(data)

    print(part1(fills))
    print(part2(fills))


if __name__ == "__main__":
    _main()
