from __future__ import annotations
from collections import defaultdict, deque
from typing import NamedTuple
from rich import print


from pyaoc2019.utils import read_file, RC, timer


def _height(char: str) -> int:
    return ord(char) - ord('a')


def parse_data(name):
    res = {}
    start = end = RC(0, 0)
    for r, row in enumerate(read_file(name)):
        for c, v in enumerate(row):
            rc = RC(r, c)
            if v == 'S':
                start, v = rc, 'a'
            elif v == 'E':
                end, v = rc, 'z'
            res[rc] = _height(v)
    return start, end, res


class WeightRC(NamedTuple):
    weight: int
    rc: RC


offsets = {
    RC(-1, 0),
    RC(1, 0),
    RC(0, -1),
    RC(0, 1),
}


def adjacency_list(d: dict[RC, int]) -> dict[RC, dict[RC, int]]:
    res = defaultdict(dict)
    for rc, height in d.items():
        for o in offsets:
            nxt = rc + o
            if (other_height := d.get(nxt)) is None:
                continue
            res[rc][nxt] = other_height - height

    return dict(res.items())


def find(grid, start, end):
    adj_list = adjacency_list(grid)
    visited: set[RC] = set()
    cost: dict[RC, int | float] = defaultdict(lambda: float('inf'))
    cost[start] = 0
    q = deque()
    q.append((0, start))

    while q:
        dist, cur = q.popleft()
        if cur in visited:
            continue
        visited.add(cur)

        dist = min(dist, cost[cur]) + 1
        for nxt, height_diff in adj_list[cur].items():
            if height_diff > 1:
                continue
            if cost[nxt] > dist:
                cost[nxt] = dist
            q.append((dist, nxt))
    return cost


def part1(name):
    start, end, grid = parse_data(name)
    cost = find(grid, start, end)
    return cost[end]


@timer
def part2(name):
    _, end, grid = parse_data(name)
    possible_starts = {rc for rc, height in grid.items() if height == 0}
    return min(find(grid, start, end)[end] for start in possible_starts)


print(part1(12))
print(part2(12))
