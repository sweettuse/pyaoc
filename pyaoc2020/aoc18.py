from typing import Any, Iterator

from pyaoc2019.utils import read_file, timer
from operator import add, mul

__author__ = 'acushner'

data = read_file(18, 2020)


def _preparse_line(s: str):
    tokens = s.replace('(', '( ').replace(')', ' )').split()
    return [int(t) if t.isdigit() else t for t in tokens]


op_map = {'+': add, '*': mul}


def _parse_expr(tokens: Iterator[Any]):
    """states:
    0 - left int or paren
    1 - operator
    2 - right int or paren
    """
    vals = []
    op = None
    tokens = iter(tokens)
    for t in tokens:
        if op and len(vals) == 2:
            vals[:] = [op(*vals)]
            op = None
        if isinstance(t, int):
            vals.append(t)
        elif t == '(':
            vals.append(_parse_expr(tokens))
        elif t == ')':
            return sum(vals)
        else:
            op = op_map[t]
    if op:
        return op(*vals)
    return vals[-1]


def _parse_line(s):
    return _parse_expr(_preparse_line(s))


def part1and2(func=_parse_line):
    return sum(map(func, data))


class MyInt(int):
    """complete and utter hack

    i cheat here and use the precedence of python's operators but change their evaluation
    so `__add__` multiplies and `__mul__` adds.

    i then switch the the operators around on the input string so that, in conjunction with `eval`,
    a call to `*` will have the higher precedence but will really call `+` and vice versa

    note: `__truediv__` implements the extension for part 1
    """

    def __add__(self, other):
        """this actually multiplies"""
        return MyInt(int(self) * int(other))

    def __mul__(self, other):
        """this actually adds"""
        return MyInt(int(self) + int(other))

    def __truediv__(self, other):
        """this actually multiplies

        # separate from `__add__` because i need something with the same precedence as `__mul__`
        only here to allow me to solve part1 in this horrible, horrible way
        """
        return MyInt(int(self) * int(other))


def _parse_line2(s: str, op_sub=None):
    res = []
    op_sub = op_sub or dict(zip('+*', '*+'))
    for t in _preparse_line(s):
        if isinstance(t, int):
            res.append(f'MyInt({t})')
        elif t in {'+', '*'}:
            res.append(op_sub[t])
        else:
            res.append(t)
    return eval(''.join(res))


def part1withhack():
    return sum(_parse_line2(s, {'+': '*', '*': '/'}) for s in data)


@timer
def __main():
    print(part1and2())
    print(part1withhack())
    print(part1and2(_parse_line2))


# 11004703763391
# 11004703763391
# 290726428573651
# '__main' took 0.046353158 seconds


if __name__ == '__main__':
    __main()
