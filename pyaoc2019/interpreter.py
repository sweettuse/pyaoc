from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps, reduce
from itertools import count, chain
from operator import add, mul, lt, eq
from typing import NamedTuple, Callable, Tuple, List, Dict, Optional, Union, Iterable

from cytoolz import first, comp

import pyaoc2019.utils as U

__author__ = 'acushner'

debug = False


# ======================================================================================================================
# HELPER FUNCTIONS
# ======================================================================================================================

def parse_data(data: str, inputs=None):
    res = Instructions(chain(map(int, data.split(',')), 2000 * [0]), inputs=inputs)
    if debug:
        print(res)
    return res


def parse_file(name, inputs=None):
    data = U.read_file(name).copy()
    return parse_data(first(data), inputs)


# ======================================================================================================================
# SUPPORTING CLASSES
# ======================================================================================================================

class Instructions(List[int]):
    _output_register = None

    def __init__(self, *args, inputs: Optional[List[int]] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.pc = 0
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
        Instructions._output_register = val

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
        # immediate mode - value at idx represents the value to use
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

        return cls(int_code, addresses, instructions, fi)

    def standard_adjust_pc(self):
        self.instructions.pc += self.fi.arity + 1


# ======================================================================================================================
# INDIVIDUAL INSTRUCTIONS
# ======================================================================================================================

def _adjust_pc(func):
    @wraps(func)
    def wrapper(self: InstructionBase, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        finally:
            self.opcode.standard_adjust_pc()

    return wrapper


class InstructionBase(ABC):
    def __init__(self, opcode: Opcode):
        self.opcode = opcode

    @abstractmethod
    def run(self):
        """logic of each instruction should be implemented here in subclasses"""

    @property
    def insts(self):
        return self.opcode.instructions


class RunAndWrite(InstructionBase):
    """reduce an operator on n-args and write out the result as an integer"""

    def __init__(self, opcode: Opcode, op: Callable[[int, ...], int]):
        super().__init__(opcode)
        self.op = op

    @_adjust_pc
    def run(self):
        *idxs, out = self.opcode.addresses
        self.insts.write(out, reduce(self.op, self.insts.read(*idxs)))


class ProcInput(InstructionBase):
    """read in input from input stream and write out"""

    @_adjust_pc
    def run(self):
        self.insts.write(*self.opcode.addresses, next(self.insts.inputs))


class ProcOutput(InstructionBase):
    """write value to output_register"""

    @_adjust_pc
    def run(self):
        self.insts.output_register = self.insts.read(*self.opcode.addresses)


class Jump(InstructionBase):
    """change pc depending on predicate"""

    def __init__(self, opcode: Opcode, predicate: Callable[[int], bool]):
        super().__init__(opcode)
        self.predicate = predicate

    def run(self):
        test, new_idx = self.insts.read(*self.opcode.addresses)
        if self.predicate(test):
            self.insts.pc = new_idx
        else:
            self.opcode.standard_adjust_pc()


class RelativeBase(InstructionBase):
    """adjust the relative base"""

    @_adjust_pc
    def run(self):
        self.insts.relative_base += self.insts.read(*self.opcode.addresses)


opcodes: Dict[int, FuncInfo] = {
    1: FuncInfo('add', lambda oc: RunAndWrite(oc, add), 3),
    2: FuncInfo('mul', lambda oc: RunAndWrite(oc, mul), 3),
    3: FuncInfo('read-in', ProcInput, 1),
    4: FuncInfo('write-out', ProcOutput, 1),
    5: FuncInfo('jump-if-true', lambda oc: Jump(oc, bool), 2),
    6: FuncInfo('jump-if-false', lambda oc: Jump(oc, lambda v: not v), 2),
    7: FuncInfo('less-than', lambda oc: RunAndWrite(oc, comp(int, lt)), 3),
    8: FuncInfo('equals', lambda oc: RunAndWrite(oc, comp(int, eq)), 3),
    9: FuncInfo('relative-base', RelativeBase, 1),
}


def parse_instruction(instructions: Instructions) -> InstructionBase:
    oc = Opcode.from_instructions(instructions)
    return oc.fi.func(oc)


# ======================================================================================================================


def process(instructions: Instructions):
    while instructions.valid:
        inst = parse_instruction(instructions)
        inst.run()

    return instructions


def __main():
    pass


if __name__ == '__main__':
    __main()
