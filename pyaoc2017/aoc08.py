from collections import defaultdict
from functools import reduce
from typing import NamedTuple, Callable, List

import pyaoc2019.utils as U

__author__ = 'acushner'


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


actions = dict(
    dec=lambda val: lambda cur_reg: cur_reg - int(val),
    inc=lambda val: lambda cur_reg: cur_reg + int(val)
)


class Registers:
    def __init__(self):
        self.data = defaultdict(int)

    def process_rule(self, rule: Rule):
        res = float('-inf')
        if rule.cond(self.data[rule.cond_reg]):
            res = self.data[rule.reg] = rule.action(self.data[rule.reg])
        return res


def parse_rules(fn=8):
    return [Rule.from_str(s) for s in U.read_file(fn, 2017)]


def aoc08(rules: List[Rule]):
    registers = Registers()
    running_max = reduce(max, map(registers.process_rule, rules))
    return max(registers.data.values()), running_max


def __main():
    rules = parse_rules()
    print(aoc08(rules))


if __name__ == '__main__':
    __main()
