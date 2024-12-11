from __future__ import annotations
from rich import print as rprint

from pyaoc2019.utils import RC, read_file, Direction


def _read_data(*, test: bool) -> dict[RC, int]:
    fname = "10.test.txt" if test else "10.txt"
    return {
        RC(r, c): int(v)
        for r, row in enumerate(read_file(fname))
        for c, v in enumerate(row)
    }


def _trailhead_score(data: dict[RC, int], start: RC) -> int:
    points = [(start, data[start])]
    visited = set()
    res = set()
    while points:
        cur, height = points.pop()
        if cur in visited:
            continue
        visited.add(cur)
        if height == 9:
            res.add(cur)
            continue

        for d in Direction:
            if data.get(cur + d.value) == height + 1:
                points.append((cur + d.value, height + 1))

    return len(res)


def part1(data) -> int:
    return sum(_trailhead_score(data, rc) for rc, v in data.items() if v == 0)


def _trailhead_rating(data: dict[RC, int], start: RC) -> int:
    points = [(start, data[start], (start,))]
    visited = set()
    res = set()
    while points:
        cur, height, path = points.pop()
        if path in visited:
            continue
        visited.add(path)
        if height == 9:
            res.add(path)
            continue

        for d in Direction:
            if data.get(nxt := cur + d.value) == height + 1:
                points.append((nxt, height + 1, path + (nxt,)))

    return len(res)


def part2(data):
    return sum(_trailhead_rating(data, rc) for rc, v in data.items() if v == 0)


def _main():
    data = _read_data(test=False)

    print(part1(data))
    print(part2(data))


if __name__ == "__main__":
    _main()
