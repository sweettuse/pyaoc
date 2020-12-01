from collections import defaultdict
from functools import reduce, partial
from typing import NamedTuple, Callable, List

import pyaoc2019.utils as U

__author__ = 'acushner'


class Rule(NamedTuple):
    """represent, e.g., 'b inc 5 if a > 1'"""
    reg: str
    action: Callable[[int], int]
    cond_reg: str
    cond: Callable[[int], bool]

    @classmethod
    def from_str(cls, s):
        reg, action, val, _, cond_reg, condition, cond_val = s.split()
        action = partial(actions[action], int(val))
        cond = lambda _val: eval(f'{_val} {condition} {cond_val}')
        return cls(reg, action, cond_reg, cond)


actions = dict(
    inc=lambda rule_val, reg_val: reg_val + rule_val,
    dec=lambda rule_val, reg_val: reg_val - rule_val,
)


class Registers:
    def __init__(self):
        self.data = defaultdict(int)

    def process_rule(self, rule: Rule):
        res = float('-inf')
        if rule.cond(self.data[rule.cond_reg]):
            res = self.data[rule.reg] = rule.action(self.data[rule.reg])
        return res


def aoc08(rules: List[Rule]):
    registers = Registers()
    running_max = max(*map(registers.process_rule, rules))
    return max(registers.data.values()), running_max


def __main():
    rules = [Rule.from_str(s) for s in U.read_file(8, 2017)]
    print(aoc08(rules))


if __name__ == '__main__':
    __main()
