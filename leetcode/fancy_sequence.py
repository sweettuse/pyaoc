# https://leetcode.com/problems/fancy-sequence/
__author__ = 'acushner'

from functools import reduce, partial, lru_cache
from itertools import groupby
from operator import mul, add, itemgetter


def parse_file(fname):
    with open(fname) as f:
        return list(map(eval, f))


def run(obj, cmds, args=None, *, do_print=False):
    if isinstance(cmds, str) and args is None:
        cmds, args = parse_file(cmds)
    z = zip(cmds, args)
    next(z)
    for c, a in z:
        res = getattr(obj, c)(*a)
        if do_print and res:
            print(c, res)


from pyaoc2019.utils import localtimer


def pipe(*funcs):
    def res(val):
        for f in funcs:
            val = f(val)
        return val

    return res


class Fancy:

    def __init__(self):
        self.s = []
        self._chain = []
        self._realized = []
        self._idx_start = {}

    def append(self, val: int) -> None:
        self._chain.append(('append', val))

    def addAll(self, inc: int) -> None:
        self._chain.append((add, inc))

    def multAll(self, m: int) -> None:
        self._chain.append((mul, m))

    def getIndex(self, idx: int) -> int:
        self._realize()
        if idx >= len(self.s):
            return -1
        val = self.s[idx]
        funcs = self._realized[self._idx_start[idx]:]
        if funcs:
            val = pipe(*funcs)(val)
        self.s[idx] = val
        self._idx_start[idx] = len(self._realized)
        return val % 1_000_000_007

    def _realize(self):
        for op, op_vals in groupby(self._chain, key=itemgetter(0)):
            vals = map(itemgetter(1), op_vals)
            if op is mul:
                self._realized.append(partial(mul, reduce(mul, vals, 1)))
            elif op is add:
                self._realized.append(partial(add, reduce(add, vals, 0)))
            else:
                for v in vals:
                    self._idx_start[len(self.s)] = len(self._realized)
                    self.s.append(v)

        self._chain.clear()

    def _create_eval(self, tmp, tmp2):
        res = f'lambda x: {"".join(reversed(tmp))}x{"".join(tmp2)}'
        tmp.clear()
        tmp2.clear()
        return eval(res)

    def _realize_eval(self):
        tmp = []
        tmp2 = []
        for op, op_vals in groupby(self._chain, key=itemgetter(0)):
            vals = map(itemgetter(1), op_vals)
            if op is mul:
                tmp.append(f'mul({reduce(mul, vals, 1)}, ')
                tmp2.append(')')
            elif op is add:
                tmp.append(f'add({reduce(add, vals, 0)}, ')
                tmp2.append(')')
            else:
                if tmp:
                    self._realized.append(self._create_eval(tmp, tmp2))
                for v in vals:
                    self._idx_start[len(self.s)] = len(self._realized)
                    self.s.append(v)
        if tmp:
            self._realized.append(self._create_eval(tmp, tmp2))

        self._chain.clear()

    def _realize_tmp(self):
        tmp = []
        for op, op_vals in groupby(self._chain, key=itemgetter(0)):
            vals = map(itemgetter(1), op_vals)
            if op is mul:
                tmp.append(partial(mul, reduce(mul, vals, 1)))
            elif op is add:
                tmp.append(partial(add, reduce(add, vals, 0)))
            else:
                self._realized.append(pipe(*tmp))
                tmp.clear()
                for v in vals:
                    self._idx_start[len(self.s)] = len(self._realized)
                    self.s.append(v)
        if tmp:
            self._realized.append(pipe(*tmp))
            tmp.clear()

        self._chain.clear()


class FancyO:

    def __init__(self):
        self.s = []

    def append(self, val: int) -> None:
        self.s.append(val)

    def addAll(self, inc: int) -> None:
        self.s = [v + inc for v in self.s]

    def multAll(self, m: int) -> None:
        self.s = [v * m for v in self.s]

    def getIndex(self, idx: int) -> int:
        if idx >= len(self.s):
            return -1
        return self.s[idx] % 1_000_000_007


# f = Fancy()
# f.append(1)
# f.addAll(1)
# f.multAll(2)
# print(f.getIndex(0))
# f.multAll(2)
# print(f.getIndex(0))
# f.multAll(2)
# print(f.getIndex(0))
#
# with localtimer():
#     for _ in range(100):
#         f = Fancy()
#         f.append(8, )
#         (f.getIndex(0, ))
#         for _ in range(1000):
#             f.multAll(7, )
#             f.addAll(2)
#             f.append(5, )
#             (f.getIndex(0, ))
#         f.append(3, )
#         f.addAll(6, )
#         (f.getIndex(0, ))
#     print(f.getIndex(32))

f = Fancy()
with localtimer():
    run(f, '/tmp/in', do_print=True)


def __main():
    pass


if __name__ == '__main__':
    __main()
