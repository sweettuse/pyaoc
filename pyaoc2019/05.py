import operator as op
from functools import partial
from itertools import count
from typing import NamedTuple, Callable, List, Dict, Tuple, Optional

from cytoolz import memoize, first

import pyaoc2019.utils as U

__author__ = 'acushner'


class FuncInfo(NamedTuple):
    meta: str
    func: Callable
    arity: int
    final_always_immediate: bool = True


class Opcode(NamedTuple):
    code: int
    param_modes: Tuple[int]
    fi: FuncInfo

    @classmethod
    def from_code(cls, code: int):
        int_code = code % 100
        str_code = f'{code:05d}'

        fi = opcodes[int_code]
        param_modes = [v for (v, _) in zip(map(int, reversed(str_code[:3])), range(fi.arity))]
        if fi.final_always_immediate:
            param_modes[-1] = 1

        return cls(int_code, tuple(param_modes), fi)

    def get_args(self, program, start_idx):
        gi = program.__getitem__
        return [gi(idx) if pm else gi(gi(idx)) for (idx, pm) in zip(count(start_idx), self.param_modes)]


def oc_run_and_write(f, program: List[int], *args):
    a, b, out_idx = args
    program[out_idx] = f(a, b)


def oc_input(program, out_idx, inputs):
    program[out_idx] = inputs


def oc_output(program, idx):
    print('out', idx)


def oc_jump(f, program, pc, test, out):
    return out if f(test) else pc + 2


def oc_comp(f):
    return lambda *args: int(f(*args))


opcodes: Dict[int, FuncInfo] = {
    1: FuncInfo('add', partial(oc_run_and_write, op.add), 3),
    2: FuncInfo('mul', partial(oc_run_and_write, op.mul), 3),
    3: FuncInfo('input', oc_input, 1),
    4: FuncInfo('output', oc_output, 1, False),
    5: FuncInfo('jump-if-true', partial(oc_jump, bool), 2, False),
    6: FuncInfo('jump-if-false', partial(oc_jump, lambda v: not v), 2, False),
    7: FuncInfo('less than', partial(oc_run_and_write, oc_comp(op.lt)), 3),
    8: FuncInfo('equals', partial(oc_run_and_write, oc_comp(op.eq)), 3),
}


def parse_data(data: str):
    return list(map(int, data.split(',')))


@memoize
def parse_file(name):
    return parse_data(first(U.read_file(name)))


def process(program, inputs: Optional[List[int]] = None):
    inputs = inputs or []
    pc = 0
    while pc < len(program) and program[pc] != 99:
        opcode = Opcode.from_code(program[pc])
        fi = opcode.fi
        pc += 1
        args = opcode.get_args(program, pc)
        inc_pc = True
        if opcode.code == 3:
            cur, *inputs = inputs
            fi.func(program, *args, cur)
        elif opcode.code in {5, 6}:
            pc = fi.func(program, pc, *args)
            inc_pc = False
        else:
            fi.func(program, *args)
        pc += inc_pc * fi.arity
    return program


def aoc5(inp):
    program = parse_file('05').copy()
    process(program, [inp])


def __main():
    aoc5(1)
    aoc5(5)


if __name__ == '__main__':
    __main()
