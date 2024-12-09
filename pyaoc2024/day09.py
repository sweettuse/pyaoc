from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from itertools import repeat
from typing import Iterable, Iterator

from more_itertools import interleave, interleave_longest
# from rich import print

from pyaoc2019.utils import mapl, read_file

@dataclass
class Block:
    id: int | None


def _read_data(*, test: bool):
    fname = "09.test.txt" if test else "09.txt"
    data = mapl(int, read_file(fname)[0])
    occupied = list(enumerate(data[::2]))
    free = list(zip(repeat(None), data[1::2]))
    return [
        Block(id)
        for id, size in interleave_longest(occupied, free)
        for _ in range(size)
    ]

def _checksum(blocks: list[Block]) -> int:
    return sum(
        i * b.id
        for i, b in enumerate(blocks)
        if b.id is not None
    )

def _display(blocks: Iterable[Block]) -> None:
    import rich
    rich.print(''.join('.' if b.id is None else str(b.id) for b in blocks))

def part1(blocks: list[Block]) -> int:
    blocks = blocks.copy()

    def _free() -> Iterator[int]:
        for i, b in enumerate(blocks):
            if b.id is None:
                yield i

    def _occupied() -> Iterator[int]:
        l_blocks = len(blocks)
        for i, b in enumerate(reversed(blocks)):
            if b.id is not None:
                yield l_blocks - 1 - i

    for l, r in zip(_free(), _occupied()):
        if l >= r:
            break
        blocks[l], blocks[r] = blocks[r], blocks[l]
        
    return _checksum(blocks)

def part2(data) -> int:
    ...

def _main():
    data = _read_data(test=False)

    print(part1(data))
    print(part2(data))

if __name__ == "__main__":
    _main()