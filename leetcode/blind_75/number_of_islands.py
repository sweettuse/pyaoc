__author__ = 'acushner'

from itertools import product
from typing import List, Tuple, Set

# https://leetcode.com/problems/number-of-islands/


offsets = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _find_connected(coords, coord) -> Set[Tuple[int, int]]:
    r, c = coord
    return {new_coord for (r1, c1) in offsets
            if (new_coord := (r + r1, c + c1)) in coords}


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        ones = {(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v == '1'}
        count = 0
        while ones:
            to_process = {ones.pop()}
            count += 1
            while to_process:
                c = to_process.pop()
                connections = _find_connected(ones, c)
                ones -= connections
                to_process.update(connections)
        return count


def __main():
    grid = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"]
    ]
    print(Solution().numIslands(grid))
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"]
    ]

    print(Solution().numIslands(grid))


if __name__ == '__main__':
    __main()
