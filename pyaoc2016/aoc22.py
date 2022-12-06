from __future__ import annotations
from dataclasses import dataclass
from typing import NamedTuple, Sequence
from itertools import product, starmap
from pyaoc2019.utils import mapt, read_file
from rich import print

SAMPLE = list(filter(bool, """
/dev/grid/node-x0-y0     92T   72T    20T   78%
/dev/grid/node-x0-y1     88T   67T    21T   76%
""".splitlines()))

class Coord(NamedTuple):
    x: int
    y: int

@dataclass(unsafe_hash=True)
class Node:
    coord: Coord
    size: int
    used: int
    
    @classmethod
    def from_str(cls, s: str) -> Node:
        """/dev/grid/node-x0-y0     92T   72T    20T   78%"""
        name, size, used, *_ = s.split()
        *_, x, y = name.split('-')
        x = int(x[1:])
        y = int(y[1:])
        size = int(size[:-1])
        used = int(used[:-1])
        return cls(Coord(x, y), size, used)
    
    @property
    def avail(self) -> int:
        return self.size - self.used

def _read_data():
    data = read_file(22, 2016)
    return mapt(Node.from_str, data[2:])

def _is_viable(a: Node, b: Node) -> bool:
    if not a.used:
        return False
    
    if a == b:
        return False

    return a.used <= b.avail

def _get_viable(nodes: Sequence[Node]) -> list[tuple[Node, Node]]:
    return [(a, b) for a, b in product(nodes, repeat=2) if _is_viable(a, b)]

def part1(nodes: Sequence[Node]) -> int:
    return len(_get_viable(nodes))

DATA = _read_data()

def __main():
    for n in DATA:
        if not n.used:
            print(n)
    print(part1(DATA))

__main()
