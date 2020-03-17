import asyncio
from asyncio import Queue, QueueEmpty
from collections import defaultdict, Counter
from contextlib import suppress
from typing import NamedTuple, List

from cytoolz.itertoolz import last
import uvloop
import pyaoc2019.utils as U

uvloop.install()

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
    def __init__(self, name, instructions, in_q: Queue, out_q: Queue, starting_vals):
        self.in_q = in_q
        self.out_q = out_q
        self._name = name
        self._insts = instructions
        self._starting_vals = starting_vals

        self._regs = defaultdict(int)
        self._pc = 0
        self._max_pc = 0
        self._inst_counts = Counter()
        self._send_count = 0
        if starting_vals:
            self._regs['p'] = last(starting_vals)

    def __setitem__(self, key, value):
        self._regs[key] = value

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._regs[item]
        return item

    @classmethod
    def from_strs(cls, name, strs: List[str], in_q, out_q, starts):
        return cls(name, [Inst.from_str(s) for s in strs], in_q, out_q, starts)

    async def _run_inst(self, inst: Inst):
        await getattr(self, inst.inst)(inst.reg, *map(self.__getitem__, inst.args))

    async def run(self):
        for v in self._starting_vals:
            await self.snd(v)
        # while True:
        for i in range(1000000):
            inst = self._insts[self._pc]
            self._inst_counts[self._pc] += 1
            if not i % 10000:
                print(i, self._name, f'{self._pc}/{self._max_pc}', inst, self.in_q.qsize(),
                      self._inst_counts.most_common(6), self._regs)
            await self._run_inst(inst)
            self._pc += 1
            self._max_pc = max(self._pc, self._max_pc)

    async def set(self, reg, val: int):
        self[reg] = val

    async def add(self, reg, val):
        self[reg] += val

    async def mul(self, reg, val):
        self[reg] *= val

    async def mod(self, reg, val):
        self[reg] %= val

    async def jgz(self, reg, val):
        try:
            reg_val = int(reg)
        except Exception:
            reg_val = self[reg]
        if reg_val > 0:
            self._pc += val - 1

    async def snd(self, reg):
        """send"""
        self._send_count += 1
        await self.out_q.put(self[reg])

    async def rcv(self, reg):
        """receive"""
        v = await asyncio.wait_for(self.in_q.get(), 3)
        self[reg] = v


class RegA(Registers):
    def __init__(self, name, instructions, in_q: Queue, out_q: Queue, starting_vals):
        super().__init__(name, instructions, in_q, out_q, starting_vals)
        self._sounds = []
        self._recovered_sounds = []

    @classmethod
    def from_strs(cls, name, strs: List[str], in_q=Queue(), out_q=Queue(), starts=[]):
        return super().from_strs(name, strs, in_q, out_q, starts)

    async def snd(self, reg):
        self._sounds.append(self[reg])

    async def rcv(self, reg):
        if self[reg]:
            self._recovered_sounds.append(last(self._sounds))
            raise Result(last(self._recovered_sounds))


async def aoc18_a():
    insts = U.read_file(18, 2017)
    regs = RegA.from_strs('regA', insts)
    try:
        await regs.run()
    except Result as r:
        return r.args[0]


async def aoc18_b():
    fn = 18
    q01 = Queue(), Queue()
    r0 = Registers.from_strs('reg0', U.read_file(fn, 2017), *q01, [1, 2, 0])
    r1 = Registers.from_strs('reg1', U.read_file(fn, 2017), *reversed(q01), [1, 2, 1])
    try:
        await asyncio.gather(r0.run(), r1.run())
    except asyncio.TimeoutError:
        print('we are done')
    print(r0._send_count, r0._regs)
    print(r1._send_count, r1._regs)


def __main():
    with U.localtimer():
        print(asyncio.run(aoc18_b()))


if __name__ == '__main__':
    __main()
