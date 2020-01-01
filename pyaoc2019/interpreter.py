from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps, reduce
from itertools import count
from operator import add, mul, lt, eq
from typing import NamedTuple, Callable, Tuple, List, Dict, Optional, Union, Iterable

from cytoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'

debug = False


def parse_data(data: str, inputs=None):
    res = Instructions(map(int, data.split(',')), inputs=inputs)
    if debug:
        print(res)
    return res


def parse_file(name, inputs=None):
    data = U.read_file(name).copy()
    return parse_data(first(data), inputs)


# ======================================================================================================================

class Instructions(List[int]):
    def __init__(self, *args, inputs: Optional[List[int]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pc = 0
        self._output_register = None
        self.relative_base = 0
        if debug:
            print(inputs)
        self.inputs = iter(inputs or [])

    @property
    def output_register(self):
        return self._output_register

    @output_register.setter
    def output_register(self, val):
        print(f'OUT: {val}')
        self._output_register = val

    def read(self, *vals) -> Union[int, Iterable[int]]:
        res = (self[v] for v in vals)
        if len(vals) == 1:
            return next(res)
        return res

    def write(self, idx, v):
        self[idx] = v

    @property
    def valid(self):
        return self.pc < len(self) and self.cur != 99

    @property
    def cur(self):
        return self[self.pc]


class FuncInfo(NamedTuple):
    meta: str
    func: Callable[[Opcode], InstructionBase]
    arity: int


def _get_idx(mode, idx, instructions: Instructions) -> int:
    """return idx to be processed"""
    if mode == 0:
        # positional mode - value at idx represents ultimate idx
        return instructions[idx]
    if mode == 1:
        # immediate mode - value at idx represents is the value to use
        return idx
    if mode == 2:
        # relative mode - idx is offset by relative_base
        return instructions[idx] + instructions.relative_base
    raise ValueError(f'invalid param mode: {mode}')


@dataclass
class Opcode(ABC):
    code: int
    addresses: Tuple[int]
    instructions: Instructions
    idx: int
    fi: FuncInfo

    @classmethod
    def from_instructions(cls, instructions: Instructions):
        code = instructions.cur
        idx = instructions.pc
        int_code = code % 100
        str_code = f'{code:05d}'
        if debug:
            print('idx, code:', idx, code)
        fi = opcodes[int_code]

        addresses = tuple(_get_idx(m, v, instructions) for (m, v, _) in
                          zip(map(int, reversed(str_code[:3])), count(idx + 1), range(fi.arity)))

        return cls(int_code, addresses, instructions, idx, fi)


def adjust_pc(func):
    @wraps(func)
    def wrapper(self: InstructionBase, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            self.standard_adjust_pc()

    return wrapper


# ======================================================================================================================


class InstructionBase(ABC):
    def __init__(self, opcode: Opcode):
        self.opcode = opcode

    @abstractmethod
    def run(self, *args, **kwargs):
        """each subclass could have different args"""

    @property
    def insts(self):
        return self.opcode.instructions

    def standard_adjust_pc(self):
        self.opcode.instructions.pc += self.opcode.fi.arity + 1


class RunAndWrite(InstructionBase):
    def __init__(self, opcode: Opcode, op: Callable):
        super().__init__(opcode)
        self.op = op

    @adjust_pc
    def run(self):
        *args, out_idx = self.opcode.addresses
        self.insts.write(out_idx, reduce(self.op, self.insts.read(*args)))


class ProcInput(InstructionBase):
    @adjust_pc
    def run(self):
        self.insts.write(*self.opcode.addresses, next(self.insts.inputs))


class ProcOutput(InstructionBase):
    @adjust_pc
    def run(self):
        self.insts.output_register = self.insts.read(*self.opcode.addresses)


class Jump(InstructionBase):
    def __init__(self, opcode: Opcode, predicate: Callable[[int], bool]):
        super().__init__(opcode)
        self.predicate = predicate

    def run(self):
        test, new_idx = self.insts.read(*self.opcode.addresses)
        if self.predicate(test):
            self.insts.pc = new_idx
        else:
            self.standard_adjust_pc()


class Comp(InstructionBase):
    def __init__(self, opcode: Opcode, comp: Callable[[int, int], bool]):
        super().__init__(opcode)
        self.comp = comp

    @adjust_pc
    def run(self):
        *idxs, out = self.opcode.addresses
        self.insts.write(out, int(self.comp(*self.insts.read(*idxs))))


opcodes: Dict[int, FuncInfo] = {
    1: FuncInfo('add', lambda oc: RunAndWrite(oc, add), 3),
    2: FuncInfo('mul', lambda oc: RunAndWrite(oc, mul), 3),
    3: FuncInfo('read-in', ProcInput, 1),
    4: FuncInfo('write-out', ProcOutput, 1),
    5: FuncInfo('jump-if-true', lambda oc: Jump(oc, bool), 2),
    6: FuncInfo('jump-if-false', lambda oc: Jump(oc, lambda v: not v), 2),
    7: FuncInfo('less-than', lambda oc: Comp(oc, lt), 3),
    8: FuncInfo('equals', lambda oc: Comp(oc, eq), 3),
}


# ======================================================================================================================


def parse_instruction(instructions: Instructions) -> InstructionBase:
    oc = Opcode.from_instructions(instructions)
    return oc.fi.func(oc)


def process(instructions: Instructions):
    while instructions.valid:
        inst = parse_instruction(instructions)
        inst.run()

    return instructions


def aoc2(p1, p2):
    data = parse_file('02')
    data[1:3] = p1, p2
    return first(process(data))


def aoc2_b(target):
    return first(p1 * 100 + p2 for p1 in range(100) for p2 in range(100) if aoc2(p1, p2) == target)


def aoc5(inp):
    return process(parse_file(5, [inp]))


def __main():
    # test_data = parse_data('1,9,10,3,2,3,11,0,99,30,40,50')
    # print(process(test_data))
    # print(aoc2(53, 35))
    # print(aoc2(12, 2))
    # print(process(parse_data('1002,4,3,4,33')))
    # print(process(parse_data('1101,100,-1,4,0')))
    # aoc5(1)
    process(parse_data('3,9,8,9,10,9,4,9,99,-1,8', [2]))


if __name__ == '__main__':
    __main()
