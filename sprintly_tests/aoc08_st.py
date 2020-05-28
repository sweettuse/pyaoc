from collections import defaultdict
from functools import partial
from typing import NamedTuple, Callable, Iterable

from pyaoc2019.utils import read_file

__author__ = 'acushner'


class Rule(NamedTuple):
    """b inc 5 if a > 1"""
    reg: str
    action: Callable[[int], int]
    comp_reg: str
    comparison: Callable[[int], bool]

    @classmethod
    def from_str(cls, s):
        reg, act, act_val, _, comp_reg, comp, comp_val = s.split()
        action = partial(actions[act], int(act_val))
        comparison = lambda _val: eval(f'{_val} {comp} {comp_val}')
        return cls(reg, action, comp_reg, comparison)


actions = dict(
    inc=lambda action_val, reg_val: reg_val + action_val,
    dec=lambda action_val, reg_val: reg_val - action_val,
)


class Registers:
    def __init__(self):
        self._regs = defaultdict(int)

    def process_rule(self, rule: Rule):
        res = 0
        if rule.comparison(self._regs[rule.comp_reg]):
            res = self._regs[rule.reg] = rule.action(self._regs[rule.reg])
        return res

    def run(self, rules: Iterable[Rule]):
        running_max = max(map(self.process_rule, rules))
        return max(self._regs.values()), running_max


def __main():
    # print(Rule.from_str('b inc 5 if a > 1'))
    rules = read_file(8, 2017)
    print(Registers().run(map(Rule.from_str, rules)))


if __name__ == '__main__':
    __main()
