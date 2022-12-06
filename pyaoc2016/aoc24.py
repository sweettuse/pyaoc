from __future__ import annotations
from collections import deque
from itertools import chain, combinations, pairwise, permutations
from tkinter import W
from typing import TypeAlias


from pyaoc2019.utils import read_file, timer

Coord: TypeAlias = tuple[int, int]  # r, c


def parse_file(name) -> tuple[dict[str, Coord], set[Coord]]:
    """
    stops:
    """
    stops = {}
    valids = set()
    for r, line in enumerate(read_file(name, 2016)):
        for c, v in enumerate(line):
            if v == '#':
                continue

            valids.add((r, c))
            if v != '.':
                stops[v] = r, c

    return stops, valids


def _calc_pairwise_stops(stops, valids) -> dict[tuple[str, str], int]:
    res = {}
    for s1, s2 in combinations(stops, 2):
        r = res[s1, s2] = _calc_edge(stops[s1], stops[s2], valids)
        res[s2, s1] = r
    return res


def _get_surrounding(coord: Coord):
    r, c = coord
    return {
        (r + 1, c),
        (r - 1, c),
        (r, c + 1),
        (r, c - 1),
    }


def _calc_edge(s1: Coord, s2: Coord, valids: set[Coord]):
    """bfs to start"""

    q = deque()
    q.append((0, s1))
    seen = {s1}
    while q:
        length, cur = q.popleft()
        neighbors = (_get_surrounding(cur) & valids) - seen
        seen.update(neighbors)
        if s2 in neighbors:
            return length + 1
        q.extend((length + 1, n) for n in neighbors)


def _calc_total_distance(path, pairwise_stops) -> int:
    return sum(pairwise_stops[p1, p2] for p1, p2 in pairwise(path))


def _generate_paths(stops):
    s = set(stops)
    s -= {'0'}
    for p in permutations(s):
        yield chain('0', p)


def _generate_paths2(stops):
    s = set(stops)
    s -= {'0'}
    for p in permutations(s):
        yield chain('0', p, '0')


def __main():
    stops, valids = parse_file('24')
    pairwise_stops = _calc_pairwise_stops(stops, valids)
    part1 = min(_calc_total_distance(p, pairwise_stops) for p in _generate_paths(stops))
    print(f'{part1=}')
    part2 = min(
        _calc_total_distance(p, pairwise_stops) for p in _generate_paths2(stops)
    )
    print(f'{part2=}')


if __name__ == '__main__':
    __main()
