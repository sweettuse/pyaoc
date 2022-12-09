from __future__ import annotations
from bisect import bisect_left
from collections import deque
from dataclasses import dataclass, field
from functools import cached_property
from typing import Literal, Optional

from pyaoc2019.utils import exhaust, read_file


class PutIter:
    def __init__(self, iterable):
        self.it = iter(iterable)
        self._buffer = deque()

    def __iter__(self):
        return self

    def __next__(self):
        if self._buffer:
            return self._buffer.pop()
        return next(self.it)

    def put(self, value):
        self._buffer.appendleft(value)


@dataclass
class Node:
    name: str
    type: Literal['dir', 'file']
    size: int = 0
    children: dict[str, Node] = field(default_factory=dict)
    parent: Optional[Node] = None

    @classmethod
    def from_str(cls, s):
        size_or_dir, name = s.split()
        if size_or_dir == 'dir':
            type = 'dir'
            size = 0
        else:
            type = 'file'
            size = int(size_or_dir)

        return cls(name, type, size)

    @cached_property
    def total_size(self) -> int:
        dir_size = sum(d.total_size for d in self.children.values() if d.type == 'dir')
        file_size = sum(f.size for f in self.children.values() if f.type == 'file')
        return dir_size + file_size


    def add(self, n: Node):
        self.children[n.name] = n

    def __iter__(self):
        yield self
        for n in self.children.values():
            yield from n

    def __str__(self):
        type, name, size = self.type, self.name, self.size
        return f'Node({type=}, {name=}, {size=}'


def parse(name):
    root = Node('/', 'dir')
    data = read_file(name)
    path = []
    cur_dir: Node = root

    def _parse_cd():
        nonlocal cur_dir

        _, target = l.split()
        if target == '/':
            path.clear()
            path.append(root)
            cur_dir = root
        elif target == '..':
            path.pop()
            cur_dir = path[-1]
        else:
            path.append(cur_dir.children[target])
            cur_dir = path[-1]

    def _parse_ls():
        for entry in it:
            if entry.startswith('$'):
                it.put(entry)
                return
            cur_dir.add(Node.from_str(entry))

    it = PutIter(data)
    for l in it:
        if l.startswith('$'):
            l = l[2:]
            if l.startswith('cd'):
                _parse_cd()
            else:  # ls
                _parse_ls()
    
    return root


def part1(name):
    root = parse(name)
    return sum(n.total_size for n in root if n.type == 'dir' and n.total_size < 100000)

def part2(name, ):
    disk_size = 70000000
    needed_for_update = 30000000
    root = parse(name)

    occupied = root.total_size
    cur_free = disk_size - occupied
    need_to_free_up = needed_for_update - cur_free
    dir_sizes = sorted(n.total_size for n in root if n.type == 'dir')
    idx = bisect_left(dir_sizes, need_to_free_up)
    return dir_sizes[idx]


print(part1(7))
print(part2(7))
