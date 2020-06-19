__author__ = 'acushner'

from functools import lru_cache, wraps
from typing import List, NamedTuple, Any

from pyaoc2019.utils import read_file, localtimer


def _convert_val(func):
    """decorator to convert either a value or a register into an int"""

    @wraps(func)
    def _wrapper(self, val_or_reg, *args):
        val = self.regs[val_or_reg] if val_or_reg.isalpha() else int(val_or_reg)
        return func(self, val, *args)

    return _wrapper


def _inc_pc(func):
    """decorator to increment program counter"""

    @wraps(func)
    def _wrapper(self, *args):
        res = func(self, *args)
        self._pc += 1
        return res

    return _wrapper


class Inst(NamedTuple):
    fn: str
    args: List[Any]

    @classmethod
    def from_str(cls, s):
        fn, *args = s.split()
        return cls(fn, args)


class Computer:
    # TODO: talk about how, from last sprintly test:
    #  - `length` could have been cribbed from used_comps
    #  - hash can be `id(self)`
    def __init__(self, inst_strs: List[str], **overrides):
        self.regs = self._init_regs(**overrides)
        self._pc = 0
        self._insts = self._to_insts(inst_strs)

    @staticmethod
    def _init_regs(**overrides):
        regs = dict.fromkeys('abcd', 0)
        regs.update(overrides)
        return regs

    @staticmethod
    def _to_insts(inst_strs: List[str]) -> List[Inst]:
        return [Inst.from_str(s) for s in inst_strs]

    @_convert_val
    @_inc_pc
    def cpy(self, val, reg):
        """copy val into reg"""
        self.regs[reg] = val

    @_inc_pc
    def inc(self, reg):
        """increment reg by 1"""
        self.regs[reg] += 1

    @_inc_pc
    def dec(self, reg):
        """decrement reg by 1"""
        self.regs[reg] -= 1

    @_convert_val
    def jnz(self, val, offset):
        """jump non-zero: inc/dec program counter by offset if val is non-zero"""
        self._pc += int(offset) if val else 1

    def _exec_inst(self, inst: Inst):
        getattr(self, inst.fn)(*inst.args)

    def run(self):
        while 0 <= self._pc < len(self._insts):
            self._exec_inst(self._insts[self._pc])


def aoc12(insts: List[str], **overrides):
    comp = Computer(insts, **overrides)
    comp.run()
    return comp.regs['a']


def __main():
    insts = read_file(12, 2016)
    with localtimer():
        print(aoc12(insts))
    with localtimer():
        print(aoc12(insts, c=1))


if __name__ == '__main__':
    __main()
