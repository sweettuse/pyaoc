from functools import wraps
from pyaoc2016.aoc12 import Computer, Inst, _convert_val, _inc_pc
from pyaoc2019.utils import read_file
from rich import print

one_arg = set('inc dec tgl'.split())
two_arg = set('cpy jnz'.split())


def make_safe(fn):
    if fn.__name__ not in one_arg | two_arg:
        return fn

    @wraps(fn)
    def wrapper(*a, **kw):
        try:
            return fn(*a, **kw)
        except:
            pass

    return wrapper


def safeify_class(cls):
    for name in set(dir(cls)) & (one_arg | two_arg):
        attr = getattr(cls, name)
        setattr(cls, name, make_safe(attr))
    return cls


@safeify_class
class C2(Computer):
    @_convert_val
    @_inc_pc
    def tgl(self, offset):
        target = self._pc + offset
        if not 0 <= target < len(self._insts):
            return

        inst = self._insts[target]
        if inst.fn in one_arg:
            inst.fn = 'dec' if inst.fn == 'inc' else 'inc'
        else:
            inst.fn = 'cpy' if inst.fn == 'jnz' else 'jnz'
        print(self._insts)

    def run(self):
        limit = 1500 ** 1500
        # limit = 1000
        i = 0
        while 0 <= self._pc < len(self._insts):
            i += 1
            if i >= limit:
                break
            if not i % 1:
                print(dict(pc=self._pc) | self.regs)
            self._exec_inst(self._insts[self._pc])

class C3(C2):
    @make_safe
    @_inc_pc
    def inc(self, reg):
        """increment reg by 1"""
        self.regs[reg] *= self.regs[reg]

def part1(insts: list[str]):
    comp = C2(insts, a=7)
    comp.run()
    return comp.regs['a']

def part2(insts: list[str]):
    comp = C2(insts, a=12)
    comp.run()
    return comp.regs['a']

def __main():
    insts = read_file('23.test', 2016)
    insts = read_file(23, 2016)
    print('res', part1(insts))

    insts = read_file(23, 2016)
    # print('res', part2(insts))

if __name__ == '__main__':
    __main()