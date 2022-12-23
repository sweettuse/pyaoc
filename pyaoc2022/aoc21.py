from __future__ import annotations
from bisect import bisect_left
from contextlib import suppress
from dataclasses import dataclass
from typing import Callable, ClassVar, Optional
from pyaoc2019.utils import exhaust, localtimer, read_file, mapt, timer
from rich import print


@dataclass
class Monkey:
    name: str
    fn: Callable
    lop: Optional[str] = None
    rop: Optional[str] = None
    registry: ClassVar[dict[str, Callable]] = {}

    def __post_init__(self):
        self.registry[self.name] = self.fn

    @classmethod
    def from_str(cls, s: str) -> Monkey:
        name, fn_str = s.split(': ')
        registry = cls.registry
        operands = []
        if fn_str.isdigit():
            fn = lambda v=int(fn_str): v

        else:
            m1, op, m2 = fn_str.split()
            operands = m1, m2
            s = f'registry[{m1!r}]() {op} registry[{m2!r}]()'
            fn = lambda registry=cls.registry: eval(s)

        return cls(name, fn, *operands)


def parse_data(name, monkey_type=Monkey):
    monkey_type.registry.clear()
    return mapt(monkey_type.from_str, read_file(name))


monkeys = parse_data(21)


def part1():
    return Monkey.registry['root']()


@dataclass
class Monkey2:
    """actually create the raw functions"""

    name: str
    val: Optional[str] = None
    lop: Optional[str] = None
    op: Optional[str] = None
    rop: Optional[str] = None
    registry: ClassVar[dict[str, Monkey2]] = {}

    def __post_init__(self):
        self.registry[self.name] = self

    @classmethod
    def from_str(cls, s: str) -> Monkey2:
        name, fn_str = s.split(': ')
        if fn_str.isdigit():
            operands = [fn_str]
        else:
            operands = [None, *fn_str.split()]

        return cls(name, *operands)

    def __call__(self) -> str:
        if self.val is not None:
            return self.val
        return f'({self.registry[self.lop]()}) {self.op} ({self.registry[self.rop]()})'


class Search:
    def __init__(self, name, size: int):
        self.name = name
        self.size = size

    def __getitem__(self, item):
        Monkey.registry['humn'] = lambda: item
        return -int(Monkey.registry[self.name]())

    def __len__(self):
        return self.size


def part2():
    root = next(m for m in monkeys if m.name == 'root')
    lval = Monkey.registry[root.lop]()
    rval = Monkey.registry[root.rop]()

    s = Search(root.lop, int(1e16))
    return bisect_left(s, -rval)


print(part1())
print(part2())
