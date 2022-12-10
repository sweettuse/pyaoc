from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from itertools import count
from typing import Callable, Generator, NamedTuple

from rich import print
from pyaoc2019.utils import chunks, read_file, mapt


class Inst(NamedTuple):
    num_cycles: int
    offset: int

    @classmethod
    def from_str(cls, s) -> Inst:
        val = 0
        name, *extra = s.split()
        if extra:
            val = int(extra[0])
        return cls(cls.get_num_cycles(name), val)

    @classmethod
    def get_num_cycles(cls, inst_name):
        return dict(addx=2, noop=1)[inst_name]

def parse_data(name) -> tuple[Inst, ...]:
    return mapt(Inst.from_str, read_file(name))


def part1(data):
    val = 1
    pc = 0
    res = [val, val]
    for inst in data:
        for _ in range(inst.num_cycles - 1):
            pc += 1
            res.append(val)
        pc += 1
        val += inst.offset
        res.append(val)

    return sum(pc * res[pc] for pc in range(20, 221, 40))


data = parse_data(10)
print(part1(data))


# =========================================================================================
# part 2
# =========================================================================================


def clock(start=0):
    yield from count(start)


class Event(NamedTuple):
    t: int
    fn: Callable[[], None]


@dataclass
class Machine:
    """racing the beam"""
    insts: list[Inst]
    reg_x: int = 1
    q: deque[Event] = deque()

    def __post_init__(self):
        self._load_instructions()

    def _load_instructions(self):
        cur = 0
        for inst in self.insts:
            cur += inst.num_cycles
            self.q.append(Event(cur, lambda offset=inst.offset: self.add_x(offset)))

    def execute(self) -> Generator[str, None, None]:
        for t in clock():
            self._process_event(t)
            if not self.q:  # no more events
                return

            yield self._cur_char(t)

    def _process_event(self, t) -> None:
        """process first event if time has come"""
        event = self.q[0]
        if event.t != t:
            return

        event.fn()
        self.q.popleft()

    def _cur_char(self, t) -> str:
        return '\u2588' if self._lit_up(t) else ' '
    
    def _lit_up(self, t) -> bool:
        return abs((t % 40) - self.reg_x) <= 1

    def add_x(self, val):
        self.reg_x += val


data = parse_data(10)


def part2(data):
    m = Machine(data)
    return '\n'.join(map(''.join, chunks(m.execute(), 40)))


print(part2(data))
