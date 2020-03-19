from asyncio import Queue
import asyncio
from collections import Counter
from contextlib import suppress
from itertools import count
from operator import itemgetter
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
    def __init__(self, instructions, mode=0):
        self._insts = instructions
        U.exhaust(map(print, enumerate(instructions)))

        self._regs = dict.fromkeys('abcdefgh', 0)
        self._regs['a'] = mode
        self._pc = 0
        self._max_pc = 0
        self._inst_counts = Counter()
        self._mul_count = 0

    def __setitem__(self, key, value):
        self._regs[key] = value

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._regs[item]
        return item

    @classmethod
    def from_strs(cls, strs: List[str], mode=0):
        return cls([Inst.from_str(s) for s in strs], mode)

    async def _run_inst(self, inst: Inst):
        await getattr(self, inst.inst)(inst.reg, *map(self.__getitem__, inst.args))

    @property
    def debug_str(self):
        insts = {(iid, i_count): self._insts[iid] for iid, i_count in self._inst_counts.most_common(4)}
        return f'{self._pc}/{self._max_pc} | {insts} | {self._regs}'

    async def run(self):
        try:
            for i in count():
                inst = self._insts[self._pc]
                self._inst_counts[self._pc] += 1
                if not i % 1e6:
                    print(i, self.debug_str)
                    print(self._inst_counts)
                    print()
                self._max_pc = max(self._pc, self._max_pc)
                await self._run_inst(inst)
                self._pc += 1
        finally:
            print(self._inst_counts)

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
            # before = self._pc
            self._pc += val - 1
            # print(f'jnz: {before} {val} {self._pc + 1}')




@U.timer
def aoc23(mode):
    reg = Registers.from_strs(U.read_file(23, 2017), mode)
    try:
        asyncio.run(reg.run())
    except Exception:
        return reg._mul_count


def __main():
    # print(aoc23(0))
    print(aoc23(1))


if __name__ == '__main__':
    __main()
