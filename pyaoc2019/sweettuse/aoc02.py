from __future__ import annotations
from functools import partial, wraps
from itertools import product
from operator import add, mul
from rich import print
import inspect

from pyaoc2019.utils import read_file


class Intcode:
    def __init__(
        self,
        memory: str,
        overrides: dict[int, int] | None = None,
    ):
        self.mem = self._parse_instructions(memory, overrides)
        self.pc = 0

    @staticmethod
    def _parse_instructions(memory, overrides) -> list[int]:
        res = [int(v) for v in memory.split(',')]
        if overrides:
            for idx, v in overrides.items():
                res[idx] = v
        return res

    def get(self, address) -> int:
        """get value at address"""
        return self.mem[address]

    def execute(self):
        while (code := self.mem[self.pc]) != 99:
            cmd = add if code == 1 else mul

            self.mem[self.get(self.pc + 3)] = cmd(
                *map(self.get, self.mem[self.pc + 1 : self.pc + 3])
            )
            self.pc += 4

    def pretty(self) -> None:
        print(self.mem)


def validate():
    cases = [
        '1,0,0,0,99 becomes 2,0,0,0,99',
        '2,3,0,3,99 becomes 2,3,0,6,99',
        '2,4,4,5,99,0 becomes 2,4,4,5,99,9801',
        '1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99',
    ]

    def _test(s: str):
        input, _, output = s.split()
        ic = Intcode(input)
        ic.execute()
        assert ic.mem == list(map(int, output.split(','))), ic.mem

    for c in cases:
        _test(c)
    print('success')


DATA = read_file(2)[0]


def part1():
    # return validate()
    ic = Intcode(DATA, {1: 12, 2: 2})
    ic.execute()
    print(ic.get(0))


def part2():
    target = 19690720
    for noun, verb in product(range(0, 100), repeat=2):
        ic = Intcode(DATA, {1: noun, 2: verb})
        ic.execute()
        if ic.get(0) == target:
            print(100 * noun + verb)
            return


part1()
part2()


def __main():
    pass
