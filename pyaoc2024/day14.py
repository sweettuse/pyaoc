from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
from math import prod
import os
import time
from rich import print as rprint

from pyaoc2019.utils import RC, Coord, read_file, timer

@dataclass
class Robot:
    start: RC
    velocity: RC

    def move(self, num_seconds: int, height_width: RC) -> RC:
        abs_pos = self.start + self.velocity * num_seconds
        res = abs_pos % height_width
        return res

    @classmethod
    def from_str(cls, s: str) -> Robot:
        p, v = s.split()
        p, v = Coord(*eval(p[2:])), Coord(*eval(v[2:]))
        return cls(p.rc, v.rc)

def _read_data(*, test: bool) -> tuple[list[Robot], RC]:
    if test:
        fname = "14.test.txt" 
        height_width = Coord(11, 7).rc
    else:
        fname = "14.txt"
        height_width = Coord(101, 103).rc

    return [Robot.from_str(line) for line in read_file(fname)], height_width

    
def _display(pos: set[RC], height_width) -> None:
    res = [
        ''.join('X' if RC(r, c) in pos else '.' for c in range(height_width.c)) for r in range(height_width.r)
    ]
    print("\n".join(res))
    print(30 * '-')


def part1(robots, height_width):
    middle = height_width // RC(2, 2)
    final_pos = [r.move(100, height_width) for r in robots]
    by_quadrant = [
        (pos.r < middle.r, pos.c < middle.c)
        for pos in final_pos
        if pos.r != middle.r and pos.c != middle.c
    ]
    return prod(Counter(by_quadrant).values())

@timer
def part2(robots, height_width):
    cur_min = float('inf')
    start = 100000
    end = start + 100000
    for i in range(start, end, 1):
        cur = {r.move(i, height_width) for r in robots}
        if len(cur) < cur_min:
            cur_min = len(cur)
            print(i, cur_min)
            # _display(cur, height_width)

def _find_longest_diagonal(pos: set[RC]):
    pos = set(pos)
    longest_chain = 0
    while pos:
        cur_chain = set()
        stack = [pos.pop()]
        while stack:
            cur = stack.pop()
            cur_chain.add(cur)
            if (nxt := cur + RC(1, 1)) in pos:
                pos.remove(nxt)
                stack.append(nxt)
                cur_chain.add(nxt)
            if (nxt := cur - RC(1, 1)) in pos:
                pos.remove(nxt)
                stack.append(nxt)
                cur_chain.add(nxt)
        longest_chain = max(longest_chain, len(cur_chain))
    return longest_chain
        


@timer
def part2_a(robots, height_width):
    min_distinct = float('inf')
    seen = set()
    continuous_seen = 0
    longest_diagonal = 0
    def _part2_helper(num_seconds) -> bool:
        nonlocal min_distinct, continuous_seen, longest_diagonal
        middle = height_width // RC(2, 2)
        adj = height_width - RC(1, 1)
        final_pos = frozenset({r.move(num_seconds, height_width) for r in robots})
        # time.sleep(1/30)
        # os.system("clear")
        # _display(final_pos, height_width)
        if len(final_pos) < min_distinct:
            min_distinct = len(final_pos)
            print(num_seconds, min_distinct)
        if final_pos in seen:
            continuous_seen += 1
            print(num_seconds, f"dupe detected at {continuous_seen}")
            if continuous_seen > 100:
                raise Exception("done")
        else:
            continuous_seen = 0

        if (cur_diagonal := _find_longest_diagonal(final_pos)) > longest_diagonal:
            longest_diagonal = cur_diagonal
            print(num_seconds, f"diag: {longest_diagonal}")
            _display(final_pos, height_width)

        seen.add(final_pos)


        left_right = defaultdict(set)
        for pos in final_pos:
            if pos.c == middle.c:
                continue

            left_right["left" if pos.c < middle.c else "right"].add(pos)
        mirrored = {RC(pos.r, adj.c - pos.c) for pos in left_right["left"]}
        return mirrored == left_right["right"]
    # for i in range(1_000_000, 2_000_000):
    for i in range(13000):
        if _part2_helper(i):
            print(i)
            return


def _main():
    data = _read_data(test=False)

    print(part1(*data))
    print(part2_a(*data))

if __name__ == "__main__":
    _main()
