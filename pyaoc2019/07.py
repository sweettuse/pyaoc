import operator as op
from functools import partial
from itertools import count, permutations, repeat
from typing import NamedTuple, Callable, List, Dict, Tuple

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

    def get_args(self, instructions, start_idx):
        gi = instructions.__getitem__
        return [gi(idx) if pm else gi(gi(idx)) for (idx, pm) in zip(count(start_idx), self.param_modes)]


def oc_run_and_write(f, instructions: List[int], *args):
    a, b, out_idx = args
    instructions[out_idx] = f(a, b)


def oc_input(instructions, out_idx, input):
    instructions[out_idx] = input


output_register = U.Atom()


def oc_output(_, value):
    output_register.value = value


def oc_jump(f, _, pc, test, out):
    return out if f(test) else pc + 2


def oc_comp(f: Callable):
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


# ======================================================================================================================


def process(instructions, init_input: int):
    """process as a generator so it keeps amps' states"""
    inputs = input_stream(init_input)
    pc = 0
    while pc < len(instructions) and instructions[pc] != 99:
        opcode = Opcode.from_code(instructions[pc])
        pc += 1
        args = opcode.get_args(instructions, pc)
        fi = opcode.fi
        inc_pc = True
        if opcode.code == 3:
            fi.func(instructions, *args, next(inputs))
        elif opcode.code in {5, 6}:
            pc = fi.func(instructions, pc, *args)
            inc_pc = False
        else:
            fi.func(instructions, *args)
            if opcode.code == 4:
                yield True

        pc += inc_pc * fi.arity
    yield False


def feedback(amps, instructions, inputs):
    output_register.value = 0
    amp_map = {}
    inputs = iter(inputs)
    endless_amps = (a for amps in repeat(amps) for a in amps)
    for a in endless_amps:
        try:
            proc = amp_map[a]
        except KeyError:
            proc = amp_map[a] = process(instructions.copy(), next(inputs))
        if not next(proc) and a == 'E':
            break
    yield output_register.value


def input_stream(i):
    yield i
    while True:
        yield output_register.value


def process_perm(instructions, inputs: List[int]):
    return next(feedback("ABCDE", instructions, inputs))


def aoc7(filename, input_str):
    instructions = parse_file(filename)
    return max(process_perm(instructions, perm) for perm in permutations(map(int, input_str)))


def __main():
    print(aoc7('07', '01234'))
    print(aoc7('07', '56789'))


if __name__ == '__main__':
    __main()
