__author__ = 'acushner'

# 8.6  Towers of Hanoi: In the classic problem of the Towers of Hanoi, you have 3 towers and N disks of
# different sizes which can slide onto any tower. The puzzle starts with disks sorted in ascending order
# of size from top to bottom (i.e., each disk sits on top of an even larger one). You have the following
# constraints:
# (1) Only one disk can be moved at a time.
# (2) A disk is slid off the top of one tower onto another tower.
# (3) A disk cannot be placed on top of a smaller disk.
# Write a program to move the disks from the first tower to the last using stacks.
from collections import deque
from functools import lru_cache

from pyaoc2019.utils import timer


class Stack(list):
    def put(self, v):
        if self and v > self.peek():
            raise ValueError(f'disks out of order {v = } > {self.peek() = }')
        self.append(v)

    def peek(self):
        return self[-1]

    def move_top_to(self, s: 'Stack'):
        s.put(self.pop())
        # print('|'.join(map(str, Stack.crap)))

    @lru_cache(0)
    def move_disks(self, qty, dest, buffer):
        if qty <= 0:
            return

        self.move_disks(qty - 1, buffer, dest)
        self.move_top_to(dest)
        buffer.move_disks(qty - 1, dest, self)


@timer
def towers(n):
    stacks = start, buffer, dest = [Stack(s) for s in (list(reversed(range(1, n + 1))), [], [])]
    Stack.crap = stacks
    start.move_disks(n, dest, buffer)
    # for s in stacks:
    #     print(s.move_disks.cache_info())
    # print(dest)


def __main():
    for n in range(16, 27):
        print(n, end=' ')
        towers(n)


if __name__ == '__main__':
    __main()


class Stacks:
    def __init__(self, n):
        self.stacks = [Stack(s) for s in (list(reversed(range(1, n + 1))), [], [])]

    def move(self, frm, to):
        self[to].put(self[frm].pop())

    def __getitem__(self, item):
        return self.stacks[item]

    def __str__(self):
        return '|'.join(map(str, self.stacks))

    @property
    def done(self):
        return not (self.stacks[0] or self.stacks[1])

    @property
    def num_empty(self):
        return sum(s.peek() == 0 for s in self.stacks)

    @property
    def _first_empty(self):
        for i, s in enumerate(self.stacks):
            if not s.peek():
                return i

    @property
    def _min_mid_max_idx(self):
        t = sorted((s.peek(), i) for i, s in enumerate(self.stacks))
        return [v[1] for v in t]

    def move_max_empty(self):
        *_, mx = self._min_mid_max_idx
        self.move(mx, self._first_empty)
        print(self)

    def move_mid_empty(self):
        _, mid, _ = self._min_mid_max_idx
        self.move(mid, self._first_empty)
        print(self)

    def move_min_mid(self):
        mn, mid, _ = self._min_mid_max_idx
        self.move(mn, mid)
        print(self)

    def move_min_max(self):
        mn, _, mx = self._min_mid_max_idx
        self.move(mn, mx)
        print(self)

    def move_mid_max(self):
        _, mid, mx = self._min_mid_max_idx
        self.move(mid, mx)
        print(self)
