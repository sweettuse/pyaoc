from __future__ import annotations
from collections import deque
from gettext import find

from hashlib import md5
from queue import Queue
from typing import Generator, NamedTuple, Optional
from rich import print

from pyaoc2019.utils import timer


Coord = tuple[int, int]  # row, col
INPUT = 'bwnlcvfs'
OPEN = frozenset('bcdef')
TARGET = 3, 3


class CurState(NamedTuple):
    path: str
    pos: Coord


def open_doors(path: str, seed=INPUT) -> list[str]:
    md5sum = md5((seed + path).encode()).hexdigest()
    return [d for v, d in zip(md5sum, 'UDLR') if v in OPEN]


def next_pos(cur, dir: str) -> Optional[Coord]:
    r, c = cur.pos
    match dir:
        case 'U':
            if (r := r - 1) < 0:
                return
        case 'D':
            if (r := r + 1) > 3:
                return
        case 'L':
            if (c := c - 1) < 0:
                return
        case 'R':
            if (c := c + 1) > 3:
                return

    return r, c


def get_next(cur: CurState, seed=INPUT) -> Generator[CurState, None, None]:
    for d in open_doors(cur.path, seed):
        if pos := next_pos(cur, d):
            yield CurState(cur.path + d, pos)


def path(seed=INPUT, *, find_longest: bool = False) -> str | int:
    q: deque[CurState] = deque()
    q.append(CurState('', (0, 0)))
    seen = set()
    longest = 0

    while q:
        cur = q.popleft()
        if cur.pos == TARGET:
            if not find_longest:
                return cur.path

            longest = max(len(cur.path), longest)
            continue

        for n in get_next(cur, seed):
            if n in seen:
                continue
            seen.add(n)
            q.append(n)
    return longest


@timer
def test():
    def _test(s, r, longest=False):
        p = path(s, find_longest=longest)
        assert p == r, f'got {p!r}, expected {r!r}'

    _test('ihgpwlah', 'DDRRRD')
    _test('kglvqrro', 'DDUDRLRRUDRD')
    _test('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR')

    _test('ihgpwlah', 370, True)
    _test('kglvqrro', 492, True)
    _test('ulqzkmiv', 830, True)


def __main():
    test()
    print(f'part1: {path()}')
    print(f'part2: {path(find_longest=True)}')


if __name__ == '__main__':
    __main()
