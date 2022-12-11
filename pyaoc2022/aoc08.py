from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from itertools import accumulate
from math import prod
from typing import Optional, TypeAlias
from rich import print

from pyaoc2019.utils import read_file, timer, Coord


# lol decided to approach the first way in a time efficient but way overly complicated manner.
# ==============================================================================
# part 1 complicated
# ==============================================================================


def rot90(grid, n=1):
    """rotate grid 90 degrees clockwise"""
    for _ in range(n):
        grid = [list(reversed(r)) for r in zip(*grid)]
    return grid


def display(grid):
    """print grid out reasonably"""
    print('==================')
    print('\n'.join(map(str, grid)))


def cum_max(grid, orientation: int):
    """
    orientation: 0 -> cum_max from left
    orientation: 1 -> cum_max from bottom
    orientation: 2 -> cum_max from right
    orientation: 3 -> cum_max from top
    """
    cur = rot90(grid, orientation)
    res = [list(accumulate(r, max)) for r in cur]
    return rot90(res, 4 - orientation)


# row, column
offsets = [
    (0, -1),  # from left
    (1, 0),  # from bottom
    (0, 1),  # from right
    (-1, 0),  # from top
]


def create_offset_cum_max_map(grid):
    """when checking a grid to see if it's blocked, what offset maps to what cum_max grid"""
    return {offset: cum_max(grid, n) for n, offset in enumerate(offsets)}


RC: TypeAlias = tuple[int, int]


def get_inner_grid_as_coord_value_map(grid) -> dict[RC, int]:
    """convert  grid"""
    inner = [r[1:-1] for r in grid[1:-1]]
    return {
        (r_idx, c_idx): v for r_idx, row in enumerate(inner, 1) for c_idx, v in enumerate(row, 1)
    }


def parse_data(name):
    return [[int(v) for v in l] for l in read_file(name)]


@timer
def part1(grid):
    """get total number of trees seen from any position outside of the grid"""
    total_seen = len(grid) * 4 - 4
    maxes = create_offset_cum_max_map(grid)
    inner = get_inner_grid_as_coord_value_map(grid)
    for rc, v in inner.items():
        for (r_o, c_o), cum_max in maxes.items():
            r, c = rc
            if v > cum_max[r + r_o][c + c_o]:  # type: ignore
                total_seen += 1
                break
    return total_seen


grid = parse_data(8)
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

display(grid)
display(rot90(grid, 1))
display(rot90(grid, 2))
display(rot90(grid, 3))

display(cum_max(grid, 2))
print(get_inner_grid_as_coord_value_map(grid))

# ==============================================================================
# part2
# ==============================================================================
def _to_coord_height_map(grid):
    return {
        Coord(r_idx, c_idx): v
        for r_idx, row in enumerate(grid)
        for c_idx, v in enumerate(row)
    }  # fmt: skip


def _calc_num_can_see(coord_height_map, cur_height, rc, offset):
    nxt = rc + offset
    if (height := coord_height_map.get(nxt)) is None:
        return 0

    if cur_height <= height:
        return 1

    return 1 + _calc_num_can_see(coord_height_map, cur_height, nxt, offset)


def part2(grid):
    coord_height_map = _to_coord_height_map(grid)
    res = {
        rc: prod(_calc_num_can_see(coord_height_map, height, rc, offset) for offset in offsets)
        for rc, height in coord_height_map.items()
    }

    return max(res.values())


# ==============================================================================
# part1 simple
# ==============================================================================


def _check_visible(coord_height_map, target_height, rc, offset) -> bool:
    nxt = rc + offset
    if (height := coord_height_map.get(nxt)) is None:
        return True

    if target_height <= height:
        return False

    return _check_visible(coord_height_map, target_height, nxt, offset)


@timer
def part1_simple(grid):
    coord_height_map = _to_coord_height_map(grid)
    return sum(
        any(_check_visible(coord_height_map, height, rc, offset) for offset in offsets)
        for rc, height in coord_height_map.items()
    )


grid = parse_data(8)
print(part1(grid))
print(part2(grid))
print(part1_simple(grid))
