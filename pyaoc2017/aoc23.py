from asyncio import Queue
import asyncio
from collections import Counter
from contextlib import suppress
from typing import NamedTuple, List

from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


class Inst(NamedTuple):
    inst: str
    reg: str
    args: List[int]

    @classmethod
    def from_str(cls, s):
        inst, reg, *args = s.split()
        with suppress(ValueError):
            args = [int(a) for a in args]
        return cls(inst, reg, args)


class Result(Exception):
    """stores result of calculation"""


class Registers:
    def __init__(self, name, instructions, in_q: Queue, out_q: Queue, starting_vals=None, mode=0):
        self.in_q = in_q
        self.out_q = out_q
        self._name = name
        self._insts = instructions
        self._starting_vals = starting_vals or []

        self._regs = dict.fromkeys('abcdefgh', 0)
        self._regs['a'] = mode
        self._pc = 0
        self._max_pc = 0
        self._inst_counts = Counter()
        self._send_count = 0
        self._mul_count = 0

    def __setitem__(self, key, value):
        self._regs[key] = value

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._regs[item]
        return item

    @classmethod
    def from_strs(cls, name, strs: List[str], in_q, out_q, starts, mode=0):
        return cls(name, [Inst.from_str(s) for s in strs], in_q, out_q, starts, mode)

    async def _run_inst(self, inst: Inst):
        await getattr(self, inst.inst)(inst.reg, *map(self.__getitem__, inst.args))

    async def run(self):
        for i in range(int(1e8)):
            inst = self._insts[self._pc]
            self._inst_counts[self._pc] += 1
            if not i % 1e6:
                print(i, self._name, f'{self._pc}/{self._max_pc}', inst, self.in_q.qsize(),
                      self._inst_counts.most_common(6), self._regs)
            await self._run_inst(inst)
            self._pc += 1
            self._max_pc = max(self._pc, self._max_pc)

    async def set(self, reg, val: int):
        if reg == 'h':
            print(f'h << {val}')
        self[reg] = val

    async def sub(self, reg, val):
        self[reg] -= val

    async def mul(self, reg, val):
        self[reg] *= val
        self._mul_count += 1

    async def jnz(self, reg, val):
        try:
            reg_val = int(reg)
        except ValueError:
            reg_val = self[reg]
        if reg_val:
            self._pc += val - 1


def in_python(a):
    b = c = d = e = f = g = h = 0

    def sub_1():
        nonlocal a, b, c, d, e, f, g, h
        b *= 100
        b -= -100000
        c = b
        c -= -17000
        f = 1
        d = 2
        e = 2
        g = d
        g *= e

    b = 93
    c = b
    if a:
        pass


@U.timer
def aoc23(mode):
    reg = Registers.from_strs('tuse', U.read_file(23, 2017), Queue(), Queue(), None, mode)
    try:
        asyncio.run(reg.run())
    except Exception:
        return reg._mul_count


def __main():
    print(aoc23(0))
    # print(aoc23(1))


if __name__ == '__main__':
    __main()
