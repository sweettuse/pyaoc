import operator as op
from functools import partial
from itertools import count
from typing import NamedTuple, Callable, List, Dict, Tuple, Optional

from cytoolz import memoize, first

import utils as U

__author__ = 'acushner'

relative_base = U.Atom(0)


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

    @staticmethod
    def _arg_helper(instructions, idx, param_mode):
        if param_mode == 0:
            idx = instructions[idx]
        elif param_mode == 1:
            pass
        elif param_mode == 2:
            idx += relative_base.value
        else:
            raise ValueError(f'invalid param mode! {param_mode}')
        return instructions[idx]

    def get_args(self, instructions, start_idx):
        return [self._arg_helper(instructions, idx, pm) for (idx, pm) in zip(count(start_idx), self.param_modes)]


def oc_run_and_write(f, instructions: List[int], *args):
    a, b, out_idx = args
    instructions[out_idx] = f(a, b)


def oc_input(instructions, out_idx, inputs):
    instructions[out_idx] = inputs


def oc_output(_, idx):
    print('out', idx)


def oc_jump(f, _, pc, test, out):
    return out if f(test) else pc + 2


def oc_comp(f):
    return lambda *args: int(f(*args))


def oc_base(_, arg):
    relative_base.value += arg
    # print(f'rb: {relative_base.value}')


opcodes: Dict[int, FuncInfo] = {
    1: FuncInfo('add', partial(oc_run_and_write, op.add), 3),
    2: FuncInfo('mul', partial(oc_run_and_write, op.mul), 3),
    3: FuncInfo('input', oc_input, 1),
    4: FuncInfo('output', oc_output, 1, False),
    5: FuncInfo('jump-if-true', partial(oc_jump, bool), 2, False),
    6: FuncInfo('jump-if-false', partial(oc_jump, lambda v: not v), 2, False),
    7: FuncInfo('less than', partial(oc_run_and_write, oc_comp(op.lt)), 3),
    8: FuncInfo('equals', partial(oc_run_and_write, oc_comp(op.eq)), 3),
    9: FuncInfo('relative-base', oc_base, 1)
}


def parse_data(data: str):
    return list(map(int, data.split(',')))


@memoize
def parse_file(name):
    return parse_data(first(U.read_file(name)))


def process(instructions, inputs: Optional[List[int]] = None):
    instructions = _extend_instructions(instructions)
    relative_base.value = 0
    inputs = inputs or []
    pc = 0
    while pc < len(instructions) and instructions[pc] != 99:
        opcode = Opcode.from_code(instructions[pc])
        fi = opcode.fi
        pc += 1
        args = opcode.get_args(instructions, pc)
        inc_pc = True
        # print(opcode)
        if opcode.code == 3:
            cur, *inputs = inputs
            fi.func(instructions, *args, cur)
        elif opcode.code in {5, 6}:
            pc = fi.func(instructions, pc, *args)
            inc_pc = False
        else:
            fi.func(instructions, *args)
        pc += inc_pc * fi.arity
    return instructions


def _extend_instructions(instructions):
    insts = instructions.copy()
    insts.extend(200 * [0])
    return insts


def aoc9(inp):
    instructions = parse_file('09')
    process(instructions, [inp])


def __main():
    test_data = parse_data('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')
    test_data = parse_data('1102,34915192,34915192,7,4,7,99,0')
    # print(process(test_data))
    aoc9(1)


if __name__ == '__main__':
    __main()
