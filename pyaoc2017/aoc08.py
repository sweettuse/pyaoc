from collections import defaultdict
from functools import partial
from operator import sub, add

import pyaoc2019.utils as U

from typing import NamedTuple, Callable, List

__author__ = 'acushner'

data = defaultdict(int)


class Rule(NamedTuple):
    reg: str
    action: Callable[[int], int]
    cond_reg: str
    cond: Callable[[int], bool]

    @classmethod
    def from_str(cls, s):
        reg, action, val, _, cond_reg, condition, cond_val = s.split()
        action = actions[action](val)
        cond = lambda _val: eval(f'{_val} {condition} {cond_val}')
        return cls(reg, action, cond_reg, cond)

    def update(self, data):
        res = float('-inf')
        if self.cond(data[self.cond_reg]):
            res = data[self.reg] = self.action(data[self.reg])
        return res


actions = dict(
    dec=lambda val: lambda cur_reg: cur_reg - int(val),
    inc=lambda val: lambda cur_reg: cur_reg + int(val)
)


def parse_rules(fn=8):
    return [Rule.from_str(s) for s in U.read_file(fn, 2017)]


def aoc08(rules: List[Rule]):
    data = defaultdict(int)
    running_max = float('-inf')
    for r in rules:
        running_max = max(r.update(data), running_max)
    print(data)
    return max(data.values()), running_max


def __main():
    rules = parse_rules()
    print(aoc08(rules))


if __name__ == '__main__':
    __main()
