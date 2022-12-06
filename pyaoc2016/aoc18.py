from __future__ import annotations
from itertools import chain, islice

from typing import Generator


INPUT = '^..^^.^^^..^^.^...^^^^^....^.^..^^^.^.^.^^...^.^.^.^.^^.....^.^^.^.^.^.^.^.^^..^^^^^...^.....^....^.'
TRAPS = frozenset(
    {
        tuple('^^.'),
        tuple('.^^'),
        tuple('^..'),
        tuple('..^'),
    }
)

def take(iterable, n: int):
    res = []
    for _ in range(n):
        res.append(next(iterable))
    return tuple(res)

def generate(row: str) -> Generator[str, None, None]:
    yield row
    while True:
        tiles = iter(chain('.', row, '.'))
        l = next(tiles)
        c = next(tiles)
        next_row = []
        for r in tiles:
            next_row.append('^' if (l, c, r) in TRAPS else '.')
            l, c = c, r 
        row = ''.join(next_row)
        yield row

def parts1and2(n=40):
    g = generate(INPUT)
    return sum(r.count('.') for _, r in zip(range(n), g))

def __main():
    print(f'{parts1and2(40)=}')
    print(f'{parts1and2(400_000)=}')



__main()