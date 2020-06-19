from functools import lru_cache, wraps
from typing import List, NamedTuple

from pyaoc2019.utils import read_file, timer


class Inst(NamedTuple):
    """instruction for computer to computate"""
    cmd: str
    args: List[str]

    @classmethod
    def from_str(cls, s: str):
        cmd, *args = s.split()
        return cls(cmd, args)


def _convert_to_val(func):
    """decorator that will convert the first arg from either a reg or an int to its int val"""

    @wraps(func)
    def wrapper(self, reg_or_val, *args):
        val = self.regs[reg_or_val] if reg_or_val.isalpha() else int(reg_or_val)
        return func(self, val, *args)

    return wrapper


def _inc_pc(func):
    @wraps(func)
    def wrapper(self, *args):
        res = func(self, *args)
        self._pc += 1
        return res

    return wrapper


class Computer:
    """computate all teh things!"""

    def __init__(self, inst_strs: List[str], **reg_overrides):
        self.regs = {**dict.fromkeys('abcd', 0), **reg_overrides}
        self._insts = self._to_insts(inst_strs)
        self._pc = 0

    @staticmethod
    def _to_insts(inst_strs: List[str]) -> List[Inst]:
        return [Inst.from_str(s) for s in inst_strs]

    @_inc_pc
    def inc(self, reg):
        """increment register by one"""
        self.regs[reg] += 1

    @_inc_pc
    def dec(self, reg):
        """decrement register by one"""
        self.regs[reg] -= 1

    @_convert_to_val
    def jnz(self, val, offset):
        """jump non-zero: jump if val at reg or val is non-zero"""
        self._pc += int(offset) if val else 1

    @_convert_to_val
    @_inc_pc
    def cpy(self, val: int, reg):
        """copy reg or val to reg"""
        self.regs[reg] = val

    def _exec_inst(self, inst: Inst):
        return getattr(self, inst.cmd)(*inst.args)

    def run(self):
        cnt = 0
        while self._pc < len(self._insts):
            cnt += 1
            self._exec_inst(self._insts[self._pc])
        print(f'total insts processed: {cnt}')


@timer
def aoc12(comp):
    comp.run()
    return comp.regs


def __main():
    inst_strs = read_file(12, 2016)
    comp = Computer(inst_strs)
    print(aoc12(comp))


if __name__ == '__main__':
    __main()
