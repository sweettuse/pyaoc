__author__ = 'acushner'

from functools import lru_cache, wraps
from typing import List

from pyaoc2019.utils import read_file, localtimer


def _get_val(func):
    @wraps(func)
    def _wrapper(self, val_or_reg, *args):
        try:
            val = int(val_or_reg)
        except ValueError:
            val = self.regs[val_or_reg]
        return func(self, val, *args)

    return _wrapper


def _inc_pc(func):
    @wraps(func)
    def _wrapper(self, *args):
        res = func(self, *args)
        self._pc += 1
        return res

    return _wrapper


class Computer:
    # TODO: talk about how, from last sprintly test, `length` could have been avoided
    def __init__(self, insts: List[str], **overrides):
        self.regs = self._init_regs(**overrides)
        self._pc = 0
        self._insts = insts

    @staticmethod
    def _init_regs(**overrides):
        regs = dict.fromkeys('abcd', 0)
        regs.update(overrides)
        return regs

    @_get_val
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

    @_get_val
    def jnz(self, val, offset):
        """inc/dec program counter if val is non-zero"""
        self._pc += int(offset) if val else 1

    @property
    @lru_cache(4)
    def _funcs(self):
        return {name: getattr(self, name) for name in dir(self) if not name.startswith('_')}

    def _exec_inst(self, s):
        fn, *args = s.split()
        self._funcs[fn](*args)

    def run(self):
        while 0 <= self._pc < len(self._insts):
            self._exec_inst(self._insts[self._pc])


def aoc11(insts: List[str], **overrides):
    comp = Computer(insts, **overrides)
    comp.run()
    return comp.regs['a']


def __main():
    insts = read_file(11, 2016)
    with localtimer():
        print(aoc11(insts))
    with localtimer():
        print(aoc11(insts, c=1))


if __name__ == '__main__':
    __main()
