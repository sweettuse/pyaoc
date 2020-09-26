from collections import defaultdict
from typing import List

from pyaoc2017.aoc18 import Program, Command

__author__ = 'acushner'

from pyaoc2019.utils import read_file


class Program23(Program):
    def __init__(self, commands: List[Command], **overrides):
        super().__init__(commands)
        self._regs = dict.fromkeys('abcdefgh', 0)
        self._regs.update(overrides)
        self.mul_count = 0

    def sub(self, x, y):
        self[x] -= self[y]

    def mul(self, x, y):
        self.mul_count += 1
        return super().mul(x, y)

    def jnz(self, x, y):
        if self[x]:
            self._pc += self[y] - 1


def parse_data():
    return [Command.from_str(s) for s in read_file(23, 2017)]


def part1():
    p = Program23(parse_data())
    p.run()
    return p.mul_count


def part2():
    b = c = 93
    h = 0
    a = 1
    b *= 100
    b += 100000
    c = b
    c += 17000
    while True:
        f = 1
        d = 2
        while True:
            e = 2
            while True:
                g = d
                g *= e
                g -= b
                if not g:
                    f = 0
                e += 1
                g = e
                g -= b
                if not g:
                    break
            d += 1
            g = d
            g -= b
            if not g:
                break

        if not f:
            h += 1
        g = b
        g -= c
        if not g:
            return h
        b += 17


def part2_2():
    total = 0
    for b in range(109300, 126301, 17):
        for i in range(2, b // 2):
            if not b % i:
                total += 1
                break
    return total


def __main():
    print(part1())
    print(part2_2())


if __name__ == '__main__':
    __main()
