__author__ = 'acushner'

# 8.2 Robot in a Grid: Imagine a robot sitting on the upper left corner of grid with r rows and c columns.
# The robot can only move in two directions, right and down, but certain cells are "off limits" such that
# the robot cannot step on them. Design an algorithm to find a path for the robot from the top left to
# the bottom right.

from functools import lru_cache
from typing import List, Set, Tuple, Optional

grid = [
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

RC = Tuple[int, int]
Grid = List[List[int]]


def get_blockers(grid) -> Set[RC]:
    return {(r_idx, c_idx)
            for r_idx, row in enumerate(grid)
            for c_idx, v in enumerate(row)
            if v == 1}


def path(grid: Grid):
    """recursive"""
    num_rows = len(grid)
    num_cols = len(grid[-1])
    target = num_rows - 1, num_cols - 1
    blocked = get_blockers(grid)

    @lru_cache(None)
    def rec(cur: RC) -> Optional[List[RC]]:
        r, c = cur
        if cur in blocked or r >= num_rows or c >= num_cols:
            return

        if cur == target:
            return [cur]

        if (res := rec((r + 1, c))) or (res := rec((r, c + 1))):
            return [cur, *res]

    return rec((0, 0))


def path_dfs(grid: Grid):
    """depth-first search"""
    num_rows, num_cols = len(grid), len(grid[-1])
    target = num_rows - 1, num_cols - 1
    blocked = get_blockers(grid)
    to_process = [start := (0, 0)]
    previous = {start: None}

    def _is_valid(cur):
        r, c = cur
        return not (cur in blocked or r >= num_rows or c >= num_cols)

    def _get_path():
        n = target
        res = [n]
        while n := previous.get(n):
            res.append(n)
        res.reverse()
        return res

    while to_process:
        r, c = cur = to_process.pop()

        for n in ((r + 1, c), (r, c + 1)):
            if n == target:
                previous[n] = cur
                return _get_path()

            if _is_valid(n):
                to_process.append(n)
                previous[n] = cur


def display(grid, vals):
    g = [['X' if v else ' ' for v in row] for row in grid]

    for r, c in vals:
        g[r][c] = '.'

    print('_' * (len(g[0]) + 2))
    for r in g:
        print('|' + ''.join(r) + '|')
    print('-' * (len(g[0]) + 2))


def __main():
    display(grid, path(grid))
    display(grid, path_dfs(grid))
    pass


if __name__ == '__main__':
    __main()
