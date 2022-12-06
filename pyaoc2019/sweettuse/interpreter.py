from __future__ import annotations
from functools import partial, wraps
from itertools import product
from operator import add, mul
from typing import Callable, NamedTuple
from rich import print
import inspect

from pyaoc2019.utils import read_file


func_map: dict[int, Callable] = {}


def register(fn=None, *, opcode: int, output: bool = True):
    if not fn:
        return partial(register, opcode=opcode, output=output)

    @wraps(fn)
    def wrapper(self: Intcode, *a):
        res = fn(self, *map(self.get, self.mem[self.pc + 1 : self.pc + 3]))
        self.mem[self.get(self.pc + 3)] = res
        self.pc += arity + 1

    wrapper = wraps(fn)(wrapper)
    func_map[opcode] = wrapper
    return wrapper


class OpcodeInfo(NamedTuple):
    code: int
    arity: int



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
        while (opcode := self.mem[self.pc]) != 99:
            func_map[opcode](self)

    def _parse_opcode(self, addr: int | None = None) -> Iterable[int]:
        code = self.get(addr or self.pc)
        modes, code = divmod(code, 100)
        code_str = str(code).zfill(8)

        
        pass

    @register(opcode=1, output=True)
    def add(self, a, b):
        return a + b

    @register(opcode=2, output=True)
    def mul(self, a, b):
        return a * b

    def output(self, value):
        print(value)

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

validate()

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
