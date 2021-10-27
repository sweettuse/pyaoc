__author__ = 'acushner'

# 8.12 Eight Queens: Write an algorithm to print all ways of arranging eight queens on an 8x8 chess board
# so that none of them share the same row, column, or diagonal. In this case, "diagonal" means all
# diagonals, not just the two that bisect the board
from collections import defaultdict
from itertools import product
from typing import NamedTuple


class Store:
    def __init__(self):
        self._by_row = defaultdict(set)
        self._by_col = defaultdict(set)
        self._by_diag_ul = defaultdict(set)
        self._by_diag_ur = defaultdict(set)
        self._all = set()

    def add(self, rc):
        r, c = rc
        self._all.add(rc)
        self._by_row[r].add(rc)
        self._by_col[c].add(rc)
        self._by_diag_ul[r - c].add(rc)
        self._by_diag_ur[r + c].add(rc)

    def remove(self, rc):
        r, c = rc
        self._all -= self._by_row[r] | self._by_col[c] | self._by_diag_ul[r - c] | self._by_diag_ur[r + c]


class Board:
    def __init__(self, n=8):
        self._size = n
        self._board = [n * ['.'] for _ in range(n)]

    def __str__(self):
        return '\n'.join(''.join(r) for r in self._board)

    def __setitem__(self, rc, value):
        r, c = rc
        self._board[r][c] = value

    def __getitem__(self, rc_or_idx):
        if isinstance(rc_or_idx, tuple):
            r, c = rc_or_idx
            return self._board[r][c]
        return self._board[rc_or_idx]

    def keys(self):
        return list(product(range(self._size), repeat=2))

    def items(self):
        return [(k, self[k]) for k in self.keys()]


RC = tuple[int, int]


class Unused(NamedTuple):
    rows: frozenset[int]
    cols: frozenset[int]
    ul_diag: frozenset[int]
    ur_diag: frozenset[int]
    used: frozenset[RC] = frozenset()

    @classmethod
    def from_board(cls, b: Board):
        rows = cols = frozenset(range(8))
        ul_diag = frozenset(r - c for r, c in b.keys())
        ur_diag = frozenset(r + c for r, c in b.keys())
        return cls(rows, cols, ul_diag, ur_diag)

    def remove(self, rc: RC):
        r, c = rc
        rows = self.rows - {r}
        cols = self.cols - {c}
        ul_diag = self.ul_diag - {r - c}
        ur_diag = self.ur_diag - {r + c}
        return type(self)(rows, cols, ul_diag, ur_diag, self.used | {rc})

    def valid(self, rc):
        r, c = rc
        return r in self.rows and c in self.cols and r - c in self.ul_diag and r + c in self.ur_diag


def eight_queens():
    b = Board()
    acc = Unused.from_board(b)

    res = []

    def run(acc: Unused, cur: RC):
        r, c = cur

        if not acc.valid(cur):
            return

        acc = acc.remove(cur)

        if len(acc.used) == 8:
            res.append(acc)

        for c in acc.cols:
            run(acc, (r + 1, c))

    for c in range(8):
        run(acc, (0, c))
    used = [r.used for r in res]
    print(len(used))
    for u in used:
        b = Board()
        for rc in u:
            b[rc] = 'Q'
        print(b)
        print(20 * '===')


def __main():
    return eight_queens()
    b = Board(8)
    print(b.items())
    print(10 * '=')
    for r, row in enumerate(b):
        for c, _ in enumerate(row):
            b[r, c] = r + c
    for r in b:
        print(r)
    pass


if __name__ == '__main__':
    __main()
