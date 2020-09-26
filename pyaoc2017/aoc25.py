from collections import deque

from more_itertools import last

import pyaoc2019.utils as U

from enum import Enum
from typing import NamedTuple, Iterator, Dict

__author__ = 'acushner'


class State(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'


class Inst(NamedTuple):
    write_val: int
    move: int
    next_state: State

    @classmethod
    def from_iter(cls, it):
        write_val = int(next(it)[-2])
        move = dir_offset_map[last(next(it).split())]
        next_state = State[next(it)[-2]]
        return cls(write_val, move, next_state)


dir_offset_map = {
    'left.': -1,
    'right.': 1,
}


class StateVal(NamedTuple):
    state: State
    val: int


def _add_to_dict(res: Dict, state: State, it: Iterator):
    cur_val = int(next(it)[-2])
    res[StateVal(state, cur_val)] = Inst.from_iter(it)
    cur_val = int(next(it)[-2])
    res[StateVal(state, cur_val)] = Inst.from_iter(it)


def parse_data(filename) -> Dict[StateVal, Inst]:
    lines = iter(U.read_file(filename, 2017))
    res = {}
    for l in lines:
        if l.startswith('In state'):
            cur_state = State[l[-2]]
            _add_to_dict(res, cur_state, lines)
    return res


class StateMachine:
    def __init__(self, state_data: Dict[StateVal, Inst]):
        self._d = deque([0])
        self._state_data = state_data
        self._cur_idx = 0

    def _grow_if_necessary(self, grow_size=1000):
        if self._cur_idx >= len(self._d):
            self._d.extend(grow_size * [0])
        elif self._cur_idx <= 0:
            self._d.extendleft(grow_size * [0])
            self._cur_idx = grow_size

    def run(self, state=State.A, n_iter=12964419):
        for _ in range(n_iter):
            self._grow_if_necessary()
            inst = self._state_data[state, self._d[self._cur_idx]]
            self._d[self._cur_idx] = inst.write_val
            self._cur_idx += inst.move
            state = inst.next_state

    @property
    def checksum(self):
        return sum(self._d)


def __main():
    sm = StateMachine(parse_data(25))
    with U.localtimer():
        sm.run()
    print(sm.checksum)


if __name__ == '__main__':
    __main()
