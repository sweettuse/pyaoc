from __future__ import annotations
from typing import NamedTuple, Type

from pyaoc2019.utils import chunks, get_file_path


class Inst(NamedTuple):
    qty: int
    frm: int
    to: int

    @classmethod
    def from_str(cls, s) -> Inst:
        _, n, _, frm, _, to = s.split()
        return cls(*map(int, (n, frm, to)))

    def execute(self, stacks: list[Stack]) -> None:
        move = stacks[self.frm].pop(self.qty)
        stacks[self.to].push(*move)


class Stack:
    def __init__(self):
        self._s: list[str] = []

    def push(self, *elements):
        self._s.extend(elements)

    def pop(self, n) -> list[str]:
        return [self._s.pop() for _ in range(n)]

    def reverse(self):
        self._s.reverse()

    def peek(self) -> str:
        return (self._s and self._s[-1]) or ''

    def __str__(self):
        return f'Stack({self._s})'


class NewStack(Stack):
    def pop(self, n) -> list[str]:
        self._s, move = self._s[:-n], self._s[-n:]
        return move


def _parse_crates(lines: list[str], stack_type=Stack) -> list[Stack]:
    res = [stack_type() for _ in range(10)]
    for l in lines[:-1]:
        for stack, crate in zip(res[1:], chunks(l, 4)):
            if crate_id := crate[1].strip():
                stack.push(crate_id)

    for stack in res:
        stack.reverse()

    return res


def _parse_instructions(lines: list[str]) -> list[Inst]:
    return [Inst.from_str(l) for l in lines]


def parse_file(name, stack_type: Type[Stack]):
    with open(get_file_path(name)) as f:
        crates, insts = f.read().split('\n\n')

    return (
        _parse_crates(crates.splitlines(), stack_type),
        _parse_instructions(insts.splitlines()),
    )


def part1and2(name, stack_type) -> str:
    stacks, insts = parse_file(name, stack_type)
    for inst in insts:
        inst.execute(stacks)
    return ''.join(s.peek() for s in stacks[1:])


print(part1and2(5, Stack))
print(part1and2(5, NewStack))
