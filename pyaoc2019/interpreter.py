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
# PROGRAM
# ======================================================================================================================

class Program(List[int]):
    """represent the working program, with instructions and registers, etc"""
    _output_register = None

    def __init__(self, *args, inputs: Optional[Iterable[int]] = None, suppress_output=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.pc = 0  # program counter
        self.relative_base = 0
        if debug:
            print(inputs)
        self.inputs = inputs
        self.suppress_output = suppress_output

    @property
    def output_register(self):
        return self._output_register

    @output_register.setter
    def output_register(self, val):
        if not self.suppress_output:
            print(f'OUT: {val}')
        Program._output_register = val

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, val):
        self._inputs = iter(val or [])

    def read(self, *vals) -> Union[int, Iterable[int]]:
        res = (self[v] for v in vals)
        if len(vals) == 1:
            res = next(res)
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
            inst = oc.inst_info.inst(oc)
            inst.run()
            if inst.opcode.code == 4:
                yield self.output_register

    def get_idx(self, param_mode, idx) -> int:
        """return idx based on param mode"""
        if param_mode == 0:
            # positional mode - value at idx represents ultimate idx
            return self[idx]
        if param_mode == 1:
            # immediate mode - value at idx represents the value to use
            return idx
        if param_mode == 2:
            # relative mode - idx is offset by relative_base
            return self[idx] + self.relative_base
        raise ValueError(f'invalid param mode: {param_mode}')


# ======================================================================================================================
# INSTRUCTION METADATA
# ======================================================================================================================

class InstructionInfo(NamedTuple):
    """store information about a single instruction type"""
    meta: str
    inst: Callable[[Opcode], InstructionBase]
    arity: int


@dataclass
class Opcode:
    code: int
    addresses: Tuple[int]
    program: Program
    inst_info: InstructionInfo

    @classmethod
    def from_program(cls, program: Program):
        code = program.cur
        idx = program.pc

        int_code = code % 100
        str_code = f'{code:05d}'
        if debug:
            print('idx, code:', idx, code)
        inst_info = opcodes[int_code]

        param_modes = take(inst_info.arity, map(int, reversed(str_code[:-2])))
        addresses = tuple(map(program.get_idx, param_modes, count(idx + 1)))

        return cls(int_code, addresses, program, inst_info)

    def standard_adjust_pc(self):
        self.program.pc += self.inst_info.arity + 1


# ======================================================================================================================
# INDIVIDUAL INSTRUCTIONS
# ======================================================================================================================

def _inc_pc(func):
    """automatically implement pc based on function arity"""

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
        """implement logic in subclasses for each instruction"""

    @property
    def prog(self):
        """convenience property"""
        return self.opcode.program


class InstCalcAndWrite(InstructionBase):
    """reduce an operator on n-args and write out the result"""

    def __init__(self, opcode: Opcode, op: Callable[[int, ...], int]):
        super().__init__(opcode)
        self.op = op

    @_inc_pc
    def run(self):
        *addresses, out = self.opcode.addresses
        self.prog.write(out, reduce(self.op, self.prog.read(*addresses)))


class InstInput(InstructionBase):
    """read in input from input stream and write out"""

    @_inc_pc
    def run(self):
        self.prog.write(first(self.opcode.addresses), next(self.prog.inputs))


class InstOutput(InstructionBase):
    """write value to output_register"""

    @_inc_pc
    def run(self):
        self.prog.output_register = self.prog.read(first(self.opcode.addresses))


class InstJump(InstructionBase):
    """change pc depending on predicate"""

    def __init__(self, opcode: Opcode, predicate: Callable[[int], bool]):
        super().__init__(opcode)
        self.predicate = predicate

    def run(self):
        test, new_idx = self.prog.read(*self.opcode.addresses)
        if self.predicate(test):
            self.prog.pc = new_idx
        else:
            self.opcode.standard_adjust_pc()


class InstRelativeBase(InstructionBase):
    """adjust the relative base"""

    @_inc_pc
    def run(self):
        self.prog.relative_base += self.prog.read(*self.opcode.addresses)


opcodes: Dict[int, InstructionInfo] = {
    1: InstructionInfo('add', lambda oc: InstCalcAndWrite(oc, add), 3),
    2: InstructionInfo('mul', lambda oc: InstCalcAndWrite(oc, mul), 3),
    3: InstructionInfo('read-in', InstInput, 1),
    4: InstructionInfo('write-out', InstOutput, 1),
    5: InstructionInfo('jump-if-true', lambda oc: InstJump(oc, bool), 2),
    6: InstructionInfo('jump-if-false', lambda oc: InstJump(oc, lambda v: not v), 2),
    7: InstructionInfo('less-than', lambda oc: InstCalcAndWrite(oc, comp(int, lt)), 3),
    8: InstructionInfo('equals', lambda oc: InstCalcAndWrite(oc, comp(int, eq)), 3),
    9: InstructionInfo('relative-base', InstRelativeBase, 1),
}


# ======================================================================================================================


def process(program: Program):
    yield from program.execute()


def process_no_yield(program: Program):
    U.exhaust(process(program))
    return program


def __main():
    pass


if __name__ == '__main__':
    __main()
