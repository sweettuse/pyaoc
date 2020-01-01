from functools import partial
from typing import NamedTuple, Callable, List, Dict
import operator as op

from cytoolz import memoize

import pyaoc2019.utils as U
from more_itertools import first

__author__ = 'acushner'


class FuncInfo(NamedTuple):
    meta: str
    func: Callable
    arity: int


def oc_run_and_write(f, instructions: List[int], *args):
    a, b, out_idx = args
    instructions[out_idx] = f(instructions[a], instructions[b])


def parse_opcode(code: int):
    return code


opcodes: Dict[int, FuncInfo] = {
    1: FuncInfo('add', partial(oc_run_and_write, op.add), 3),
    2: FuncInfo('mul', partial(oc_run_and_write, op.mul), 3),
}


def parse_data(data: str):
    return list(map(int, data.split(',')))


@memoize
def parse_file(name):
    return parse_data(first(U.read_file(name)))


def process(instructions):
    pc = 0
    while pc < len(instructions) and instructions[pc] != 99:
        opcode = parse_opcode(instructions[pc])
        pc += 1
        fi = opcodes[opcode]
        fi.func(instructions, *instructions[pc: pc + fi.arity])
        pc += fi.arity
    return instructions


def aoc2(p1, p2):
    data = parse_file('02').copy()
    data[1:3] = p1, p2
    return first(process(data))


def aoc2_b(target):
    return first(p1 * 100 + p2 for p1 in range(100) for p2 in range(100) if aoc2(p1, p2) == target)


def __main():
    test_data = '1,9,10,3,2,3,11,0,99,30,40,50'
    # print(first(process(parse_data(test_data))))
    print(aoc2(12, 2))
    print(aoc2_b(19690720))


if __name__ == '__main__':
    __main()
