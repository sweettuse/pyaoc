from functools import wraps
from typing import NamedTuple, List

from more_itertools import first

from pyaoc2019.utils import read_file, chunks, exhaust, timer

__author__ = 'acushner'


class Inst(NamedTuple):
    opcode: int
    a: int
    b: int
    output: int

    @classmethod
    def from_str(cls, s):
        op, *ins, out = map(int, s.split())
        return cls(op, *ins, out)


Regs = List[int]


class Debug(NamedTuple):
    before: Regs
    inst: Inst
    after: Regs

    @classmethod
    def from_strings(cls, lines: List[str]):
        before, inst, after, *_ = lines
        b = eval(before.split(maxsplit=1)[-1])
        a = eval(after.split(maxsplit=1)[-1])
        return cls(b, Inst.from_str(inst), a)


def _register_helper(func):
    name = func.__name__
    if name == 'set':
        Interpreter.add_func('seti')
        Interpreter.add_func('setr')
        return

    @wraps(func)
    def wrap_r(self, inst: Inst, regs: Regs):
        new_inst = Inst(inst.opcode, regs[inst.a], regs[inst.b], inst.output)
        return func(self, new_inst, regs.copy())

    @wraps(func)
    def wrap_i(self, inst: Inst, regs: Regs):
        new_inst = Inst(inst.opcode, regs[inst.a], inst.b, inst.output)
        return func(self, new_inst, regs.copy())

    if name in {'eq', 'gt'}:
        @wraps(func)
        def wrap_ir(self, inst: Inst, regs: Regs):
            new_inst = Inst(inst.opcode, inst.a, regs[inst.b], inst.output)
            return func(self, new_inst, regs.copy())

        Interpreter.add_func(f'{name}rr', wrap_r)
        Interpreter.add_func(f'{name}ri', wrap_i)
        Interpreter.add_func(f'{name}ir', wrap_ir)
    else:
        Interpreter.add_func(f'{name}r', wrap_r)
        Interpreter.add_func(f'{name}i', wrap_i)


def register(func):
    _registry.add(func)


_registry = set()


class Interpreter:
    func_names = set()

    @classmethod
    def add_func(cls, name, func=None):
        cls.func_names.add(name)
        if func:
            setattr(cls, name, func)

    @register
    def add(self, inst: Inst, regs: List[int]):
        regs[inst.output] = inst.a + inst.b
        return regs

    @register
    def mul(self, inst: Inst, regs: List[int]):
        regs[inst.output] = inst.a * inst.b
        return regs

    @register
    def ban(self, inst: Inst, regs: List[int]):
        regs[inst.output] = inst.a & inst.b
        return regs

    @register
    def bor(self, inst: Inst, regs: List[int]):
        regs[inst.output] = inst.a | inst.b
        return regs

    @register
    def set(self):
        """set functions implemented manually below"""

    def setr(self, inst: Inst, regs: List[int]):
        regs = regs.copy()
        regs[inst.output] = regs[inst.a]
        return regs

    def seti(self, inst: Inst, regs: List[int]):
        regs = regs.copy()
        regs[inst.output] = inst.a
        return regs

    @register
    def gt(self, inst: Inst, regs: List[int]):
        regs[inst.output] = int(inst.a > inst.b)
        return regs

    @register
    def eq(self, inst: Inst, regs: List[int]):
        regs[inst.output] = int(inst.a == inst.b)
        return regs


exhaust(_register_helper, _registry)


def test():
    i = Interpreter()
    regs = [1, 2, 3, 4]
    assert i.addr(Inst(2, 2, 3, 0), regs)[0] == 7
    assert i.addi(Inst(2, 2, 3, 0), regs)[0] == 6
    assert i.mulr(Inst(2, 2, 3, 0), regs)[0] == 12
    assert i.muli(Inst(2, 2, 3, 0), regs)[0] == 9
    assert i.banr(Inst(2, 2, 3, 0), regs)[0] == 0
    assert i.bani(Inst(2, 2, 3, 0), regs)[0] == 3
    assert i.borr(Inst(2, 2, 3, 0), regs)[0] == 7
    assert i.bori(Inst(2, 2, 3, 0), regs)[0] == 3
    assert i.setr(Inst(2, 2, 3, 0), regs)[0] == 3
    assert i.seti(Inst(2, 2, 3, 0), regs)[0] == 2


def parse_test_data():
    return [Debug.from_strings(lines) for lines in chunks(read_file('16.first', 2018), 4)]


def _test_1(dd: Debug):
    i = Interpreter()
    print(dd)
    for fname in sorted(Interpreter.func_names):
        regs = getattr(i, fname)(dd.inst, dd.before)
        success = int(dd.after == regs)
        print(f'{fname}: {success} {regs}')


def part1():
    debug_data = parse_test_data()
    i = Interpreter()

    counts = [sum(dd.after == getattr(i, fname)(dd.inst, dd.before)
                  for fname in Interpreter.func_names)
              for dd in debug_data]

    return sum(c >= 3 for c in counts)


def _determine_opcodes() -> List[str]:
    opcodes = {i: set(Interpreter.func_names) for i in range(16)}
    i = Interpreter()

    debug_data = parse_test_data()
    for dd in debug_data:
        opcodes[dd.inst.opcode] &= {fname for fname in Interpreter.func_names
                                    if dd.after == getattr(i, fname)(dd.inst, dd.before)}
    solved = [''] * 16
    min_key = lambda kv: len(kv[1])
    while opcodes:
        oc, vals = min(opcodes.items(), key=min_key)
        solved[oc] = first(vals)
        opcodes.pop(oc)
        for cur in opcodes.values():
            cur -= vals

    return solved


def part2():
    opcodes = _determine_opcodes()
    i = Interpreter()
    regs = [0, 0, 0, 0]
    for inst in map(Inst.from_str, read_file('16.second', 2018)):
        regs = getattr(i, opcodes[inst.opcode])(inst, regs)

    return regs[0]


def __main():
    print(part1())
    print(part2())
    test()


if __name__ == '__main__':
    __main()
