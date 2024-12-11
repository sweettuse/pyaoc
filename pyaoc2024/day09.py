from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import dataclass
from itertools import count, repeat
from typing import Iterable, Iterator

from more_itertools import interleave_longest
import rich

# from rich import print

from pyaoc2019.utils import mapl, read_file


@dataclass
class Block:
    id: int | None


@dataclass
class File:
    id: int | None
    start: int
    end: int

    @property
    def size(self) -> int:
        return self.end - self.start


@dataclass
class Node:
    f: File
    next: Node | None = None

    def __iter__(self) -> Iterator[Node]:
        cur = self
        while cur:
            if cur.f:
                yield cur
            cur = cur.next
        ...

    def display(self, n=None) -> None:
        limit = count() if n is None else range(n)
        for _, n in zip(limit, self):
            rich.print(n.f)

    @property
    def occupied(self) -> Iterator[Node]:
        for n in self:
            if n.f.id is not None:
                yield n

    @property
    def free(self) -> Iterator[Node]:
        for n in self:
            if n.f.id is None:
                yield n

    @property
    def blocks(self) -> Iterator[Block]:
        for n in self:
            b = Block(n.f.id)
            for _ in range(n.f.size):
                yield b


def _read_data(*, test: bool) -> list[Block]:
    fname = "09.test.txt" if test else "09.txt"
    data = mapl(int, read_file(fname)[0])
    occupied = list(enumerate(data[::2]))
    free = list(zip(repeat(None), data[1::2]))
    return [
        Block(id)
        for id, size in interleave_longest(occupied, free)
        for _ in range(size)
    ]


def _read_data2(*, test: bool) -> Node:
    fname = "09.test.txt" if test else "09.txt"
    data = mapl(int, read_file(fname)[0])

    def ids():
        c = count()
        while True:
            yield next(c)
            yield None

    res = []
    idx = 0
    cur = head = Node(None)

    for id, size in zip(ids(), data):
        f = File(id, idx, idx + size)
        cur.next = Node(f)
        cur = cur.next
        idx += size

    return head


def _checksum(blocks: Iterable[Block]) -> int:
    return sum(i * b.id for i, b in enumerate(blocks) if b.id is not None)


def _display(blocks: Iterable[Block]) -> None:
    rich.print("".join("." if b.id is None else str(b.id) for b in blocks))


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


def _move(src: Node, target: Node):
    """move and merge any contiguous free space"""
    assert target.f.id is None
    assert target.f.size >= src.f.size

    cur_end = target.f.end

    # move to target
    target.f.id = src.f.id
    target.f.end = target.f.start + src.f.size

    # clear out src
    src.f.id = None
    
    if cur_end == target.f.end:
        return

    assert (t_next := target.next), target

    # insert new free node
    f = File(None, target.f.end, cur_end)
    n = Node(f, t_next)
    target.next = n


def part2(head: Node) -> int:
    file_nodes = list(head.occupied)
    file_nodes.reverse()
    for file_n in file_nodes:
        size = file_n.f.size
        for free_n in head.free:
            if free_n.f.start > file_n.f.start:
                break
            if free_n.f.size >= size:
                _move(file_n, free_n)
                break

    return _checksum(head.blocks)


def _main():
    data = _read_data(test=True)
    print(part1(data))

    head = _read_data2(test=False)
    print(part2(head))


if __name__ == "__main__":
    _main()
