from collections import defaultdict
from enum import Enum
from typing import Set, Tuple, Dict

import pyaoc2019.utils as U
from pyaoc2019.utils import Coord

__author__ = 'acushner'


class Direction(Enum):
    up = Coord(0, 1)
    right = Coord(1, 0)
    down = Coord(0, -1)
    left = Coord(-1, 0)

    def rotated(self, val):
        """
        0: rotate left
        1: rotate right
        """
        dirs = list(Direction)
        val = 2 * val - 1
        new_idx = (dirs.index(self) + val) % len(dirs)
        return dirs[new_idx]


class State(Enum):
    clean = 'clean'
    weakened = 'weakened'
    infected = 'infected'
    flagged = 'flagged'

    def __next__(self):
        return _state_map[self]


_state_map = dict(zip(State, list(State)[1:] + list(State)[:1]))


def parse_data(fn) -> Tuple[Coord, Dict[Coord, State]]:
    """return starting coord and dict of infected nodes"""
    res = defaultdict(lambda: State.clean)
    for y, r in enumerate(U.read_file(fn, 2017)):
        for x, v in enumerate(r):
            if v == '#':
                res[Coord(x, -y)] = State.infected
    start = Coord(x // 2, -y // 2)
    return start, res


def aoc22(fn, n_iter=100):
    cur, infected = parse_data(fn)
    infected = set(infected)
    d = Direction.up
    num_infected = 0
    for _ in range(n_iter):
        if is_infected := cur in infected:
            infected.remove(cur)
        else:
            infected.add(cur)
            num_infected += 1
        d = d.rotated(is_infected)
        cur += d.value
    return num_infected


def aoc22_b(fn, n_iter=10000):
    state_dir_map = {
        State.clean: lambda _d: _d.rotated(0),
        State.weakened: U.identity,
        State.infected: lambda _d: _d.rotated(1),
        State.flagged: lambda _d: _d.rotated(1).rotated(1)

    }
    cur, states = parse_data(fn)
    d = Direction.up
    num_infected = 0

    for _ in range(n_iter):
        s = states[cur]
        d = state_dir_map[s](d)
        s = states[cur] = next(s)

        if s is State.infected:
            num_infected += 1

        cur += d.value
    return num_infected


def __main():
    print(aoc22(22, 10000))
    with U.localtimer():
        print(aoc22_b(22, 10_000_000))


if __name__ == '__main__':
    __main()
