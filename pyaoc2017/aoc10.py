from functools import reduce
from operator import xor
from typing import List, Iterable

from cytoolz.itertoolz import first

import pyaoc2019.utils as U

__author__ = 'acushner'


def apply_rotations(data: Iterable[int], input_lens: List[int], skip=0):
    d = U.SliceableDeque(data)
    total_rotation = 0
    for skip, il in enumerate(input_lens, skip):
        d[:il] = d[:il]
        cur_skip = -skip - il
        total_rotation += cur_skip
        d.rotate(cur_skip)
    return d, total_rotation


def aoc10_a():
    input_lens = [int(e) for e in first(U.read_file(10, 2017)).split(',')]
    d, total_rotation = apply_rotations(range(256), input_lens)
    d.rotate(-total_rotation)
    return d[0] * d[1]


def knot_hash(s: str):
    const = 17, 31, 73, 47, 23
    input_lens = [ord(e) for e in s.strip()]
    input_lens.extend(const)
    d = range(256)
    total_rotation = 0
    for i in range(64):
        d, cur_rotation = apply_rotations(d, input_lens, len(input_lens) * i)
        total_rotation += cur_rotation
    d.rotate(-total_rotation)
    res = [hex(reduce(xor, c)) for c in U.chunks(d, 16)]
    return ''.join(h[-2:] for h in res).replace('x', '0')


def __main():
    print(aoc10_a())
    print(knot_hash(first(U.read_file(10, 2017))))


if __name__ == '__main__':
    __main()
