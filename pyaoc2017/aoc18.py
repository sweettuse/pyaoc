from collections import defaultdict
from queue import Queue
from typing import NamedTuple, Tuple, List

from cytoolz.itertoolz import first, last
from contextlib import suppress

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
    pass


class Registers:
    def __init__(self, instructions):
        self._insts = instructions
        self._regs = defaultdict(int)
        self._sounds = []
        self._recovered_sounds = []
        self._pc = 0

    def __setitem__(self, key, value):
        self._regs[key] = value

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._regs[item]
        return item

    @classmethod
    def from_strs(cls, strs: List[str]):
        return cls([Inst.from_str(s) for s in strs])

    def run(self):
        while True:
            inst = self._insts[self._pc]
            getattr(self, inst.inst)(inst.reg, *map(self.__getitem__, inst.args))
            self._pc += 1

    def snd(self, reg):
        self._sounds.append(self[reg])

    def set(self, reg, val: int):
        self[reg] = val

    def add(self, reg, val):
        self[reg] += val

    def mul(self, reg, val):
        self[reg] *= val

    def mod(self, reg, val):
        self[reg] %= val

    def rcv(self, reg):
        if self[reg]:
            self._recovered_sounds.append(last(self._sounds))
            raise Result(last(self._recovered_sounds))

    def jgz(self, reg, val):
        if self[reg] > 0:
            self._pc += val - 1


class Reg2(Registers):
    def __init__(self, instructions, in_q: Queue, out_q: Queue):
        super().__init__(instructions)
        self.in_q = in_q
        self.out_q = out_q

    def snd(self, reg):
        self.out_q.put(self[reg])

    def rcv(self, reg):
        self[reg] = self.in_q.get()


def aoc18_a():
    regs = Registers.from_strs(U.read_file(18, 2017))
    try:
        regs.run()
    except Result as r:
        return r.args[0]


def __main():
    print(aoc18_a())


if __name__ == '__main__':
    __main()
