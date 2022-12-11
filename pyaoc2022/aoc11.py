from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from math import prod
from typing import Callable

from rich import print
from pyaoc2019.utils import read_file, timer


@dataclass
class Monkey:
    num: int
    items: deque
    inflate_worry: Callable[[int], int]
    next_monkey: Callable[[int], int]
    div_by: int
    num_inspected: int = 0

    @classmethod
    def from_str(cls, s) -> Monkey:
        lines = iter(s.splitlines())

        l = next(lines)
        num = int(l.split()[-1][:-1])

        l = next(lines)
        items = deque(map(int, l.split(':')[-1].split(',')))

        l = next(lines)
        func_body = l.split(' = ')[-1].replace('old', 'orig_worry')
        inflate_worry = cls._get_inflate_worry_fn(func_body)

        l = next(lines)
        div_by = int(l.split()[-1])
        is_divisible_target = int(next(lines).split()[-1])
        is_not_divisible_target = int(next(lines).split()[-1])

        def next_monkey(new_worry):
            return is_not_divisible_target if new_worry % div_by else is_divisible_target

        return cls(num, items, inflate_worry, next_monkey, div_by)

    @classmethod
    def _get_inflate_worry_fn(cls, func_body: str):
        return eval(f'lambda orig_worry: ({func_body}) // 3')

    def process(self):
        while self.items:
            self.num_inspected += 1
            yield self._process_one(self.items.popleft())

    def _process_one(self, worry):
        new_worry = self.inflate_worry(worry)
        target = self.next_monkey(new_worry)
        return (target, new_worry)

    def add(self, worry):
        self.items.append(worry)


class Monkey2(Monkey):
    @classmethod
    def _get_inflate_worry_fn(cls, func_body):
        return eval(f'lambda orig_worry: {func_body}')


@dataclass
class Monkeys:
    monkeys: list[Monkey]
    mod_by: int

    @classmethod
    def from_file(cls, name, monkey_cls):
        monkeys = list(map(monkey_cls.from_str, read_file(name, do_split=False).split('\n\n')))
        mod_by = prod(m.div_by for m in monkeys)
        return cls(monkeys, mod_by)

    def execute_round(self):
        for m in self.monkeys:
            for target, worry in m.process():
                self.monkeys[target].add(worry % self.mod_by)


def part1(name):
    monkeys = Monkeys.from_file(name, Monkey)
    for _ in range(20):
        monkeys.execute_round()
    return prod(sorted(m.num_inspected for m in monkeys.monkeys)[-2:])


@timer
def part2(name):
    monkeys = Monkeys.from_file(name, Monkey2)
    for _ in range(10000):
        monkeys.execute_round()
    return prod(sorted(m.num_inspected for m in monkeys.monkeys)[-2:])


print(part1(11))
print(part2(11))
