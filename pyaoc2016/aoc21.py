from __future__ import annotations
from collections import deque
from itertools import permutations
from typing import Iterable
from pyaoc2019.utils import read_file, timer
from rich import print

DATA = read_file(21, 2016)

class Scrambler:
    def __init__(self, s: Iterable[str]):
        self.d = deque(s)
    
    def swap_pos(self, x: int, y: int):
        self.d[x], self.d[y] = self.d[y], self.d[x]

    def swap_letter(self, x: str, y: str):
        self.swap_pos(self.d.index(x), self.d.index(y))
    
    def rotate_n(self, n: int, direction: str):
        if direction == 'left':
            n = -n
        self.d.rotate(n)
    
    def rotate_by_letter_pos(self, x: str):
        idx = self.d.index(x)
        self.d.rotate(1 + idx + (idx >= 4) * 1)

    def reverse_positions(self, x: int, y: int):
        # x_idx, y_idx = self.d.index(x), self.d.index(y)
        x_idx, y_idx = x, y
        while x_idx < y_idx:
            self.swap_pos(x_idx, y_idx)
            x_idx += 1
            y_idx -= 1
    
    def move_pos(self, x: int, y: int):
        char = self.d[x]
        del self.d[x]
        self.d.insert(y, char)

    def __repr__(self):
        return f'{type(self).__name__}({self.d})'
    
    def __str__(self):
        return ''.join(self.d)
    
    def _execute(self, s: str):
        match s.split():
            case ['rotate', 'based', *_, letter]:
                self.rotate_by_letter_pos(letter)
            case ['rotate', direction, num, _]:
                self.rotate_n(int(num), direction)
            case ['swap', 'letter', x, *_, y]:
                self.swap_letter(x, y)
            case ['swap', 'position', x, *_, y]:
                self.swap_pos(int(x), int(y))
            case ['move', 'position', x, *_, y]:
                self.move_pos(int(x), int(y))
            case ['reverse', _, x, _ , y]:
                self.reverse_positions(int(x), int(y))
            case fail:
                raise ValueError(fail)

    def run(self, data):
        for inst in data:
            self._execute(inst)

def test():
    def _test(_, res):
        assert str(s) == res, (str(s), res)

    s = Scrambler('abcde')
    _test(s.swap_pos(4, 0), 'ebcda')
    _test(s.swap_letter('d', 'b'), 'edcba')
    _test(s.reverse_positions(0, 4), 'abcde')
    _test(s.rotate_n(1, 'left'), 'bcdea')
    _test(s.move_pos(1, 4), 'bdeac')
    _test(s.move_pos(3, 0), 'abdec')
    _test(s.rotate_by_letter_pos('b'), 'ecabd')
    _test(s.rotate_by_letter_pos('d'), 'decab')


def part1() -> str:
    s = Scrambler('abcdefgh')
    s.run(DATA)
    return str(s)

@timer
def part2() -> str:
    target = 'fbgdceah'
    for pos in permutations('abcdefgh'):
        s = Scrambler(pos)
        s.run(DATA)
        if str(s) == target:
            return ''.join(pos)
    raise Exception

def __main():
    test()
    print(part1())
    print(part2())


__main()
    