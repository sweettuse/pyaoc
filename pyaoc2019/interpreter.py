from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps, reduce
from itertools import count, chain
from operator import add, mul, lt, eq
from typing import NamedTuple, Callable, Tuple, List, Dict, Optional, Union, Iterable

from cytoolz import first, comp, take

import pyaoc2019.utils as U

__author__ = 'acushner'

debug = False


# ======================================================================================================================
# HELPER FUNCTIONS
# ======================================================================================================================

def parse_data(data: str, inputs=None):
    res = Program(chain(map(int, data.split(',')), 2000 * [0]), inputs=inputs)
    if debug:
        print(res)
    return res


def parse_file(name, inputs=None):
    data = U.read_file(name).copy()
    return parse_data(first(data), inputs)


# ======================================================================================================================
# SUPPORTING CLASSES
# ======================================================================================================================

class Program(List[int]):
    """represent the working program, with instructions and registers, etc"""
    _output_register = None

    def __init__(self, *args, inputs: Optional[Iterable[int]] = None, suppress_output=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.pc = 0
        self.relative_base = 0
        if debug:
            print(inputs)
        self.inputs = iter(inputs or [])
        self.suppress_output = suppress_output

    @property
    def output_register(self):
        return self._output_register

    @output_register.setter
    def output_register(self, val):
        if not self.suppress_output:
            print(f'OUT: {val}')
        Program._output_register = val

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

    def execute(self):
        while self.valid:
            oc = Opcode.from_program(self)
            yield oc.fi.inst(oc)


class InstructionInfo(NamedTuple):
    """store information about a single instruction type"""
    meta: str
    inst: Callable[[Opcode], InstructionBase]
    arity: int


def _get_idx(param_mode, idx, program: Program) -> int:
    """return idx based on param mode"""
    if param_mode == 0:
        # positional mode - value at idx represents ultimate idx
        return program[idx]
    if param_mode == 1:
        # immediate mode - value at idx represents the value to use
        return idx
    if param_mode == 2:
        # relative mode - idx is offset by relative_base
        return program[idx] + program.relative_base
    raise ValueError(f'invalid param mode: {param_mode}')


@dataclass
class Opcode(ABC):
    code: int
    addresses: Tuple[int]
    program: Program
    fi: InstructionInfo

    @classmethod
    def from_program(cls, program: Program):
        code = program.cur
        idx = program.pc
        int_code = code % 100
        str_code = f'{code:05d}'
        if debug:
            print('idx, code:', idx, code)
        fi = opcodes[int_code]

        addresses = tuple(_get_idx(m, v, program) for (m, v) in
                          take(fi.arity, zip(map(int, reversed(str_code[:-2])), count(idx + 1))))

        return cls(int_code, addresses, program, fi)

    def standard_adjust_pc(self):
        self.program.pc += self.fi.arity + 1


# ======================================================================================================================
# INDIVIDUAL PROGRAM
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
    """base class for an individual instruction"""

    def __init__(self, opcode: Opcode):
        self.opcode = opcode

    @abstractmethod
    def run(self):
        """logic of each instruction should be implemented here in subclasses"""

    @property
    def insts(self):
        """convenience property"""
        return self.opcode.program


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


opcodes: Dict[int, InstructionInfo] = {
    1: InstructionInfo('add', lambda oc: RunAndWrite(oc, add), 3),
    2: InstructionInfo('mul', lambda oc: RunAndWrite(oc, mul), 3),
    3: InstructionInfo('read-in', ProcInput, 1),
    4: InstructionInfo('write-out', ProcOutput, 1),
    5: InstructionInfo('jump-if-true', lambda oc: Jump(oc, bool), 2),
    6: InstructionInfo('jump-if-false', lambda oc: Jump(oc, lambda v: not v), 2),
    7: InstructionInfo('less-than', lambda oc: RunAndWrite(oc, comp(int, lt)), 3),
    8: InstructionInfo('equals', lambda oc: RunAndWrite(oc, comp(int, eq)), 3),
    9: InstructionInfo('relative-base', RelativeBase, 1),
}


# ======================================================================================================================


def process(program: Program):
    for inst in program.execute():
        inst.run()
        if inst.opcode.code == 4:
            yield program.output_register


def process_no_yield(program: Program):
    U.exhaust(process(program))
    return program


def __main():
    pass


if __name__ == '__main__':
    __main()
