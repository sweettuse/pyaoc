from __future__ import annotations
from collections import defaultdict, deque
from itertools import count, product, starmap

from pyaoc2019.utils import RC, exhaust, read_file, timer
from rich import print


N = RC(-1, 0)
E = RC(0, 1)
S = RC(1, 0)
W = RC(0, -1)

norths = {N, N + W, N + E}
souths = {S, S + W, S + E}
wests = {W, W + N, W + S}
easts = {E, E + N, E + S}

orig_directions = N, S, W, E
directions = deque(orig_directions)
checks = dict(zip(orig_directions, (norths, souths, wests, easts)))

surrounding = set(starmap(RC, product(range(-1, 2), repeat=2))) - {RC(0, 0)}


class NoMove(Exception):
    pass


def parse_data(name):
    return {
        RC(r, c)
        for r, row in enumerate(read_file(name))
        for c, val in enumerate(row) if val == '#'
    }  # fmt: skip


def _min_max(elves):
    min_r = min(r for r, _ in elves)
    min_c = min(c for _, c in elves)
    max_r = max(r for r, _ in elves)
    max_c = max(c for _, c in elves)
    return RC(min_r, min_c), RC(max_r, max_c)


def _with_offsets(pos, offsets):
    return {pos + o for o in offsets}


def _move(e: RC, elves: set[RC]):
    if not _with_offsets(e, surrounding) & elves:
        return e

    for d in directions:
        if not _with_offsets(e, checks[d]) & elves:
            return e + d

    return e


def _first_half(elves):
    moves = defaultdict(list)
    i_think_it_moved = False

    for e in elves:
        new_pos = _move(e, elves)
        i_think_it_moved |= (new_pos != e)
        moves[new_pos].append(e)

    if not i_think_it_moved:
        raise NoMove

    directions.rotate(-1)
    return set(_second_half(moves))


def _second_half(moves):
    for target, cur in moves.items():
        if len(cur) > 1:
            yield from iter(cur)
        else:
            yield target


def _calc_empty(elves):
    min_rc, max_rc = _min_max(elves)
    return (max_rc.r - min_rc.r + 1) * (max_rc.c - min_rc.c + 1) - len(elves)


def _display(elves):
    (min_r, min_c), (max_r, max_c) = _min_max(elves)
    res = [
        ['#' if RC(r, c) in elves else '.' for c in range(min_c, max_c + 1)]
        for r in range(min_r, max_r + 1)
    ]
    exhaust(print, map(''.join, res))
    print('====================')


@timer
def part1(name):
    global directions
    directions = deque(orig_directions)
    elves = parse_data(name)
    for _ in range(10):
        elves = _first_half(elves)
    return _calc_empty(elves)


@timer
def part2(name):
    global directions
    directions = deque(orig_directions)
    elves = parse_data(name)
    for i in count(1):
        try:
            elves = _first_half(elves)
        except NoMove:
            return i


print(part1(23))
print(part2(23))
