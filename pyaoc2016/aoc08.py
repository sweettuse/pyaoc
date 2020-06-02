__author__ = 'acushner'

from collections import deque
from typing import List

from pyaoc2019.utils import exhaust, read_file

ON = '#'
OFF = ' '

WIDTH = 50
HEIGHT = 6


class Display:
    def __init__(self):
        self.disp = [[OFF] * WIDTH for _ in range(HEIGHT)]

    def rect(self, c_end, r_end):
        """create rectangle from UL `c_end` wide and `r_end` tall"""
        for r in range(r_end):
            for c in range(c_end):
                self.disp[r][c] = ON

    @property
    def num_on(self):
        return sum(self.disp[r][c] == ON for c in range(WIDTH) for r in range(HEIGHT))

    @staticmethod
    def _rotate(idx, n, board):
        r = deque(board[idx])
        r.rotate(n)
        board[idx] = list(r)
        return board

    def rot_row(self, row, n):
        """rotate row `row` right by `n` pixels"""
        self.disp = self._rotate(row, n, self.disp)

    def rot_col(self, col, n):
        """rotate column `col` down by `n` pixels"""
        cols = list(map(list, zip(*self.disp)))
        cols = self._rotate(col, n, cols)
        self.disp = list(map(list, zip(*cols)))

    def show(self):
        print(WIDTH * '=')
        for r in self.disp:
            print(''.join(map(str, r)))
        print(WIDTH * '=')

    def _parse_inst(self, s: str):
        if s.startswith('rect'):
            return self.rect(*map(int, s.split()[-1].split('x')))
        _, rc, idx, _, n = s.split()
        idx = int(idx.split('=')[-1])
        eval(f'self.rot_{rc[:3]}({idx}, {n})')

    def parse_instructions(self, insts: List[str]):
        exhaust(map(self._parse_inst, insts))


def __main():
    instructions = read_file(8, 2016)
    d = Display()
    d.parse_instructions(instructions)
    print(d.num_on)
    d.show()


if __name__ == '__main__':
    __main()
